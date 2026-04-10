# Task 3 — Analysis with Pandas & NumPy
# TrendPulse: What's Actually Trending Right Now
# This script loads a cleaned dataset, performs analysis using Pandas and NumPy,
# adds new columns, and saves the results to a new CSV file.

import pandas as pd
import numpy as np

# -------------------------------
# 1. Load and Explore the Data
# -------------------------------

# Load the dataset
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)

# Print shape of the dataset
print(f"Loaded data: {df.shape}")

# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate averages using Pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score: {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# -------------------------------
# 2. Basic Analysis with NumPy
# -------------------------------

# Convert columns to NumPy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

# Calculate statistics using NumPy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

# Category with the most stories
top_category = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Story with the most comments
most_commented = df.loc[df["num_comments"].idxmax()]
print(
    f'Most commented story: "{most_commented["title"]}" '
    f'— {most_commented["num_comments"]:,} comments'
)

# -------------------------------
# 3. Add New Columns
# -------------------------------

# Engagement: comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popularity flag: True if score is above average
df["is_popular"] = df["score"] > avg_score

# -------------------------------
# 4. Save the Result
# -------------------------------

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")