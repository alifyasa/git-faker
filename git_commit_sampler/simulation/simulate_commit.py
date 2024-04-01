import numpy as np

from datetime import datetime, timedelta
from git_commit_sampler.simulation.constants import DAY, MINUTE, EPSILON
from git_commit_sampler.simulation.poisson import generate_poisson_functions

SimulationResult = np.ndarray

def simulate(
        start_time: datetime, end_time: datetime,
        iter_time_step = 7 * DAY
    ):
    timestamp_start = int(start_time.timestamp())
    timestamp_end = int(end_time.timestamp())

    T = timestamp_end - timestamp_start
    sim_result: SimulationResult = np.array([])

    for time_part_start in range(0, T, iter_time_step):

        time_step = min(7 * DAY, T - time_part_start)
        
        print(f"Simulating {time_step // DAY} DAYS FROM {datetime.fromtimestamp(timestamp_start)}")

        __sim_result = __simulate(time_step, timestamp_start)
        sim_result = np.append(sim_result, __sim_result)

        if sim_result.size == 0:
            break

        timestamp_start = sim_result[-1]
    
    return sim_result
    
def __simulate(T: float, start_time: int):
    _, mu, tau, _ = generate_poisson_functions(T, start_time)
    
    s_h, t_h = 0, 0
    t_nh: np.ndarray = np.array([])
    while True:
        u = np.random.uniform(EPSILON, 1)
        s_h = - np.log( 1 - u )

        if t_h + s_h > mu(T):
            return t_nh + start_time
        
        t_h += s_h       
        t_nh = np.append(t_nh, tau(t_h))
        
def generate_report(
        result: SimulationResult, start_time: datetime, end_time: datetime,
        print_timestamps = False
    ):
    timestamp_start = int(start_time.timestamp())
    timestamp_end = int(end_time.timestamp())

    if print_timestamps:
        for t in result:
            print(datetime.fromtimestamp(t))
    

    print("\n\n" + "=" * 30, "REPORT", "=" * 30)
    print(f"COMMIT COUNT         : {result.size} commits")
    print(f"TOTAL SIMULATION DAY : {(timestamp_end - timestamp_start) / DAY} DAY")
    print(f"MEAN                 : {(result.size / (timestamp_end - timestamp_start) * DAY):.2f} commits per day")


if __name__ == "__main__":
    start_time = datetime.now()
    end_time = start_time + timedelta(days=365)

    sim_result = simulate(start_time, end_time)
    generate_report(sim_result, start_time, end_time)
