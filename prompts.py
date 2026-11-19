from LLMcalls import chat_ollama,add_to_csv

if __name__ == '__main__':

    prompts = ["What is the biggest planet in the solar system?",
               "List the eight planets from largest to smallest by diameter.",
               "What is Jupiter’s diameter in km?"]

    results_csv = "results.csv"

    add_to_csv(results_csv, ["model", "prompt", "response", "time"], new=True)

    for prompt in prompts:
        model = "llama3.2:1b"
        response,elapsed = chat_ollama(model,prompt)
        print(response['message']['content'])
        add_to_csv(results_csv,[model,prompt,response['message']['content'],elapsed])

    for prompt in prompts:
        model = "gemma3:1b"
        response, elapsed = chat_ollama(model, prompt)
        print(response['message']['content'])
        add_to_csv(results_csv, [model, prompt, response['message']['content'], elapsed])