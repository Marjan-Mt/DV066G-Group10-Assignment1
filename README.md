# Usage Guide

### Models
The models used for this are llama3.2:1b and gemma3:1b

### How to run
Group10_judge.py is the main script to run the tests

### Observations

#### Karim:

The test was initially ran according to this prompt to test the models with a static answer:

    >>  def test_judge_accepts_right_capital(self):
        testq = new_country()
        country = testq[0]
        city = testq[1]
        answer = f"The capital of {country} is {city}."
        print(f"Answer is: The capital of {country} is {city}.")
        self.assertTrue(llm_as_judge(country,resp,city))
>

    >> prompt = (f"Question: What is the capital of {country}?\n"
              f"Expected answer: {expected}\n"
              f"Given answer: {answer}\n\n"
              f"Does the given answer agree with the expected answer? "
              f"Extra details are fine as long as they do not contradict it. Reply with only YES or NO."
              )


Which worked for gemma 3:1b, but when testing llama3.2:1b it would only answer with NO, Occasionally llama3.2:1b would also answer with
Yes to the question of the made up country this was observed once, which gave reason to have a new prompt to allow for a longer answer:

    >> prompt = (f"Question: What is the capital of {country}?\n"
              f"Expected answer: {expected}\n"
              f"Given answer: {answer}\n\n"
              f"Does the given answer agree with the expected answer? reply with YES or NO."
              f"Explain your reasoning with less than 15 words"
              )

Changing the prompt to allow the llm to give its reasoning in short answers results showed: 
> llama3.2:1b : 
>> Answer is: The capital of Norway is Oslo.  
  Judge response: NO. Oslo is not the capital of Norway; Oslo is the capital of Norway's capital city.

However it did seem to reason correctly with the nonsensical land
> llama3.2:1b :
>> Judge response: NO. The given answer does not agree with the expected answer, as MachineLand does not exist.


Karim ran 3 additional tests for each model and in 3/3 gemma did not show any faults in the answers and the reasoning was sound
>gemma3:1b:
>>test 1  
Answer is: The capital of Sweden is Stockholm.  
Judge response: YES. It accurately reflects the expected answer.  
Judge response: NO.  
Reasoning: The expected answer explicitly states there’s no country, so “Capacity” isn’t the capital.
> 
>>test 2  
Answer is: The capital of Norway is Oslo.  
Judge response: YES. It accurately reflects the expected answer.  
Judge response: NO.  
Reasoning: The expected answer explicitly states there is no country, thus there is no capital.
>
>>test 3  
Answer is: The capital of Norway is Oslo.  
Judge response: YES. The answer matches the expected answer perfectly.  
Judge response: NO. It disagrees with the expected answer, which states there is no capital.  

Llama however failed each of the test when it came to judging the real cities and also gave nonsensical reasoning to 
answers.
>llama3.2:1b
>>test 1  
Answer is: The capital of Norway is Oslo.  
Judge response: NO. Oslo is the largest city, not the capital. <-- Hallucination  
Judge response: NO. The given answer does not agree with the expected answer. MachineLand is not a real country.  
>
>>test 2  
Answer is: The capital of Sweden is Stockholm.  
Judge response: NO. The given answer does not agree with the expected answer.  
Judge response: NO. The given answer is incorrect as MachineLand is a fictional country.  
>
>>test 3  
Answer is: The capital of Sweden is Stockholm.  
Judge response: NO  
Judge response: NO, it does not agree as Capacity is a city, not a country. <- Hallucination

After establishing this discrepancy testing method was change into

    >>  def test_judge_accepts_right_capital(self):
        testq = new_country()
        country = testq[0]
        city = testq[1]
        resp = question(country,"llama3.2:1b") <-- LLM response
        answer = f"The capital of {country} is {city}."
        print(f"Answer is: The capital of {country} is {city}.")
        print(f"Answer {resp}?")
        self.assertTrue(llm_as_judge(country,resp,city)) <-- Fed as answer

Gemma3:1b was used to judge llama3.2:1b and at this point the responses were correct, answers ending with ? are llm responses.
> Judge gemma3:1b, responder: llama3.2:1b
>> Test 1:  
>> Answer is: The capital of Norway is Oslo.   
>>Answer The capital of Norway is Oslo.?  
>>Judge response: YES. The answer accurately reflects the expected answer.
> 
>> Test 2:   
>> Answer is: The capital of Sweden is Stockholm.  
Answer The capital of Sweden is Stockholm.?  
Judge response: YES. It accurately reflects the correct capital city.
> 
>> Test 3:   
>> Answer is: The capital of United Kingdom is London.   
Answer The capital of the United Kingdom is London.?  
Judge response: YES. It accurately reflects the expected capital city.

Reversing the roles gave immediate faults
> Judge: llama3.2:1b, responder: gemma3:1b
>> Test 1:   
>> Answer is: The capital of Sweden is Stockholm.  
>>Answer The capital of Sweden is **Stockholm**. 
>>
>>It’s a wonderful city! 😊 
>>
>>Would you like to know more about Stockholm, perhaps about its history, culture, or attractions??   
>>Judge response: No, the given answer does not agree with the expected answer.
> 
>> Test 2:  
>> Answer is: The capital of Sweden is Stockholm.   
>>Answer The capital of Sweden is **Stockholm**. 
>>
>>It’s a wonderfully unique city! 😊?  
>>Judge response: NO. The expected answer "Stockholm" is incorrect, as Stockholm is a different city.
> 
>> Test 3:   
>>Answer is: The capital of United Kingdom is London.  
Answer The capital of the United Kingdom is **London**.    
>>
>> While Westminster is the seat of government, London is the center of the country’s political, economic, and cultural life.?  
>> Judge response: NO. The given answer, Westminster, is incorrect.

For this part it is reasonable to see these results, as gemma gave longer answers than needed and also added extra trivia which llama
got hung-up on in addition to using markup language to "exclaim" the capital probably confusing llama.