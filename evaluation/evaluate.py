import pandas as pd

from src.rule_classifier import classify_prompt


df = pd.read_csv("data/prompts.csv")


correct = 0
incorrect = 0


for index, row in df.iterrows():

    prompt = row["prompt_text"]

    expected_decision = row["expected_decision"]

    result = classify_prompt(prompt)

    predicted_decision = result["decision"]


    print("-----------------------------------")
    print("Prompt:", prompt)
    print("Expected:", expected_decision)
    print("Predicted:", predicted_decision)


    if predicted_decision == expected_decision:

        print("Result: CORRECT")
        correct += 1

    else:

        print("Result: INCORRECT")
        incorrect += 1


print("\n==============================")
print("FINAL RESULTS")
print("==============================")

print("Correct predictions:", correct)
print("Incorrect predictions:", incorrect)
total = len(df)

accuracy = correct / total


print("\n==============================")
print("FINAL RESULTS")
print("==============================")

print("Total prompts:", total)
print("Correct predictions:", correct)
print("Incorrect predictions:", incorrect)
print("Accuracy:", round(accuracy * 100, 2), "%")