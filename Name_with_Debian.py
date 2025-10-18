import json
import os

# First get the name of all CVEs present in the Debian dataset (44833)

## Invert the Debian dataset dict
debian_cves = open("./data/Debian CVEs.json")
debian_dict = json.load(debian_cves)
inverted_debian_dict = {}
for package_name in debian_dict.keys():
    cve_ids = list(debian_dict[package_name].keys())
    for cve_id in cve_ids:
        inverted_debian_dict[cve_id] = package_name

## Annotate each CVE that appears in the Debian data and save to new file
data = open("./data/CVEs_short.json", 'r')
cves = json.load(data)
debian_cve_ids = inverted_debian_dict.keys()
result_file = open("./data/CVEs_short_debian_named.json" , "w")
result_file.write("[\n")
for cve in cves:
    if cve["id"] in debian_cve_ids:
        cve["name"] = inverted_debian_dict[cve["id"]]
    else:
        cve["name"] = ""
    result_file.write(json.dumps(cve) + ",\n")
result_file.seek(result_file.tell() - 2, os.SEEK_SET)
result_file.write("\n]")
result_file.close()