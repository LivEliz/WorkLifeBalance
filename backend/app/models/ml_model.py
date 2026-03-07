print("=== ML MODEL MODULE LOADED ===")

import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "weekly_worklife_dataset.csv")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# -------------------------------------------------
# Convert label to numeric
# -------------------------------------------------

label_map = {
    "POOR": 0,
    "MODERATE": 1,
    "GOOD": 2
}

df["wlb_label"] = df["wlb_label"].map(label_map)

# -------------------------------------------------
# Range to numeric mappings
# -------------------------------------------------

range_maps = {

"hours_worked":{
"<35":32,"35-40":38,"40-45":43,"45-50":48,">50":55
},

"overtime_hours":{
"None":0,"1-5":3,"6-10":8,"11-15":13,">15":18
},

"projects_handled":{
"1":1,"2-3":3,"4-5":5,"6-8":7,">8":9
},

"meetings_count":{
"0-5":3,"6-10":8,"11-15":13,"16-20":18,">20":25
},

"breaks":{
"None":0,"1":1,"2":2,"3":3,"4+":4
},

"family_time":{
"<3":2,"3-5":4,"6-10":8,"11-15":12,">15":16
},

"break_duration":{
"<10":5,"10-20":15,"20-30":25,"30-45":35,">45":50
},

"commute_time":{
"No commute":0,"<30":20,"30-60":45,"1-2h":90,">2h":150
},

"sick_days":{
"None":0,"1":1,"2":2,"3":3,"4+":4
},

"leave_days":{
"None":0,"1":1,"2":2,"3":3,"4+":4
},

"travel":{
"No travel":0,"1 trip":1,"2 trips":2,"3 trips":3,">3 trips":4
},

"task_delay":{
"Never":0,"Rarely":1,"Sometimes":2,"Often":3,"Always":4
}

}

# Apply mappings
for col, mapping in range_maps.items():
    if col in df.columns:
        df[col] = df[col].map(mapping)

# -------------------------------------------------
# Feature Selection
# -------------------------------------------------

features = [

"hours_worked",
"overtime_hours",
"projects_handled",
"meetings_count",

"workload_rating",
"deadline_pressure",

"productivity_rating",
"task_delay",

"breaks",
"break_duration",

"sick_days",
"leave_days",

"exhaustion_rating",

"travel",
"travel_enjoyment",

"family_time",
"social_satisfaction",

"commute_time"
]

X = df[features]
y = df["wlb_label"]

# -------------------------------------------------
# Feature Scaling
# -------------------------------------------------

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

# -------------------------------------------------
# Train/Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# Train RandomForest
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Model trained successfully")
print("Accuracy:", round(accuracy * 100, 2), "%")

# -------------------------------------------------
# Reverse Label Map
# -------------------------------------------------

reverse_label = {
0:"POOR",
1:"MODERATE",
2:"GOOD"
}

# -------------------------------------------------
# Prediction Function
# -------------------------------------------------

def predict_wlb(user_data:dict):

    sample = pd.DataFrame([user_data])

    for col, mapping in range_maps.items():
        if col in sample.columns:
            sample[col] = sample[col].map(mapping)

    sample_scaled = scaler.transform(sample)

    pred = model.predict(sample_scaled)[0]

    probs = model.predict_proba(sample_scaled)[0]

    confidence = round(np.max(probs)*100,2)

    label = reverse_label[pred]

    return {
        "wlb_label": label,
        "confidence": confidence
    }