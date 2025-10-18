import json
import os
import random

names = json.load(open("./data/Names_annotated_Debian.json", "r"))
path = "./data/Names_annotated/"
for file in os.listdir(path):
    names_year = json.load(open(path + file, 'r'))
    for name in names_year.keys():
        if names_year[name]["open_source"] != "":
            names[name] = names_year[name]


path = "./data/CVEs_named/"
cves = []
for file in os.listdir(path):
    cves_year = json.load(open(path + file, 'r'))
    cves += cves_year


cves_scored = json.load(open("./data/CVE_metrics.json", 'r'))
cves_scored_dict = {entry["id"]: entry["metrics"] for entry in cves_scored}

cves_annotated_scored = []
for cve in cves:
    annotation = names[cve["name"]]["open_source"].lower()
    if "open" in annotation or "true" in annotation:
        open_source = "true"
    elif "closed" in annotation or "false" in annotation:
        open_source = "false"
    else:
        open_source = "unknown"
    annotated_cve = {
        "id": cve["id"],
        "timestamp": cve["timestamp"],
        "package_name": cve["name"],
        "open_source": open_source,
        "metrics": cves_scored_dict[cve["id"]]
    }
    cves_annotated_scored.append(annotated_cve)










