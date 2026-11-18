# Usage Guide

### Models
The models used for this are llama3.2:1b and gemma3:1b

### How to run
Group10_judge.py is the main script to run the tests

### Observations

The possible countries were put in a list named **prompts** and a dictionary associated with each country capital called **answers**.

The test was initially ran according to this prompt to test the models with a static answer that acted as both the given answer and the expected answer:

    >>  def test_judge_accepts_right_capital(self):
        testq = new_country()
        country = testq[0]
        city = testq[1]
        answer = f"The capital of {country} is {city}."
        print(f"Answer is: The capital of {country} is {city}.")
        self.assertTrue(llm_as_judge(country,answer,city))
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

Changing the prompt to allow the llm to give its reasoning in short answers showed: 
> llama3.2:1b : 
>> Expected Answer is: The capital of Norway is Oslo.  
  Judge response: NO. Oslo is not the capital of Norway; Oslo is the capital of Norway's capital city.

However it did seem to reason correctly with the nonsensical land
> llama3.2:1b :
>> Judge response: NO. The given answer does not agree with the expected answer, as MachineLand does not exist.


Ran 3 additional tests for each model and in 3/3 gemma did not show any faults in the answers and the reasoning was sound
>gemma3:1b:
>>test 1  
Expected Answer is: The capital of Sweden is Stockholm.  
Judge "llama3.2:1b" response: YES. It accurately reflects the expected answer.  
Judge "llama3.2:1b" response: NO.  
Reasoning: The expected answer explicitly states there’s no country, so “Capacity” isn’t the capital.
> 
>>test 2  
Expected Answer is: The capital of Norway is Oslo.  
Judge "llama3.2:1b" response: YES. It accurately reflects the expected answer.  
Judge "llama3.2:1b" response: NO.  
Reasoning: The expected answer explicitly states there is no country, thus there is no capital.
>
>>test 3  
Expected Answer is: The capital of Norway is Oslo.  
Judge "llama3.2:1b" response: YES. The answer matches the expected answer perfectly.  
Judge "llama3.2:1b" response: NO. It disagrees with the expected answer, which states there is no capital.  

Llama however failed each of the test when it came to judging the real cities and also gave nonsensical reasoning to 
answers.
>llama3.2:1b
>>test 1  
Expected Answer is: The capital of Norway is Oslo.  
Judge "llama3.2:1b" response: NO. Oslo is the largest city, not the capital. <-- Hallucination  
Judge "llama3.2:1b" response: NO. The given answer does not agree with the expected answer. MachineLand is not a real country.  
>
>>test 2  
Expected Answer is: The capital of Sweden is Stockholm.     
Judge "llama3.2:1b" response: NO. The given answer does not agree with the expected answer.  
Judge "llama3.2:1b" response: NO. The given answer is incorrect as MachineLand is a fictional country.  
>
>>test 3  
Answer is: The capital of Sweden is Stockholm.  <--- Strict expected answer   
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

Gemma3:1b was used to judge llama3.2:1b and at this point the responses were correct.
> Judge gemma3:1b, responder: llama3.2:1b
>> Test 1:  
>>Expected Answer is: The capital of Norway is Oslo.    
>>Answer llama3.2:1b: The capital of Norway is Oslo.?  
>>Judge "gemma3:1b" response: YES. The answer accurately reflects the expected answer.
> 
>> Test 2:   
>>Expected Answer is: The capital of Sweden is Stockholm.    
>>Answer llama3.2:1b: The capital of Sweden is Stockholm.?  
>>Judge "gemma3:1b" response: YES. It accurately reflects the correct capital city.
> 
>> Test 3:   
>> Expected Answer is: The capital of United Kingdom is London.       
>>Answer llama3.2:1b: The capital of the United Kingdom is London.?  
>>Judge "gemma3:1b" response: YES. It accurately reflects the expected capital city.

Reversing the roles gave immediate faults
> Judge: llama3.2:1b, responder: gemma3:1b
>> Test 1:   
>>Expected Answer is: The capital of Sweden is Stockholm.     
>>Answer gemma3:1b : The capital of Sweden is **Stockholm**. 
>>
>>It’s a wonderful city! 😊 
>>
>>Would you like to know more about Stockholm, perhaps about its history, culture, or attractions??   
>>Judge "llama3.2:1b" response: No, the given answer does not agree with the expected answer.
> 
>> Test 2:  
>>Expected Answer is: The capital of Sweden is Stockholm.      
>>Answer gemma3:1b: The capital of Sweden is **Stockholm**. 
>>
>>It’s a wonderfully unique city! 😊?  
>>Judge "llama3.2:1b" response: NO. The expected answer "Stockholm" is incorrect, as Stockholm is a different city.
> 
>> Test 3:   
>>Expected Answer is: The capital of United Kingdom is London.     
>>Answer gemma3:1b: The capital of the United Kingdom is **London**.    
>>
>> While Westminster is the seat of government, London is the center of the country’s political, economic, and cultural life.?  
>> Judge "llama3.2:1b" response: NO. The given answer, Westminster, is incorrect.

At this point llama3.2:1b can safely be assumed to lack the capabilities to act as a judge, as even when given a strict answer that was
used as both the expected output and the input, llama3.2:1b failed every time.    
Llama3.2:1b had no problem giving correct answers in the **def test_is_right(self)** method, the problem could be with the prompt from the **llm_as_judge** method, 
that might have been too complicated for it to comprehend the task it was given. When acting as a judge it exhibited classic hallucination behaviour such as 
*Judge "llama3.2:1b" response: NO. Oslo is the largest city, not the capital. <-- Hallucination* or,
*Judge "llama3.2:1b" response: NO, it does not agree as Capacity is a city, not a country. <- Hallucination*.
and for the last question it missed London in the answer from Gemma3:1b and instead focused on the final sentence that mentioned Westminster instead


Gemma3:1b never exhibited any faults on testing, as either judge or answering questions in the **def test_is_right(self)** method