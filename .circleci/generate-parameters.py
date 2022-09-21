import json
import os

java_services = ["balancereader", "ledgerwriter", "transactionhistory"]
python_services = ["frontend", "contacts", "userservice"]

params = {
    "java-services": [],
    "python-services": [],
    "all-services": []
}

if os.environ.get("CIRCLE_BRANCH") == "main":
    params = {
        "java-services": [*java_services],
        "python-services": [*python_services],
        "all-services": [*java_services, *python_services] 
    }
else:
    with open('.circleci/filter-services.json') as f:
        filtered = json.load(f)

    for service in [*filtered]:
        if service in java_services:
            params.get("java-services").append(service)
        if service in python_services:
            params.get("python-services").append(service)

with open('.circleci/pipeline-parameters.json', 'w') as f:
  json.dump(params, f, ensure_ascii=False)

print("Generated pipeline parameters:", params)
