from json import load
from pathlib import Path
from angel import tag
from csv import DictWriter
import re

MORPH = load(open('morphology_tagset.json', 'r'))
MORPH_TAGS = MORPH["tags"]
MORPH_VALUES = MORPH["keys"]


def parse_morph(morph_code):
    result = {}
    for index, value in enumerate(morph_code):
        if value == "-":
            continue
        result[MORPH_TAGS[index]] = MORPH_VALUES[index][value]
    return result


files = Path('../texts').rglob('*.txt')
for file in files:
    print("\nReading file:", file)

    content = []
    with open(file) as fp:
        content = fp.readlines()

    text_only = ""
    cumulative_length = 0
    ref_by_char_pos = []
    for line in content:
        # Sometimes the chapter is "EP" (epilogue) or "SB" (?)
        # Also note that Shepherd has three levels: i.e., "1.2.3"
        split = line.split(None, 1)
        ref = split[0]
        greek_string = split[1]
        text_only += greek_string + " "
        # Based on the assumption that the only loss in tokenization is spaces
        cumulative_length += len(greek_string.replace(" ", ""))
        ref_by_char_pos.append((
            cumulative_length,
            ref
        ))
    print("> Length of Text:", len(text_only))
    print(">", text_only[:100], "...")

    tagged_token_array = tag(text_only)

    token_length = 0
    output_rows = []
    cumulative_length = 0
    for t in tagged_token_array:
        cumulative_length += token_length
        token = t[0]
        token_length = len(token)
        morph_code = t[1]

        # Handle punctuation as trailer on previous word
        if morph_code == "u--------" and len(output_rows) > 0:
            output_rows[-1]["trailer"] = token + " "
            continue

        # Get reference based on the cumulative length of the tokens processed thus far
        ref = [x for x in ref_by_char_pos if x[0] > cumulative_length][0][1]

        row_data = {}

        # Only parse non-Latin words
        # Note, polycarp-phil has "ë" in 10.2
        #       shepherd has a ":" in 26.31.5, 26.32.4...
        if re.match('^[a-zA-Zë:]+$', token) is None:
            row_data = parse_morph(morph_code)

        row_data["token"] = token
        row_data["trailer"] = " "
        row_data["reference"] = ref

        # ":" is not tokenized separately
        # (This only occurs in Latin sections of Shepherd)
        if token.endswith(":"):
            row_data["token"] = token[:-1]
            row_data["trailer"] = ": "

        output_rows.append(row_data)

    # Remove trailing space
    output_rows[-1]["trailer"].strip()

    out_file = str(file).replace("texts", "tagged-texts").replace("txt", "csv")
    keys = ["reference", "token", "trailer", *MORPH_TAGS]
    print("Writing file", out_file, "\n")
    with open(out_file, 'w', newline='') as fp:
        dict_writer = DictWriter(fp, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_rows)
