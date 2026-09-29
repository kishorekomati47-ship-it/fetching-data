import pandas as pd
import numpy as np
df = pd.read_csv("data/trends_clean.csv")

print("Loaded data:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
highest_score = np.max(scores)
lowest_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {highest_score}")
print(f"Min score    : {lowest_score}")
category_counts = df["category"].value_counts()
most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print(f"\nMost stories in: {most_category} ({most_category_count} stories)")
most_commented_index = np.argmax(comments)
most_commented_story = df.iloc[most_commented_index]

print(
    f'Most commented story: "{most_commented_story["title"]}" '
    f'— {most_commented_story["num_comments"]} comments'
)
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > average_score
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
