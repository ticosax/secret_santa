import tomllib

import click
from ortools.sat.python import cp_model


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def assign_pairs(filename):
    with open(filename, "rb") as f:
        data = tomllib.load(f)
    model = cp_model.CpModel()
    per_giver_vars = {}
    per_receiver_vars = {}

    for giver, data_giver in data["participants"].items():
        for receiver in data["participants"]:
            if giver == receiver:
                continue
            var = model.NewBoolVar(f"{giver} => {receiver}")
            per_giver_vars.setdefault(giver, []).append(var)
            per_receiver_vars.setdefault(receiver, []).append(var)
            if receiver in data_giver["exclusions"]:
                model.Add(var == 0)

    for receivers in per_giver_vars.values():
        model.Add(sum(receivers) == 1)
    for givers in per_receiver_vars.values():
        model.Add(sum(givers) == 1)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL
    for giver, giver_vars in per_giver_vars.items():
        for var in giver_vars:
            if solver.BooleanValue(var):
                receiver = next(
                    (
                        receiver
                        for receiver, vars_ in per_receiver_vars.items()
                        if var in vars_
                    )
                )
                print(f"{giver} should give to {receiver} ")


if __name__ == "__main__":
    assign_pairs()
