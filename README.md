# DV066G – Group 10 – Assignment 1

## Purpose

We ran the same prompts through small open models locally with Ollama and the ollama Python library, saved the answers to CSV and compared speed, correctness and hallucinations.

## Prompts:

1. What is the biggest planet in the solar system?
2. List the eight planets from largest to smallest by diameter.
3. What is Jupiter’s diameter in km?

## Models

### Karim

- llama3.2:1b
- gemma3:1b

The test were run on a MSI thin with 16 GB RAM

### Marjan

- `llama3.2:latest`
- `qwen2.5:1.5b`

The tests were run on a MacBook Air M1 with 8 GB RAM.

### Yasaman

- llama3.2:1b
- gemma3:1b

The tests were run on a HP ZBook Fury with 32 GB RAM.

## How to run

### Karim

These instructions are for windows, Install ollama from [https://docs.ollama.com/quickstart#local](https://docs.ollama.com/quickstart#local) .

In cmd get the models by typing in ollama pull model, ex ollama pull llama3.2:1b

```bash
py install ollama
```

and then call to the script using py prompts.py

### Marjan

These instructions are for macOS.

```bash
ollama pull llama3.2:latest
ollama pull qwen2.5:1.5b
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ollama
```

Keep `prompts.py` and `LLMcalls.py` together. In `prompts.py`, use the models above and set:

```python
results_csv = "marjan_planets_results.csv"
```

```bash
python prompts.py
```

### Yasaman

These instructions are for Windows with WSL2 (Ubuntu 24.04). Ollama 0.40.14.

```bash
sudo apt-get install -y zstd python3-venv
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
ollama pull gemma3:1b
python3 -m venv ~/.venvs/dv066g && source ~/.venvs/dv066g/bin/activate
pip install ollama
python prompts.py
```

Output: `results_yasaman.csv` (run 1) and `results_yasaman_run2.csv` (run 2, same prompts about 3 minutes later).

## Results and observations

### Marjan

#### Llama 3.2

Llama correctly answered that Jupiter is the biggest planet. However, it said Jupiter has about 1,475 times Earth's mass. The correct value is about 318 times Earth's mass.

It listed the planets in the correct order:

Jupiter, Saturn, Uranus, Neptune, Earth, Venus, Mars, Mercury.

For Jupiter's diameter, it gave 142,984 km. This is the equatorial diameter, although the answer did not explain which diameter it used.

#### Qwen 2.5

Qwen also correctly named Jupiter as the biggest planet. It gave a diameter of 139,822 km, which is the mean diameter. However, its extra statement about a sphere with a diameter of 39 km did not make sense as an explanation of Jupiter's size.

Its planet order was incorrect. It placed Venus after Mars and Mercury and called Venus the smallest planet. Venus should be between Earth and Mars. Mercury is the smallest.

For the final question, Qwen gave Jupiter's equatorial diameter of 142,984 km. The different diameter values are not necessarily a contradiction, but the model should explain whether it means the average or equatorial diameter.

### Yasaman

I ran the same three prompts twice with both models to see if the answers change between runs.

#### Llama 3.2 (1b)

Llama answered all three questions correctly in both runs and listed the planets in the correct order. The mistakes were in details nobody asked for. In run 1 it said Jupiter is "more than 1,300 times the size of Earth", which is right for volume. In run 2 the same sentence became "1,300 times the diameter of the Earth", which is wrong (about 11 times). It also converted Jupiter's diameter to 87,975 miles in one answer and 88,846 miles in the next (the correct value is 88,846).

#### Gemma 3 (1b)

Gemma also answered the main questions correctly and listed the planets in the correct order, but it hallucinated more in the extra details:

- Run 1: "Jupiter has a mass approximately 318 times that of all the other planets combined". 318 is Jupiter's mass compared to Earth, not to all other planets (about 2.5 times).
- Run 1: "roughly the size of several thousand Earths". About 1,300 Earths fit inside Jupiter.
- Run 2: "Jupiter holds roughly 95% of the total mass of the solar system". The Sun holds about 99.8%.
- Run 2: 142,984 km = "91,000 miles". The correct conversion is 88,846 miles.
- It made up today's date: "October 26, 2023" in run 1 and "November 2, 2023" in run 2. The model has no clock and guesses a date from its training data.

Both models mixed equatorial and mean diameters in the same list without saying so.

#### Non-determinism

Same prompt, same model, same machine, a few minutes apart, but the details changed. Some errors disappeared and new ones appeared. One run is not enough to judge a model.

### Karim

Both of my models gave correct answers, however gemma always added onto each of the measurement queries that these measurements are approximations and can be reported differently from different sources, whilst llama only did so for 1 out of 4 queries. For these queries I would say they were about the same as what I would expect from ChatGPT.

## Timing and limitations

### Karim

The longest time it took for any query was 3.7 s and the quickest was 0.16 s.

### Marjan

Llama took 7.32 seconds to answer the biggest-planet question, 7.20 seconds to list the planets by diameter, and 0.96 seconds to give Jupiter’s diameter.

Qwen took 3.58, 2.08 and 0.40 seconds for the same questions. Qwen was faster for all three questions in this run.

### Yasaman

Gemma's first request took 52 seconds, most likely because the model had to be loaded into memory (cold start). I ran it right after downloading the model. In run 2 the same question took under 7 seconds. The answer length was similar in both runs so the difference is not explained by length. Gemma also wrote much longer answers than Llama, which takes more time.

## Learning

**LLMs predict tokens, they do not look facts up.**

LLMs are pre-trained by hiding a word and predicting it and GPTs predict the next word. Text is split into numbers. This explains why the models got well-known facts right (Jupiter is the biggest planet) but attached real numbers to the wrong quantity: Llama said "1,475 × Earth's mass" (Marjan's run), and Gemma said "318 × all other planets" (Yasaman's run). It also explains why unit conversions to miles gave different results.

**Hallucinations sound right.**

"Hallucinations can sound right even when they are fundamentally wrong or unverifiable". None of the wrong answers sounded uncertain. We could only find the errors because our prompts had answers we could check against NASA's fact sheet.

**The same prompt gives different answers.**

The model samples each next token and temperature controls how random the choice is. Karim found no errors with llama3.2:1b and gemma3:1b, while Yasaman found several with the same models and prompts. Yasaman's two runs also differed from each other. "Test outputs over many runs": one run is not enough to judge a model.

**Small models can make factual mistakes.**

Qwen 2.5 (1.5B) got the planet order wrong (Marjan's run). Every model got the main question right but errors appeared in harder or extra details.

**We cannot tell where an answer comes from.**

The models do not look up sources when they answer. They generate text from patterns learned from their training data and we do not know exactly what that data contained. This may explain why the models mixed mean and equatorial diameters without saying which one they used. Gemma listed links to NASA and Space.com, it generated them as text and did not read them. As the course slides put it, "some AI models are difficult to understand, making their decisions hard to explain". To trust an answer, we had to check it against a source ourselves.

**Speed depends on more than the model.**

The first request includes loading the model into memory. Longer answers take longer and we used different hardware so times are not directly comparable between members.

**Why this matters for AI engineering.**

If an LLM is used as a software component its output must be tested over many runs and checked against a trusted source because it can be fluent, confident and wrong.

## Sources used to check the answers

NASA Planetary Fact Sheet

W45. Intro to the course and to AI, Beatriz Cabrero-Daniel | 26-11-02