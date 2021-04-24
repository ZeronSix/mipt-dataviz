from label import Label
from pysat.solvers import Glucose3
import itertools


class Placer:
    def __init__(self, labels: list):
        self.labels = labels
        self.variable_to_id = dict()
        self.id_to_variable = dict()

    def variable_index(self, label_id: int, offset_id: int) -> int:
        variable_name = f'{label_id}_{offset_id}'
        if variable_name not in self.variable_to_id:
            variable_id = len(self.variable_to_id) + 1
            self.variable_to_id[variable_name] = variable_id
            self.id_to_variable[variable_id] = variable_name

        return self.variable_to_id[variable_name]

    def make_intersection_clauses(self):
        forbidden = []

        label_ids = list(range(0, len(self.labels)))
        for first_id, second_id in itertools.product(label_ids, label_ids):
            if first_id == second_id:
                continue

            first_label = self.labels[first_id]
            second_label = self.labels[second_id]

            first_offset_ids = list(range(0, len(first_label.placement_offsets)))
            second_offset_ids = list(range(0, len(second_label.placement_offsets)))
            for first_offset_id, second_offset_id in itertools.product(first_offset_ids, second_offset_ids):
                first_offset = first_label.placement_offsets[first_offset_id]
                second_offset = second_label.placement_offsets[second_offset_id]

                first_rect = first_label.generate_rect(first_offset)
                second_rect = second_label.generate_rect(second_offset)

                if first_rect.intersects(second_rect):
                    forbidden.append([-self.variable_index(first_id, first_offset_id),
                                      -self.variable_index(second_id, second_offset_id)])

        return forbidden

    @staticmethod
    def make_only_one_true_variable_clauses(variables):
        clauses = []
        for length in range(len(variables) + 1):
            if length == 1:
                continue

            combinations = [set(combination) for combination in itertools.combinations(variables, length)]
            for combination in combinations:
                clause = []
                for variable in variables:
                    clause.append(variable if variable not in combination else -variable)
                clauses.append(clause)

        return clauses

    def make_offset_selection_clauses(self):
        clauses = []

        for label_id in range(len(self.labels)):
            label = self.labels[label_id]

            variables = []
            for offset_id in range(len(label.placement_offsets)):
                variables.append(self.variable_index(label_id, offset_id))
            clauses += self.make_only_one_true_variable_clauses(variables)

        return clauses

    def place(self) -> list:
        solver = Glucose3()
        clauses = self.make_intersection_clauses() + self.make_offset_selection_clauses()
        for clause in clauses:
            solver.add_clause(clause)

        if not solver.solve():
            raise ValueError('Impossible placement: no solution!')

        placements = []
        for variable in solver.get_model():
            if variable < 0:
                continue  # Means false

            label_id, offset_id = map(int, self.id_to_variable[variable].split('_'))
            label = self.labels[label_id]
            rectangle = label.generate_rect(label.placement_offsets[offset_id])
            placements.append((rectangle, label.pos))

        return placements
