import json
import math
import os
import time

import func_timeout
from func_timeout import func_set_timeout

from mistralai import Mistral

api_key = ""
client = Mistral(api_key=api_key)

@func_set_timeout(20)
def call_llm(input):
    # Prompt:
    # You will be given a list of names of software. Your task is to
    # tell me for each name of software if it is open-source. For each name,
    # reply only with "open" if it is open-source software, reply only with
    # "closed" if it is not open-source or closed-source software, reply only
    # with "unknown" if you cannot find any information of the name of
    # software. For each name, only reply "open", "closed", or "unknown".
    # Do not reply with more than one word for each name and do not
    # include any extra text in your answer."
    llm_response = client.beta.conversations.start(
        agent_id="",
        inputs=input,
    )
    try:
        return llm_response.outputs[0].content
    except:
        return " \n \n \n \n "


year = 1999
names = json.load(open("./data/Names_annotated_Debian.json", "r"))

# Update with the names of year already done.
path = "./data/Names_annotated/"
for file in os.listdir(path):
    names_year = json.load(open(path + file, 'r'))
    for name in names_year.keys():
        if names_year[name]["open_source"] != "":
            names[name] = names_year[name]


# Do unlabelled names one year at a time
names_todo = []
for name in names.keys():
    if names[name]["open_source"] == "":
        names_todo.append(name)




# Divide into batches
batch_size = 3
num_batches = math.ceil(len(names_todo) / batch_size)
batches = []
for i in range(num_batches - 1):
    batches.append((names_todo[i * batch_size:(i+1) * batch_size]))
batches.append(names_todo[(num_batches-1) * batch_size:])


# Annotate each batch by calling the llm
count = 0
result_file = open("./data/Names_annotated/names-" + year + ".json" , "w")
result_file.write("{\n")
for batch in batches:
    input = ""
    k = 1
    for name in batch:
        input = input + str(k) + ': \"' + name + '\"\n'
        k += 1
    count += 1
    print("\n" + str(count) + " / " + str(len(batches)))
    print(input)
    try:
        output = call_llm(input)
    except:
        output = " \n \n \n \n "
    print(output)
    results = output.split("\n")
    for i in range(len(batch)):
        name = batch[i]
        names[name]["open_source"] = results[i].replace(":", "").strip()
        result_file.write("\"" + name + "\": " + json.dumps(names[name]) + ",\n")
    time.sleep(2)

result_file.seek(result_file.tell() - 2, os.SEEK_SET)
result_file.write("\n}")
result_file.close()


