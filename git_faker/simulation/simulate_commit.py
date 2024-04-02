import numpy as np

from datetime import datetime, timedelta
from git_faker.simulation.constants import DAY, MINUTE, EPSILON
from git_faker.simulation.poisson import generate_poisson_functions

SimulationResult = np.ndarray


def simulate(
    start_time: datetime, end_time: datetime,
    iter_time_step=7 * DAY
):
    timestamp_start = start_time.timestamp()
    timestamp_end = end_time.timestamp()

    T = int(timestamp_end - timestamp_start)
    sim_result: SimulationResult = np.array([])

    for time_part_start in range(0, T, iter_time_step):

        time_step = min(7 * DAY, T - time_part_start)

        print(
            f"Simulating {time_step // DAY} DAYS FROM {datetime.fromtimestamp(timestamp_start)}")
        progress_bar(time_part_start / T)

        __sim_result = __simulate(time_step, timestamp_start)
        sim_result = np.append(sim_result, __sim_result)

        if sim_result.size == 0:
            break

        timestamp_start = sim_result[-1]

        clean_progress_bar()

    return sim_result


def __simulate(T: float, start_time: float):
    _, mu, tau, _ = generate_poisson_functions(T, start_time)

    s_h, t_h = 0, 0
    t_nh: np.ndarray = np.array([])
    while True:
        u = np.random.uniform(EPSILON, 1)
        s_h = - np.log(1 - u)

        if t_h + s_h > mu(T):
            return t_nh + start_time

        t_h += s_h
        t_nh = np.append(t_nh, tau(t_h))


def progress_bar(percentage: float):
    print(
        f"[{('=' * int(percentage * 0.7 * 100)):<70}] {percentage:.2%}",
        end='\r')


def clean_progress_bar():
    print(" " * 80, end='\r')


def generate_report(
    result: SimulationResult, start_time: datetime, end_time: datetime,
    print_timestamps=False,
    write_to_file: str = None
):
    timestamp_start = start_time.timestamp()
    timestamp_end = end_time.timestamp()

    if print_timestamps:
        for t in result:
            print(datetime.fromtimestamp(t))

    if write_to_file:
        with open(write_to_file, "w") as f:
            for t in result:
                f.write(f"{datetime.fromtimestamp(t)}\n")

    print("\n\n" + "=" * 36, "REPORT", "=" * 36)
    print(f"COMMIT COUNT         : {result.size} commits")
    print(
        f"TOTAL SIMULATION DAY : {(timestamp_end - timestamp_start) / DAY} DAY")
    print(
        f"MEAN                 : {(result.size / (timestamp_end - timestamp_start) * DAY):.2f} commits per day")


if __name__ == "__main__":
    start_time = datetime.now()
    end_time = start_time + timedelta(days=45 * 365)

    sim_result = simulate(start_time, end_time)
    generate_report(
        sim_result, start_time, end_time,
        write_to_file=f"output/simulation/{start_time.date()} to {end_time.date()}.txt"
    )
