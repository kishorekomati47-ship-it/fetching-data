import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
df = pd.read_csv("data/trends_analysed.csv")
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

top_stories = df.nlargest(10, "score").copy()
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(output_folder / "chart1_top_stories.png")
plt.show()
plt.close()

category_counts = df["category"].value_counts()

colors = [
    "red",
    "blue",
    "green",
    "orange",
    "purple"
]

plt.figure(figsize=(8, 5))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=colors[:len(category_counts)]
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()
plt.savefig(output_folder / "chart2_categories.png")
plt.show()
plt.close()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(9, 6))

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()
plt.savefig(output_folder / "chart3_scatter.png")
plt.show()
plt.close()

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].invert_yaxis()
axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=colors[:len(category_counts)]
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")
axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()
axes[1, 1].axis("off")

fig.suptitle("TrendPulse Dashboard", fontsize=16)

plt.tight_layout()
plt.savefig(output_folder / "dashboard.png")
plt.show()
plt.close()

print("Charts saved successfully to the outputs folder.")
