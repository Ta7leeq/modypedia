import pandas as pd
import re
import os
from interface.models import Item, Branch

# 1. Get items from the specific branch
branch = Branch.objects.get(branch_name="Kapital_01")
items = Item.objects.filter(branch=branch)


# 2. Define Excel column headers
columns = [
    "sentence", "level", "word", "plural", "category", "translation",
    "f_feature1", "f_feature2", "synonyms", "fill_the_gap1",
    "multiple_choice1", "multiple_choice2", "multiple_choice3", "multiple_choice4"
]

# 3. Function to split text into sentences (keeping punctuation)
def split_sentences(text):
    # This will split at . ? ! followed by space or end of string
    return re.findall(r'[^.!?]+[.!?]?', text)

# 4. Prepare data
data = []

for item in items:
    full_text = item.content if item.content else ""
    tags = item.tags.split("-") if item.tags else []
    tags = [tag.strip() for tag in tags if tag.strip()]

    # Split into individual sentences
    sentences = split_sentences(full_text)

    for raw_sentence in sentences:
        sentence = raw_sentence.strip()
        if not sentence:
            continue

        matched_tags = []

        for tag in tags:
            tag_pattern = rf'\b{re.escape(tag)}\b'
            if re.search(tag_pattern, sentence, flags=re.IGNORECASE):
                matched_tags.append(tag)

                # Add space before tag if preceded by non-letter
                sentence = re.sub(rf'(?<![A-Za-z])({re.escape(tag)})(?!\s)', r' \1', sentence)

                # Add space after tag if followed by non-letter
                sentence = re.sub(rf'({re.escape(tag)})(?=[^\sA-Za-z])', r'\1 ', sentence)

        fill_the_gap = ",".join(matched_tags)

        row = [sentence.strip()] + ["empty"] * 8 + [fill_the_gap] + ["empty"] * 4
        data.append(row)

# 5. Save to Excel
df = pd.DataFrame(data, columns=columns)
output_path = "Kapital_01_split_sentences.xlsx"
df.to_excel(output_path, index=False)

print("✅ File saved at:", os.path.abspath(output_path))
