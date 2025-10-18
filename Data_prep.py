
import json
import os

def list_files_recursive(path):
    res = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            res = res + list_files_recursive(full_path)
        else:
            res.append(full_path)
    return res


# Combine all the individual CVE files into one file per year.
path = "./data/cvelistV5-main/cves/"
for year in os.listdir(path):
    files = list_files_recursive(path + year)

    result_file = open("./data/CVEs/CVEs-" + year + ".json", "w")
    result_file.write("[\n")
    for file in files:
        data = open(file, 'r').read().replace("\n", " ") + ",\n"
        result_file.write(data)

    result_file.seek(result_file.tell() - 2, os.SEEK_SET)
    result_file.write("\n]")
    result_file.close()

# Combine all year files into one file with only the important fields.
path = "./data/CVEs/"
result_file = open("./data/CVEs_short.json", "w")
result_file.write("[\n")
count = 0
for file in os.listdir(path):
    data = open(path+file, 'r')
    cves = json.load(data)
    for cve in cves:
        if cve["cveMetadata"]["state"] != "PUBLISHED":
            continue
        tiny_cve = {
            "id": cve["cveMetadata"]["cveId"],
            "timestamp": cve["cveMetadata"]["datePublished"],
        }
        if "affected" in cve["containers"]["cna"].keys() and "packageName" in cve["containers"]["cna"]["affected"][0].keys():
            tiny_cve["packageName"] = cve["containers"]["cna"]["affected"][0]["packageName"]
        else:
            tiny_cve["packageName"] = "n/a"
        tiny_cve["description"] = cve["containers"]["cna"]["descriptions"][0]["value"]
        if "programFiles" in cve["containers"]["cna"]["affected"][0].keys():
            tiny_cve["openSource"] = "true"
        else:
            tiny_cve["openSource"] = "unknown"

        result_file.write(json.dumps(tiny_cve) + ",\n")

result_file.seek(result_file.tell() - 2, os.SEEK_SET)
result_file.write("\n]")
result_file.close()



