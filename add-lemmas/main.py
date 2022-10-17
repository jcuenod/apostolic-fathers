import csv
import os
import json
import re

lemmas = []
with open("./lemmas.json") as f:
    lemmas = json.load(f)

disambiguations = {}
with open("./disambiguations.json") as f:
    disambiguations = json.load(f)

def l(word):
    if word in disambiguations:
        return disambiguations[word]
    if word not in lemmas:
        print("Word not found:", word)
        return ""
    return lemmas[word][0]["hdwd"] if len(lemmas[word]) == 1 else ""

def get_lemma(word):
    lemmas = [l(w) for w in word["token"]]
    return lemmas

# pattern = re.compile('[,·;.?»«“„)]')
pattern = re.compile('(\W*)(\w+’?)(\W*)')
def leader_word_trailer(word):
    match = re.search(pattern, word)
    return [match.group(1),match.group(2),match.group(3)] if match is not None else ["", word, ""]

def row_from_token(chv, word):
    leader, token, trailer = leader_word_trailer(word)
    # token = word[0:i] if i > 0 else word
    # trailer = word[i:] if i > 0 else ""
    lemma = l(token)
    return [chv, leader, token, trailer, lemma]

blank_lemma_tally = 0
files = os.listdir("../texts/")
for file in files:
    print(file)
    rows = [["reference", "leader", "word", "trailer", "lemma"]]
    with open("../texts/" + file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            spl = line.rstrip().split(" ")
            chv = spl[0]
            content = spl[1:]
            rows.extend([row_from_token(chv, word) for word in content])
    
    with open("../lemma-texts/" + file.replace("txt", "csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    no_lemma_count = len([r for r in rows if r[4] == ""])
    blank_lemma_tally += no_lemma_count
    print(" - blank lemmas:", no_lemma_count)

print("Total missing lemmas:", blank_lemma_tally)
