import json
import time
import os

import requests

max_num = 252000
i = 0
result_file = open("./data/CVE_metrics.json", "w")
result_file.write("[\n")
while i < max_num:
    print(i)
    cves = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0\?startIndex=" + str(i)).json()
    for entry in cves["vulnerabilities"]:
        cve = entry["cve"]
        smaller_cve = {
            "id": cve["id"],
            "metrics": cve["metrics"]
        }
        result_file.write(json.dumps(smaller_cve) + ",\n")
    i += 2000
    time.sleep(6.1) # Max 5 API calls in 30 seconds

result_file.seek(result_file.tell() - 2, os.SEEK_SET)
result_file.write("\n]")
result_file.close()