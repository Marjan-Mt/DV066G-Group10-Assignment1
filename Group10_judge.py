from LLMcalls import chat_ollama
import unittest
import random

prompts = ["Norway","Sweden","Spain","United Kingdom"]
answers = {"Norway":"Oslo",
           "Sweden":"Stockholm",
           "Spain":"Madrid",
           "United Kingdom":"London"}



def question(country,model="gemma3:1b"):
    prompt = f"What is the capital of {country}?"
    response,elapsed = chat_ollama(model, prompt, verbose=False)
    return response['message']['content']

def llm_as_judge(country,answer,expected):
    model = "llama3.2:1b"
    prompt = (f"Question: What is the capital of {country}?\n"
              f"Expected answer: {expected}\n"
              f"Given answer: {answer}\n\n"
              f"Does the given answer agree with the expected answer? reply with YES or NO."
              f"Explain your reasoning with less than 15 words"
              )
    response,elapsed = chat_ollama(model, prompt, verbose=False)
    verdict = response['message']['content']
    print(f"Judge {model}'s judgement: {verdict}")
    return verdict.strip().upper().startswith("YES")

##Random country
def new_country():
    country = random.choice(prompts)
    answer = answers[country]
    return [country,answer]
##Controlled country
def fixed_country():
    country = prompts[0]
    answer = answers[country]
    return [country,answer]


class JudgeTester(unittest.TestCase):

    def test_is_right(self):
        correct = 0
        testq = new_country()
        country = testq[0]
        city = testq[1]
        print("Running test_is_right")
        print(f"Answer is: The capital of {country} is {city}.")
        print(f"Question is: What is the capital of {country}?")
        for i in range(3):
            answer = question(country)
            if city.lower() in answer.lower():
                correct += 1
        self.assertGreaterEqual(correct, 2)
        print(f"gemma3:1b was correct: {correct} times out of 3\n")

    def test_judge_accepts_right_capital(self):
        print("Running test_judge_accepts_right_capital")
        testq = fixed_country()
        country = testq[0]
        city = testq[1]
        resp = question(country)
        answer = f"The capital of {country} is {city}."
        print(f"Exact answer is: The capital of {country} is {city}.")
        print(f"Answer from LLM {resp}")
        self.assertTrue(llm_as_judge(country,resp,city))


    def test_judge_rejects_invented_capital(self):
        answer = f"The capital of MachineLand is Capacity."
        self.assertFalse(llm_as_judge("MachineLand",answer,"There is no such country, so it has no capital."))



if __name__ == '__main__':
    unittest.main()