import pandas as pd
import json
import tiktoken

df = pd.read_csv("/Users/travisjpeck/Desktop/dataset.csv")
enc = tiktoken.encoding_for_model("gpt-4o")
MAX_TOKENS = 128000

def num_tokens_from_messages(messages, encoding):
    return sum(len(encoding.encode(msg["content"])) for msg in messages)

with open("train_chat_truncated.jsonl", "w") as f, open("skipped_examples.jsonl", "w") as skipped:
    for _, row in df.iterrows():
        messages = [
            {"role": "system", "content": "You are a compassionate and thoughtful therapist. Respond to the user with empathy, clarity, and emotional intelligence."},
            {"role": "user", "content": str(row["Context"])},
            {"role": "assistant", "content": str(row["Response"])}
        ]

        token_count = num_tokens_from_messages(messages, enc)

        if token_count <= MAX_TOKENS:
            json.dump({"messages": messages}, f)
            f.write("\n")
        else:
            json.dump({"messages": messages}, skipped)
            skipped.write("\n")


