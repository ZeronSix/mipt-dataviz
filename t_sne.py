import numpy as np

ITERATIONS = 1000
MOMENTUM = 0.5
ETA = 500
MIN_GAIN = 0.01
ITERATION_LOG_STEP = 50
P_EPS = 1e-12


def compute_entropy_and_kernel(distances: np.ndarray, beta: float) -> tuple:
    kernel = np.exp(-distances * beta)
    kernel_sum = np.sum(kernel)
    entropy = np.log(kernel_sum) + beta * np.sum(distances * kernel) / kernel_sum
    kernel = kernel / kernel_sum

    return entropy, kernel


def compute_non_symmetric_similarities(objects: np.ndarray, perplexity: float, eps: float = 1e-5,
                                       attempts: int = 50) -> np.ndarray:
    num_objects, dimensions = objects.shape
    sum_object_squares = np.sum(np.square(objects), 1)
    similarity_matrix = np.zeros((num_objects, num_objects))
    distances = np.add(np.add(-2 * np.dot(objects, objects.T), sum_object_squares).T, sum_object_squares)
    betas = np.ones((num_objects, 1))  # beta = 1 / sigma
    log_perplexity = np.log(perplexity)

    for i in range(num_objects):
        beta_min = -np.inf
        beta_max = np.inf
        distance_row = distances[i, np.concatenate((np.r_[0:i], np.r_[i + 1:num_objects]))]

        kernel = None

        for attempt in range(attempts):
            entropy, kernel = compute_entropy_and_kernel(distance_row, betas[i])

            entropy_diff = np.abs(entropy - log_perplexity)

            if entropy_diff <= eps:
                break

            if entropy > log_perplexity:
                beta_min = betas[i]
                if beta_max == np.inf or beta_max == -np.inf:
                    betas[i] = betas[i] * 2.0
                else:
                    betas[i] = (betas[i] + beta_max) / 2.0
            else:
                beta_max = betas[i]
                if beta_min == np.inf or beta_min == -np.inf:
                    betas[i] = betas[i] / 2.0
                else:
                    betas[i] = (betas[i] + beta_min) / 2.0

            entropy, kernel = compute_entropy_and_kernel(distance_row, betas[i])

        similarity_matrix[i, np.concatenate((np.r_[0:i], np.r_[i + 1:num_objects]))] = kernel

    return similarity_matrix


def compute_symmetric_similarities(objects: np.ndarray, perplexity: float) -> np.ndarray:
    similarities = compute_non_symmetric_similarities(objects, perplexity)
    similarities = similarities + np.transpose(similarities)
    similarities = similarities / np.sum(similarities)
    similarities = np.maximum(similarities, P_EPS)

    return similarities


def compute_y_similarities(y: np.ndarray) -> np.ndarray:
    num_objects, _ = y.shape

    sum_y = np.sum(np.square(y), 1)
    similarities = -2.0 * np.dot(y, y.T)
    similarities = 1.0 / (1.0 + np.add(np.add(similarities, sum_y).T, sum_y))
    similarities[range(num_objects), range(num_objects)] = 0

    return similarities


def t_sne(objects: np.ndarray, perplexity: float = 30.0) -> np.ndarray:
    num_objects, dimensions = objects.shape
    y = np.random.randn(num_objects, 2)
    delta_y = np.zeros((num_objects, 2))
    i_y = np.zeros((num_objects, 2))
    gains = np.ones((num_objects, 2))

    p = compute_symmetric_similarities(objects, perplexity)
    print(f'Running {ITERATIONS} iterations...')
    for iteration in range(ITERATIONS):
        y_similarities = compute_y_similarities(y)
        q = y_similarities / np.sum(y_similarities)
        q = np.maximum(q, P_EPS)

        diff = p - q
        for i in range(num_objects):
            delta_y[i, :] = np.sum(np.tile(diff[:, i] * y_similarities[:, i], (2, 1)).T * (y[i, :] - y), 0)

        # See https://habr.com/ru/post/267041/
        gains = (gains + 0.2) * ((delta_y > 0) != (i_y > 0)) + \
                (gains * 0.8) * ((delta_y > 0) == (i_y > 0))
        gains[gains < MIN_GAIN] = MIN_GAIN
        i_y = MOMENTUM * i_y - ETA * (gains * delta_y)
        y = y + i_y
        y = y - np.tile(np.mean(y, 0), (num_objects, 1))

        if iteration % ITERATION_LOG_STEP == 0:
            loss = np.sum(p * np.log(p / q))
            print(f'Iteration {iteration}, loss {loss}')

    return y
