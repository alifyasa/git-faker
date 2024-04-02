"""
Gather all function related to simulation and wrap it into one function.
"""

from datetime import datetime, timedelta, timezone

import numpy as np

from git_faker.simulation.constants import DAY, EPSILON
from git_faker.simulation.poisson import generate_poisson_functions

SimulationResult = np.ndarray


def simulate(start_time: datetime, end_time: datetime, iter_time_step=7 * DAY):
    """
    Simulate Git Commit.
    """

    timestamp_start = start_time.timestamp()
    timestamp_end = end_time.timestamp()

    total_time = int(timestamp_end - timestamp_start)
    sim_result: SimulationResult = np.array([])

    for time_part_start in range(0, total_time, iter_time_step):

        time_step = min(iter_time_step, total_time - time_part_start)

        print(
            f"SIMULATING {time_step // DAY} DAYS FROM {datetime.fromtimestamp(timestamp_start)} UTC"
        )
        progress_bar(time_part_start / total_time)

        __sim_result = __simulate(time_step, timestamp_start)
        sim_result = np.append(sim_result, __sim_result)

        if sim_result.size == 0:
            break

        timestamp_start = sim_result[-1]

        clean_progress_bar()

    return sim_result


def __simulate(total_time: float, start_time: float):
    """
    Helper function for iterating long total_time
    """

    _, mu, tau, _ = generate_poisson_functions(total_time, start_time)

    s_h, t_h = 0, 0
    t_nh: np.ndarray = np.array([])
    while True:
        u = np.random.uniform(EPSILON, 1)
        s_h = -np.log(1 - u)

        if t_h + s_h > mu(total_time):
            return t_nh + start_time

        t_h += s_h
        t_nh = np.append(t_nh, tau(t_h))


def progress_bar(percentage: float):
    """
    Print a progress bar
    """

    print(f"[{('=' * int(percentage * 0.7 * 100)):<70}] {percentage:.2%}", end="\r")


def clean_progress_bar():
    """
    Clean progress bar residue
    """

    print(" " * 80, end="\r")


def generate_report(
    result: SimulationResult,
    start_time: datetime,
    end_time: datetime,
    print_timestamps=False,
    write_to_file: str = None,
):
    """
    Write simulation result to stdout or a file
    """

    timestamp_start = start_time.timestamp()
    timestamp_end = end_time.timestamp()
    current_timezone = datetime.now().astimezone().tzinfo

    if print_timestamps:
        for t in result:
            print(datetime.fromtimestamp(t, current_timezone))

    if write_to_file:
        with open(write_to_file, "w", encoding="utf-8") as f:
            for t in result:
                # Write without timezone information
                f.write(f"{datetime.fromtimestamp(t)}\n")

    print("\n\n" + "=" * 36, "REPORT", "=" * 36)
    commit_count = result.size
    print(f"COMMIT COUNT         : {commit_count} commits")
    total_simulation_day = (timestamp_end - timestamp_start) / DAY
    print(f"TOTAL SIMULATION DAY : {total_simulation_day} DAY")
    mean_commit_per_day = commit_count / total_simulation_day
    print(f"MEAN                 : {mean_commit_per_day:.2f} commits per day")


if __name__ == "__main__":
    sim_start_time = datetime.now()
    sim_end_time = sim_start_time + timedelta(days=45 * 365)

    simulation_result = simulate(sim_start_time, sim_end_time)
    generate_report(
        simulation_result,
        sim_start_time,
        sim_end_time,
        write_to_file=f"output/simulation/{sim_start_time.date()} to {sim_end_time.date()}.txt",
    )
