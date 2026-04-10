import pandas as pd
import os

# -------- 1. LOAD JSON FILE --------
file_path = "data/trends_20240115.json"   # change date if needed

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# -------- 2. CLEAN THE DATA --------

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Drop rows with missing values in important columns
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace from title
df["title"] = df["title"].str.strip()

# -------- 3. SAVE AS CSV --------

output_path = "data/trends_clean.csv"

# Create folder if not exists
os.makedirs("data", exist_ok=True)

df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")

# -------- SUMMARY --------

print("\nStories per category:")
print(df["category"].value_counts())