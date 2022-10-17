import requests
import json
import pandas as pd
import os

tokens = set([])
files = os.listdir("../tagged-texts/")
for file in files:
    df = pd.read_csv("../tagged-texts/" + file, index_col=0)
    tokens = tokens.union(set(df["token"].values))


lemmas = {}
with open("./lemmas.json", "r") as f:
   lemmas = json.load(f) 

def write():
    with open('lemmas.json', 'w') as file:
        file.write(json.dumps(lemmas))

print("Tokens:", len(tokens))
print("Loaded:", len(list(lemmas.keys())))
print("Fetching morphs:")
i = 0
for token in tokens:
    if token in lemmas:
        continue
    morph_req = requests.get('https://scaife.perseus.org/morpheus/?lang=grc&word=' + token)
    morph = json.loads(morph_req.text)
    lemmas[token] = morph["Body"]
    i += 1
    if i % 10 == 0:
        write()
        print(" - ",i)


write()
