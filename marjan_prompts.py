import csv
import time
import ollama

models = ["llama3.2:latest", "qwen2.5:1.5b"]

question = (
    "A file was deleted from a shared project. "
    "Jon logged in at 10:00. "
    "Mark edited a different file at 10:05. "
    "Sara noticed the deletion at 10:10. "
    "All three had permission to delete files. "
    "Who deleted the file? Use only the evidence provided. "
    "Can you reach a definite conclusion?"
)

reference = (
    "\n\nReference answer: There is not enough evidence to know "
    "who deleted the file. None of these actions proves who did it. "
    "Do you agree? Explain why or why not."
)

prompts = [question, question + reference]

with open("marjan_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["model", "prompt", "answer", "seconds"])

    for model in models:
        for prompt in prompts:
            start = time.perf_counter()

            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                keep_alive=0,
            )

            seconds = round(time.perf_counter() - start, 2)
            answer = response["message"]["content"]

            writer.writerow([model, prompt, answer, seconds])

            print(f"\nModel: {model}")
            print(f"Prompt: {prompt}")
            print(f"Answer: {answer}")
            print(f"Time: {seconds} seconds")

print("\nSaved to marjan_results.csv")