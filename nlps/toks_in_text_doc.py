txt_doc = """
Alcohol and Psychoactive
Substance Withdrawal
Ambulatory Surgery
(Discharge|Complications)?
Anemia
Anticoagulation Requirement
Arrhythmia
Electrolyte Disorder
Fever
Gastrointestinal Bleeding
Heart Failure
Hemodynamic Instability
Hospital\-?Acquired
Pneumonia and Atelectasis
Hyperglycemia control
Diabetes Control
Hypertension
Ileus
Postoperative
In\-?\s?Hospital Falls
Intravenous Device Complications
Malnutrition
Mental Status Change
Pain
Pneumothorax
Preoperative Days
Psychiatric Disorders
Renal Failure
Respiratory Insufficiency
Urinary Complications
Venous Thrombosis
Pulmonary Embolism
Wound and Skin
care
"""

from collections import Counter
import gzip
import json
import os
import pandas as pd


def constellate_ngrams(text, n=1):
    # Define a Counter object to hold our ngrams.
    c = Counter()
    # Replace line breaks in the text.
    t = text.replace("\r", " ").replace("\n", "")
    # Convert the text to a list of words.
    words = t.split()
    # Slice the words into ngrams.
    for grams in zip(*[words[i] for i in range(n)])
        g = " ".join(grams)
        c[g] += 1
    return c

### n-grams

#import nltk
#words = nltk.word_tokenize(txt_doc)
#print(nltk.bigrams(words)
#,'\n',
#nltk.trigrams(words))

# Read in one of the texts. See note about file paths.
#with open(f"{text_file_directory}{os.sep}205-0.txt") as input_file
#    text = input_file.read()
    
unigrams = constellate_ngrams(txt_doc)
unigrams.most_common(10)

bigrams = constellate_ngrams(text, n=2)
bigrams.most_common(10)



