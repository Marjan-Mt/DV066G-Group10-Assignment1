import time
import csv
import ollama

def chat_ollama(model,prompt, verbose=True):
    start = time.time()
    if verbose:
        print(f"Prompting {model} : {prompt}")

    result = call_ollama_chat(model, prompt)
    end = time.time()

    elapsed = end - start
    if verbose:
        print(f"{model} elapsed time: {elapsed:.2f} seconds")

    return [result,elapsed]


def call_ollama_chat(current_model,prompt):
    return ollama.chat(model=current_model,messages = [{'role':'user','content' : prompt }])

def add_to_csv(filename,row,new=False):
    mode = 'w' if new else 'a+'
    with (open(filename,mode,newline='') as file):
        writer = csv.writer(file,delimiter=';')
        writer.writerow(row)