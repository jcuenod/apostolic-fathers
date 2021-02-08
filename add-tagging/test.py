from pathlib import Path
import re


def isolate_greek_punctuation(fsentence):
    """Place spaces around punctuation so it can be easily split into its own token later."""
    return fsentence.replace(',', ' , ').replace('·', ' · ').replace(';', ' ; ').replace('.', ' . ').\
        replace('?', ' ? ').replace('»', ' » ').replace('«', ' « ').replace('“', ' “ ').replace('„', ' „ ').\
        replace('(', ' ( ').replace(')', ' ) ').replace('>', ' > ').replace('<', ' < ').replace(':', ' : ').\
        replace('‘', ' ‘ ')


files = Path('../texts').rglob('*.txt')
for file in files:
    print("\nReading file:", file)

    content = []
    with open(file) as fp:
        content = fp.readlines()

    for line in content:
        punc_separated_text = isolate_greek_punctuation(line)
        split_text = punc_separated_text.split()
        for token in split_text:
            if re.match('^[a-zA-Z]+$', token) is not None:
                print(token)
