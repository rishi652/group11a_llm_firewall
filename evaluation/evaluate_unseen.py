import pandas as pd

from src.rule_classifier import classify_prompt


df = pd.read_csv("evaluation/test_cases.csv")

correct = 0
incorrect = 0


for index, row in df.iterrows():

    prompt = row["prompt_text"]
    expected_decision = row["expected_decision"]
    expected_category = row["expected_category"]

    result = classify_prompt(prompt)

    predicted_decision = result["decision"]
    predicted_category = result["category"]

    print("-----------------------------------")
    print("Prompt:", prompt)
    print("Expected category:", expected_category)
    print("Predicted category:", predicted_category)
    print("Expected decision:", expected_decision)
    print("Predicted decision:", predicted_decision)

    if predicted_decision == expected_decision:
        print("Result: CORRECT")
        correct += 1
    else:
        print("Result: INCORRECT")
        incorrect += 1


total = len(df)
accuracy = correct / total


print("\n==============================")
print("UNSEEN TEST RESULTS")
print("==============================")

print("Total prompts:", total)
print("Correct predictions:", correct)
print("Incorrect predictions:", incorrect)
print("Accuracy:", round(accuracy * 100, 2), "%")