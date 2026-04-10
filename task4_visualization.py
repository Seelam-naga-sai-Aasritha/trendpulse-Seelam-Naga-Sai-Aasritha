import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1. Setup
# ----------------------------

# Load data
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# ----------------------------
# 2. Chart 1: Top 10 Stories by Score
# ----------------------------

# Get top 10 by score
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles > 50 chars
top10["short_title"] = top10["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()

plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# ----------------------------
# 3. Chart 2: Stories per Category
# ----------------------------

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()

# ----------------------------
# 4. Chart 3: Score vs Comments
# ----------------------------

plt.figure()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

# ----------------------------
# 5. Bonus: Dashboard
# ----------------------------

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axs[0].barh(top10["short_title"], top10["score"])
axs[0].set_title("Top Stories")
axs[0].invert_yaxis()

# Chart 2 in dashboard
axs[1].bar(category_counts.index, category_counts.values)
axs[1].set_title("Categories")

# Chart 3 in dashboard
axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")
axs[2].legend()