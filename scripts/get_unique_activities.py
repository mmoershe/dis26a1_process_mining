import os
import csv

def read_unique_activities(directory) -> set[str]:
    unique_activities = set()

    with open(directory, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'ACTIVITY_EN' in row and row['ACTIVITY_EN']:
                unique_activities.add(row['ACTIVITY_EN'])

    return unique_activities

if __name__ == "__main__": 
    SCRIPTS_DIRECTORY: str = os.path.dirname(__file__)
    BASE_DIRECTORY: str = os.path.dirname(SCRIPTS_DIRECTORY)
    DATA_DIRECTORY: str = os.path.join(BASE_DIRECTORY, "data")
    ACTIVITY_DIRECTORY: str = os.path.join(DATA_DIRECTORY, "activity.csv")
    unique_activities: set[str] = read_unique_activities(ACTIVITY_DIRECTORY) 

    for i, activity in enumerate(unique_activities): 
        print(f"{i}\t{activity}")
