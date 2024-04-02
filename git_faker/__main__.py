"""
Git Faker

Simulate git commit using non-homogenenous poisson process and create a git
repository based on simulation result.
"""

from datetime import datetime, timedelta

from git_faker.simulation import simulate, generate_report
from git_faker.create import create_simulated_repository, generate_random_string
from git_faker.simulation import DAY


if __name__ == "__main__":

    start_time = datetime.now()
    end_time = start_time + timedelta(days=45 * 365)  # 45 Years

    sim_result_path = f"output/simulation/{start_time.date()} to {end_time.date()}.txt"

    sim_result = simulate(start_time, end_time)
    generate_report(sim_result, start_time, end_time, write_to_file=sim_result_path)

    create_simulated_repository(
        sim_result_path, f"../shadow-git-{generate_random_string(8)}/"
    )
