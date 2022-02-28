from ortools.linear_solver import pywraplp


def main():
    data = {}

    #what exactly are those weights? // werden für die Berechnung der Constraints gebraucht
    data['weights'] = [
       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    data['function_CPU'] = [
        100, 250, 75, 50, 35, 250, 150, 200, 250, 90, 100, 100, 150, 250, 200
    ]
    assert len(data['weights']) == len(data['function_CPU'])
    data['num_items'] = len(data['weights'])
    data['all_items'] = range(data['num_items'])

    data['bin_capacities'] = [500, 500, 500, 500, 500]
    data['num_bins'] = len(data['bin_capacities'])
    data['all_bins'] = range(data['num_bins'])

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print('SCIP solver unavailable.')
        return

    # Variables.
    # x[i, b] = 1 if item i is packed in bin b.
    x = {}
    for i in data['all_items']:
        for b in data['all_bins']:
            x[i, b] = solver.BoolVar(f'x_{i}_{b}')

    # Constraints.
    # Each item is assigned to at most one bin.
    for i in data['all_items']:
        solver.Add(sum(x[i, b] for b in data['all_bins']) <= 1)

    # The amount packed in each bin cannot exceed its capacity.
    for b in data['all_bins']:
        solver.Add(
            sum(x[i, b] * data['weights'][i]
                for i in data['all_items']) <= data['bin_capacities'][b])

    # Objective.
    # Maximize total value of packed items.
    objective = solver.Objective()
    for i in data['all_items']:
        for b in data['all_bins']:
            objective.SetCoefficient(x[i, b], data['function_CPU'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Total packed value: {objective.Value()}')
        total_weight = 0
        for b in data['all_bins']:
            print(f'Bin {b}')
            bin_weight = 0
            bin_value = 0
            for i in data['all_items']:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]} value: {data['function_CPU'][i]}"
                    )
                    bin_weight += data['weights'][i]
                    bin_value += data['function_CPU'][i]
            print(f'Packed bin weight: {bin_weight}')
            print(f'Packed bin value: {bin_value}\n')
            total_weight += bin_weight
        print(f'Total packed weight: {total_weight}')
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()