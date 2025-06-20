import csv

from datetime import date, timedelta
import random

deps = [
    'finance',
    'production',
    'sales',
    'support',
    'marketing'
]

statuses = [
    "On_Duty", "Remote_Work", "Vacation", "Sick_Leave",
    "Maternity_Leave", "Paternity_Leave", "Emergency_Leave",
    "Retired", "Hybrid_Work", "Personal_Day"
]


def data_gen(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        for dep in deps:
            for status in statuses:
                value = random.randint(1, 20)
                yield [current_date.year, current_date.month, current_date.day, dep, status, value]
        current_date += timedelta(days=1)

if __name__ == "__main__":
    for year, month, day, dep, status, value in data_gen(2019, 2024):
        print(f"{year}-{month}-{day}-{dep}-{status}-{value}")
