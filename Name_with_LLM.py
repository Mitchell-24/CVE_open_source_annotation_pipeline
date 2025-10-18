
from mistralai import Mistral
import json
import os
import math

api_key = ""
client = Mistral(api_key=api_key)

def call_llm(input):
    # Prompt:
    # "You will be given a list of text fragments. Each fragment contains a
    # description of a problem with a piece of software. For each
    # description, tell me what the name of the mentioned software is. For
    # each description, reply only with one name. Each name should be
    # prepended with the number and a colon. Make sure to exclude any
    # version numbers."
    llm_response = client.beta.conversations.start(
        agent_id="",
        inputs=input,
    )
    return llm_response.outputs[0].content


# Annotate all other CVEs by retrieving the name from the description

## Do one year at a time
year = "2004"
data = open("./data/CVEs_short_debian_named.json", 'r')
cves = json.load(data)
result_file = open("./data/CVEs_named/CVEs-" + year + ".json" , "w")
result_file.write("[\n")
cves_year = []
for cve in cves:
    if cve["timestamp"].split("-")[0] == year:
        if cve["name"] == "":
            cves_year.append(cve)
        else:
            result_file.write(json.dumps(cve) + ",\n")  # All previously annotated can be saved immediately.

## Devide into batches
batch_size = 50
num_batches = math.ceil(len(cves_year) / batch_size)
batches = []
for i in range(num_batches - 1):
    batches.append((cves_year[i * batch_size:(i+1) * batch_size]))
batches.append(cves_year[(num_batches-1) * batch_size:])

## Annotate each batch by calling the llm
for batch in batches:
    input = ""
    k = 1
    for cve in batch:
        input = input + str(k) + ': \"' + cve["description"] + '\"\n'
        k += 1
    print(input)
    output = call_llm(input)
    print(output)
    names = output.split("\n")
    for i in range(len(batch)):
        cve = batch[i]
        cve["name"] = "".join(names[i].split(":")[1:]).strip()
        result_file.write(json.dumps(cve) + ",\n")

result_file.seek(result_file.tell() - 2, os.SEEK_SET)
result_file.write("\n]")
result_file.close()








