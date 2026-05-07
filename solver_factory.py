from solver import BacktrackingSolver


class SolverFactory:
    def create_solver(self, solver_type):
        if solver_type == "backtracking":
            return BacktrackingSolver()

        return None