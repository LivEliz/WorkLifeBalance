import random
import pandas as pd

roles = ["Entry Level","Mid Level","Senior Level","Manager / Lead","Executive / Director"]
age_groups = ["18-25","26-35","36-45","46-55","55+"]
marital_status = ["Single","Married","Divorced","Widowed"]
children = ["No children","1 child","2 children","3+ children"]

work_modes = ["Work From Home","Hybrid","Office Only"]
official_hours = ["8-4","9-5","10-6","11-7","Rotational","Night"]

commute = ["No commute","<30","30-60","1-2h",">2h"]

hours_ranges = ["<35","35-40","40-45","45-50",">50"]
overtime_ranges = ["None","1-5","6-10","11-15",">15"]

projects_ranges = ["1","2-3","4-5","6-8",">8"]
meetings_ranges = ["0-5","6-10","11-15","16-20",">20"]

task_delay = ["Never","Rarely","Sometimes","Often","Always"]

breaks = ["None","1","2","3","4+"]
break_duration = ["<10","10-20","20-30","30-45",">45"]

sick_days = ["None","1","2","3","4+"]
leave_days = ["None","1","2","3","4+"]

travel = ["No travel","1 trip","2 trips","3 trips",">3 trips"]

family_time = ["<3","3-5","6-10","11-15",">15"]


# Numeric helpers for WLB calculation
hours_score = {"<35":35,"35-40":38,"40-45":43,"45-50":48,">50":55}
overtime_score = {"None":0,"1-5":3,"6-10":8,"11-15":13,">15":18}
projects_score = {"1":1,"2-3":3,"4-5":5,"6-8":7,">8":9}
meetings_score = {"0-5":3,"6-10":8,"11-15":13,"16-20":18,">20":25}
breaks_score = {"None":0,"1":1,"2":2,"3":3,"4+":4}
family_score = {"<3":2,"3-5":4,"6-10":8,"11-15":12,">15":16}


def calculate_wlb(row):

    score = 100

    score -= max(0, hours_score[row["hours_worked"]] - 40) * 0.8
    score -= overtime_score[row["overtime_hours"]] * 1.5
    score -= projects_score[row["projects_handled"]] * 0.8
    score -= meetings_score[row["meetings_count"]] * 0.5

    score -= row["workload_rating"] * 2
    score -= row["deadline_pressure"] * 2

    score -= row["exhaustion_rating"] * 3

    score -= row["sick_days_num"] * 3

    score += breaks_score[row["breaks"]] * 2

    score += family_score[row["family_time"]]

    score += row["social_satisfaction"] * 2

    score += row["productivity_rating"]

    score += row["travel_enjoyment"] * 0.5

    score = max(0, min(100, int(score)))

    if score < 40:
        label = "POOR"
    elif score < 70:
        label = "MODERATE"
    else:
        label = "GOOD"

    return score, label


def generate_employee():

    role = random.choice(roles)

    if role == "Entry Level":
        projects = random.choice(["1","2-3"])
    elif role == "Mid Level":
        projects = random.choice(["2-3","4-5"])
    elif role == "Senior Level":
        projects = random.choice(["4-5","6-8"])
    else:
        projects = random.choice(["6-8",">8"])

    commute_choice = random.choice(commute)

    if commute_choice in ["1-2h",">2h"]:
        exhaustion = random.randint(3,5)
    else:
        exhaustion = random.randint(1,4)

    overtime = random.choice(overtime_ranges)

    if overtime in ["11-15",">15"]:
        workload = random.randint(4,5)
    else:
        workload = random.randint(1,4)

    productivity = max(1, 6 - exhaustion + random.randint(-1,1))

    sick = random.choice(sick_days)
    sick_num = 0 if sick == "None" else int(sick.replace("+",""))

    row = {

        "age_group": random.choice(age_groups),
        "marital_status": random.choice(marital_status),
        "children": random.choice(children),

        "role_level": role,

        "official_work_hours": random.choice(official_hours),
        "work_mode": random.choice(work_modes),
        "commute_time": commute_choice,

        "hours_worked": random.choice(hours_ranges),
        "overtime_hours": overtime,

        "projects_handled": projects,
        "meetings_count": random.choice(meetings_ranges),

        "workload_rating": workload,
        "deadline_pressure": random.randint(1,5),

        "productivity_rating": productivity,
        "task_delay": random.choice(task_delay),

        "breaks": random.choice(breaks),
        "break_duration": random.choice(break_duration),

        "sick_days": sick,
        "sick_days_num": sick_num,

        "leave_days": random.choice(leave_days),

        "exhaustion_rating": exhaustion,

        "travel": random.choice(travel),
        "travel_enjoyment": random.randint(1,5),

        "family_time": random.choice(family_time),
        "social_satisfaction": random.randint(1,5)

    }

    score, label = calculate_wlb(row)

    row["wlb_score"] = score
    row["wlb_label"] = label

    return row


dataset = []

for i in range(5000):
    dataset.append(generate_employee())

df = pd.DataFrame(dataset)

df.to_csv("weekly_worklife_dataset.csv", index=False)

print("Dataset generated:", len(df))

