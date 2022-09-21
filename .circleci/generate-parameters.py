import json
import os

all_java_services = ["balancereader", "ledgerwriter", "transactionhistory"]
all_python_services = ["frontend", "contacts", "userservice"]

params = {}

if os.environ.get("CIRCLE_BRANCH") == "main":
    params = {
        "java-services": all_java_services,
        "python-services": all_python_services,
        "all-services": [*all_java_services, *all_python_services] 
    }
else:
    java_tracker = []
    python_tracker = []

    with open('.circleci/filter-services.json') as f:
        filtered = json.load(f)
    for service in [*filtered]:
        if service in all_java_services:
            java_tracker.append(service)
        if service in all_python_services:
            python_tracker.append(service)

    if len(java_tracker):
        params["java-services"] = java_tracker
    if len(python_tracker):
        params["python-services"] = python_tracker

with open('.circleci/pipeline-parameters.json', 'w') as f:
  json.dump(params, f, ensure_ascii=False)

print("Generated pipeline parameters:", params)
