import pandas as pd
from sklearn.model_selection import train_test_split


# Load cleaned unique dataset
df = pd.read_csv("data/prompts_300_v2_clean.csv")


# Create 80% development set and 20% holdout test set
development_df, holdout_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["category"]
)


# Save both files
development_df.to_csv(
    "data/development_240.csv",
    index=False
)

holdout_df.to_csv(
    "data/holdout_60.csv",
    index=False
)


print("Development rows:", len(development_df))
print("Holdout rows:", len(holdout_df))

print("\nDevelopment category counts:")
print(development_df["category"].value_counts())

print("\nHoldout category counts:")
print(holdout_df["category"].value_counts())