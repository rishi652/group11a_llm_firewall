import pandas as pd
import re


def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_dataset(
    input_file="data/prompts_300_v2.csv",
    output_file="data/prompts_300_v2_clean.csv"
):
    df = pd.read_csv(input_file)

    print("Original rows:", len(df))

    # Remove duplicate prompt text
    df = df.drop_duplicates(subset=["prompt_text"])

    # Remove rows where prompt text is missing
    df = df.dropna(subset=["prompt_text"])

    # Create cleaned version of prompt
    df["clean_prompt"] = df["prompt_text"].apply(clean_text)

    # Remove empty prompts
    df = df[df["clean_prompt"] != ""]

    # Normalize labels
    df["category"] = df["category"].str.upper().str.strip()
    df["risk_level"] = df["risk_level"].str.upper().str.strip()
    df["expected_decision"] = (
        df["expected_decision"]
        .str.upper()
        .str.strip()
    )

    # Save
    df.to_csv(
        output_file,
        index=False
    )

    print("Cleaned rows:", len(df))
    print(
        "Unique prompts:",
        df["prompt_text"].nunique()
    )
    print(
        "Duplicate prompts:",
        df.duplicated(
            subset=["prompt_text"]
        ).sum()
    )

    print("Saved to:", output_file)

    return df


if __name__ == "__main__":
    preprocess_dataset()