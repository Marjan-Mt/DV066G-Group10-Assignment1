# Assignment 2 – Test logs and prompt experiments

These are the notes from developing the tests in `Group10_judge.py`. The summary and reflections are in [README.md](README.md#assignment-2-testing-ask_capital).

The possible countries were put in a list named `prompts` and a dictionary associated with each country capital called `answers`.

The test was initially run according to this prompt to test the models with a static answer that acted as both the given answer and the expected answer:

```python
def test_judge_accepts_right_capital(self):
    testq = new_country()
    country = testq[0]
    city = testq[1]
    answer = f"The capital of {country} is {city}."
    print(f"Answer is: The capital of {country} is {city}.")
    self.assertTrue(llm_as_judge(country, answer, city))
```

```python
prompt = (f"Question: What is the capital of {country}?\n"
          f"Expected answer: {expected}\n"
          f"Given answer: {answer}\n\n"
          f"Does the given answer agree with the expected answer? "
          f"Extra details are fine as long as they do not contradict it. Reply with only YES or NO.")
```

This worked for gemma3:1b, but when testing llama3.2:1b it would only answer with NO. Occasionally llama3.2:1b would also answer YES to the question about the made-up country (observed once). This gave reason to try a new prompt that allows a longer answer:

```python
prompt = (f"Question: What is the capital of {country}?\n"
          f"Expected answer: {expected}\n"
          f"Given answer: {answer}\n\n"
          f"Does the given answer agree with the expected answer? reply with YES or NO."
          f"Explain your reasoning with less than 15 words")
```

Changing the prompt to allow the LLM to give its reasoning in short answers showed:

> llama3.2:1b:
>
> Expected answer is: The capital of Norway is Oslo.
>
> Judge response: NO. Oslo is not the capital of Norway; Oslo is the capital of Norway's capital city.

However, it did seem to reason correctly about the nonsensical country:

> llama3.2:1b:
>
> Judge response: NO. The given answer does not agree with the expected answer, as MachineLand does not exist.

We ran 3 additional tests for each model as judge. With gemma3:1b as judge, the verdicts and reasoning were correct in 3/3 tests:

> **Test 1** – Expected answer: The capital of Sweden is Stockholm.
>
> Judge "gemma3:1b": YES. It accurately reflects the expected answer.
>
> Judge "gemma3:1b": NO. Reasoning: The expected answer explicitly states there's no country, so "Capacity" isn't the capital.
>
> **Test 2** – Expected answer: The capital of Norway is Oslo.
>
> Judge "gemma3:1b": YES. It accurately reflects the expected answer.
>
> Judge "gemma3:1b": NO. Reasoning: The expected answer explicitly states there is no country, thus there is no capital.
>
> **Test 3** – Expected answer: The capital of Norway is Oslo.
>
> Judge "gemma3:1b": YES. The answer matches the expected answer perfectly.
>
> Judge "gemma3:1b": NO. It disagrees with the expected answer, which states there is no capital.

llama3.2:1b as judge, however, failed every test with the real cities and gave nonsensical reasoning:

> **Test 1** – Expected answer: The capital of Norway is Oslo.
>
> Judge "llama3.2:1b": NO. Oslo is the largest city, not the capital. ← hallucination
>
> Judge "llama3.2:1b": NO. The given answer does not agree with the expected answer. MachineLand is not a real country.
>
> **Test 2** – Expected answer: The capital of Sweden is Stockholm.
>
> Judge "llama3.2:1b": NO. The given answer does not agree with the expected answer.
>
> Judge "llama3.2:1b": NO. The given answer is incorrect as MachineLand is a fictional country.
>
> **Test 3** – Expected answer: The capital of Sweden is Stockholm.
>
> Judge "llama3.2:1b": NO
>
> Judge "llama3.2:1b": NO, it does not agree as Capacity is a city, not a country. ← hallucination

After establishing this discrepancy, the testing method was changed so that one model answers and the other judges:

```python
def test_judge_accepts_right_capital(self):
    testq = new_country()
    country = testq[0]
    city = testq[1]
    resp = question(country, "llama3.2:1b")   # LLM response
    print(f"Answer is: The capital of {country} is {city}.")
    print(f"Answer {resp}?")
    self.assertTrue(llm_as_judge(country, resp, city))   # fed as answer
```

**Judge gemma3:1b, responder llama3.2:1b** – all verdicts were correct:

> Test 1 – Expected: Oslo. llama3.2:1b: "The capital of Norway is Oslo." Judge gemma3:1b: YES. The answer accurately reflects the expected answer.
>
> Test 2 – Expected: Stockholm. llama3.2:1b: "The capital of Sweden is Stockholm." Judge gemma3:1b: YES. It accurately reflects the correct capital city.
>
> Test 3 – Expected: London. llama3.2:1b: "The capital of the United Kingdom is London." Judge gemma3:1b: YES. It accurately reflects the expected capital city.

**Judge llama3.2:1b, responder gemma3:1b** – reversing the roles gave immediate faults:

> Test 1 – Expected: Stockholm. gemma3:1b: "The capital of Sweden is **Stockholm**. It's a wonderful city! 😊 Would you like to know more about Stockholm…?" Judge llama3.2:1b: No, the given answer does not agree with the expected answer.
>
> Test 2 – Expected: Stockholm. gemma3:1b: "The capital of Sweden is **Stockholm**. It's a wonderfully unique city! 😊" Judge llama3.2:1b: NO. The expected answer "Stockholm" is incorrect, as Stockholm is a different city.
>
> Test 3 – Expected: London. gemma3:1b: "The capital of the United Kingdom is **London**. While Westminster is the seat of government, London is the center of the country's political, economic, and cultural life." Judge llama3.2:1b: NO. The given answer, Westminster, is incorrect.

At this point llama3.2:1b can safely be assumed to lack the capabilities to act as a judge: even when given a strict answer that was used as both the expected output and the input, it failed every time. Llama3.2:1b had no problem giving correct answers when it was the responder (judged by gemma3:1b). The problem could be the `llm_as_judge` prompt, which might be too complicated for such a small model. As a judge it showed classic hallucination behaviour, such as "Oslo is the largest city, not the capital" and "Capacity is a city, not a country", and in the last test it missed London in gemma3:1b's answer and focused on the final sentence that mentioned Westminster instead.
