import pandas as pd
import re


def clean_text(text):

    # Convert to string in case of missing/non-text values
    text = str(text)

    # Convert text to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove spaces at beginning/end
    text = text.strip()

    return text


def preprocess_dataset(
    input_file="data/prompts_300.csv",
    output_file="data/prompts_300_clean.csv"
):

    # Load dataset
    df = pd.read_csv(input_file)

    print("Original rows:", len(df))

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    # Remove rows with missing prompt text
    df = df.dropna(subset=["prompt_text"])

    # Clean prompt text
    df["clean_prompt"] = df["prompt_text"].apply(clean_text)

    # Remove rows that become empty after cleaning
    df = df[df["clean_prompt"] != ""]

    # Standardize labels
    df["category"] = df["category"].str.upper().str.strip()

    df["risk_level"] = df["risk_level"].str.upper().str.strip()

    df["expected_decision"] = (
        df["expected_decision"]
        .str.upper()
        .str.strip()
    )

    # Save cleaned dataset
    df.to_csv(
        output_file,
        index=False
    )

    print("Cleaned rows:", len(df))
    print("Saved to:", output_file)

    return df


if __name__ == "__main__":

    preprocess_dataset()