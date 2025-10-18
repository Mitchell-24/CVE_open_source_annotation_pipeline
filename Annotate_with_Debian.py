import json
import os



# Make a dict of all the names
names = {}
path = "./data/CVEs_named/"
for file in os.listdir(path):
    data = open(path + file, 'r')
    cves = json.load(data)
    year = cves[0]["timestamp"].split("-")[0]
    for cve in cves:
        name = cve["name"]
        if name not in names.keys():
            years = set()
            years.add(int(year))
            names[name] = {
                "open_source": "",
                "years": years
            }
        else:
            years = names[name]["years"]
            years.add(int(year))
            names[name]["years"] = years

        # Annotate with true the CVEs which we already found to have a link to the repo.
        if cve["openSource"] == "true":
            names[name]["open_source"] = "true"

#
data = json.load(open("./data/Debian-packages.json", "r"))
debian_names = list(map(lambda x: x["name"], data["packages"]))
for name in names.keys():
    if name in debian_names or name.lower() in debian_names:
        names[name]["open_source"] = "true"

    names[name]["years"] = list(names[name]["years"]) # To make serializable


result_file = open("./data/Names_annotated_Debian.json" , "w")
result_file.write(json.dumps(names))
result_file.close()

