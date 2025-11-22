# src/etl/entity_resolution.py
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

customers = pd.read_csv("data/silver/customers_clean.csv")

# Example: find similar names
def find_similar_names(name, names_list, threshold=90):
    matches = process.extract(name, names_list, scorer=fuzz.token_sort_ratio)
    return [match for match, score in matches if score >= threshold]

# You can iterate over dataset to merge highly similar customers
# For demo, we will skip full merge due to size; in real project use `recordlinkage` or `dedupe`

print("Entity resolution step ready (apply fuzzy matching as needed).")
