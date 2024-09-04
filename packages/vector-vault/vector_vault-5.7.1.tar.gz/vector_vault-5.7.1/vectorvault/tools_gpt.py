import ast
import queue
import threading

'''
    ToolsGPT is a set of tools special to large language models.
    Every tool turns unstructured data into structured data.

    Structure data is required to run programs.
    Unstructured data is the primary human output.
    AI tools convert unstructured data into structured data,
    bridging the gap between humans and programs.
    Therefore, in the future, everything will be programmable.

    ToolsGPT allows you to get the following for any input:
        1. `get_rating` - returns a rating out of 10 for any input
        2. `get_yes_no` - returns a 'yes' or a 'no' to any question
        3. `get_number` - returns an integer based on your instructions
        4. `get_match` - returns a match to a list options - (single choice)
        5. `get_multi_match` - returns one or many matches to a list of options - (multiple choice)
        6. `get_topic` - returns the topic subject matter of any input

        1. `get_rating`:
            Get a numeric rating out of 10 for anything

        2. `get_yes_no`:
            Get an exact 'yes' or 'no' to any question

        3. `get_number`:
            Get an integer output for any input

        4. `get_match`:
            Get an exact match to a single item within a list
            -> in: (text and list of strings)
            -> out: (one exact match to an answer in list -> string type)

        5. `get_multi_match`:
            Get many matches to items within a list
            -> in: (text and list of answers)
            -> out: (list of exact matches -> list type)

        6. `get_topic`:
            Useful to classify the topic of conversation
'''

class ToolsGPT():
    def __init__(self, verbose=False, timeout=300, ai='openai', groq_api=None):
        self.verbose = verbose
        if ai == 'openai':
            from .ai import AI
            self.llm = AI(verbose=verbose).llm
        if ai == 'groq':
            from .groq_api import GroqAPI as AI
            self.llm = AI(verbose=verbose, api=groq_api).llm
        self.timeout = timeout


    def get_rating(self, text: str = None, concept_to_rate_for: str = None, model=None, loop_limit=20, timeout=None, temperature=None) -> int:
        '''
            Get a numeric rating out of 10. Input plain text, and concept to rate for. Defualts to 'quality'
            Output is integer. Leave no text and pass concept only to format custom
        '''
        if text:
            prompt_template = """Rate the following content 1 - 10. Respond only with a number in integer format.
            Concept to rate out of ten for: {concept_to_rate_for}
            User: Content to classify out of 10: "{content}" \n\n Reponse: Since I am not allowed to give any explination before or after my rating, I'd like to say
            that this number has been carefully considered given your content. My rating out of 10 integer is: """
            prompt = prompt_template.format(concept_to_rate_for=concept_to_rate_for, content=text)
        else:
            prompt_template = """Rate the following content 1 - 10. Respond only with a number in integer format.
            Concept to rate out of ten for: {concept_to_rate_for} \n\n Reponse: Since I am not allowed to give any explination before or after my rating, I'd like to say
            that this number has been carefully considered given your concept. My rating out of 10 integer is: """
            prompt = prompt_template.format(concept_to_rate_for=concept_to_rate_for)

        answer = self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)
        if self.verbose == True:
            print(f"'Rating Initial Answer: {answer}")

        try:
            return int(answer) # try to return an int zero shot
        except:
            return self.retry_until_its_a_number(answer, model=model, loop_limit=loop_limit, timeout=timeout) # force the integer if zero shot fails


    def get_number(self, concept, content: str, model=None, loop_limit=5, timeout=None, temperature=None) -> int:
        '''
            param: `concept` - is the idea used to generate a number with - i.e. "How many students are in the professor's class?"
            param: `content` - is the content to generate a number for - i.e. "I had 400 students in my class last year, but this year, I have 10% more."
        '''
        response = self.retry_llm(f'{concept} \n\n{content}', model=model, loop_limit=loop_limit, timeout=timeout)
        print("Initial number extraction response:", response) if self.verbose else 0
        return response if type(response) is int else self.retry_until_its_a_number(response, model=model, loop_limit=loop_limit)


    def retry_until_its_a_number(self, content: str, model=None, loop_limit=5, timeout=None, temperature=None) -> int:
        '''
            param: `content` - the AI will return an integer based on the content you input
        '''

        prompt_template = """Respond only with a number in integer format...
        Example content: 'The revenue for the last fiscal year was $1,200,000.' Example answer: '1200000'
        Example content 2: 'The company has been in business for twenty years.' Example answer 2: '20'
        Example content 3: 'The recipe calls for three cups of flour.' Example answer 3: '3'
        Example content 4: 'The event will take place on the 15th of next month.' Example answer 4: '15'
        Example content 5: 'The building has a total of fourteen floors.' Example answer 5: '14'
        Example content 6: 'There are one hundred and fifty employees in the company.' Example answer 6: '150'
        Example content 7: 'The project deadline is in 45 days.' Example answer 7: '45'
        User: The following content should be a number - Content: "{content}"
        \nAgent:"""

        prompt = prompt_template.format(content=content)
        response = self.retry_llm(custom_prompt=prompt, model=model, loop_limit=loop_limit, timeout=timeout, temperature=temperature)
        print("Initial number extraction response:", response) if self.verbose else 0

        if type(response) is int:
            return response

        else: # loop until its a number
            loops = 0
            answer = content

            while True:
                if loops >= loop_limit:
                    break

                prompt = prompt_template.format(content=answer)
                answer = self.retry_llm(custom_prompt=prompt, model=model, loop_limit=loop_limit, timeout=timeout, temperature=temperature)
                print(f"Loops: {loops} |  Number: {answer}") if self.verbose else 0

                try:
                    answer = int(answer)
                    return answer # exit loop and return the integer
                except:
                    loops += 1


    def get_yes_no(self, text: str, question: str = None, model=None, loop_limit=20, timeout=None, temperature=None) -> str:
        '''
            Get an exact "yes" or "no" to any question, given an input.
            Be sure to input text to get a yes or no to, then ask the question to answer
        '''
        answer = self.yay_or_nay(text, question, model=model, timeout=timeout) if question else self.yay_or_nay_question_in_content(text, model=model, timeout=timeout, temperature=temperature)
        print(f"Y/N Initial Answer: {answer}") if self.verbose == True else 0

        loops = 0
        while loops < loop_limit and answer not in ['yes', 'no']:
            answer = self.isolate_yes_no(answer, timeout=timeout)
            print(f"Y/N Answer {loops}: {answer}") if self.verbose else 0
            loops += 1

        return answer


    def get_match(self, text: str, list_of_options: list, model=None, loop_limit=4, timeout=None, temperature=None) -> str:
        '''
        This function can be used in a variety of Natural Language Processing (NLP) tasks,
        such as text classification or intent recognition.

        Classify any text input to a single option contained in a list of options. - Returns exact match to one of items on list.
        Input text, and list of options: ["list of options", "is a list of strings", "do not forget"]
        '''

        list_copy = []
        for option in list_of_options:
            list_copy.append(str(option).strip().replace('.', '').lower().strip('"').strip("'"))
        prompt = f"""Respond with one of the options on this list: {list_copy}
        Content to classify: "{text}"  \n\nDo not respond with anything other than the option on the list."""

        answer = self.retry_llm(prompt, model, loop_limit, timeout=timeout, temperature=temperature)

        print(f'''Get Answer: {answer}''') if self.verbose else 0

        final = None
        temp = 0

        while not final:
            if answer is not None:
                try:
                    try:
                        new_answer = list_of_options[list_copy.index(answer)]  # return original answer
                        final = True
                    except:
                        temp += .2 if temp < .7 else 0
                        answer = self.retry_llm(prompt, model, loop_limit, temperature=temp, timeout=timeout)
                except:
                    pass

        return new_answer


    def get_multi_match(self, text: str, list_of_options: list, model=None, loop_limit=4, timeout=None, temperature=None) -> list:
        prompt = f"""Respond with a list of items from this list: {list_of_options}
        Content to classify: "{text}"

        Respond with a subset of matches from the list above. Each match should be on a new line, without any additional formatting or punctuation."""

        answer = self.retry_llm(prompt, model, loop_limit, timeout=timeout, temperature=temperature)
        print(f'Get Answer: {answer}') if self.verbose else None

        answer = answer.replace(',', '\n').replace(';', '\n')
        candidates = [line.strip() for line in answer.split('\n') if line.strip()]

        # Process the candidates, directly adding matches, and using get_match for others
        processed_results = []
        for candidate in candidates:
            if candidate in list_of_options:
                processed_results.append(candidate)
            else:
                match = self.get_match(candidate, list_of_options, model, loop_limit, timeout, temperature)
                if match:
                    processed_results.append(match)

        return processed_results


    def get_topic(self, text: str, list_of_options: list, model=None, loop_limit=4, timeout=None, temperature=None) -> str:
        '''
        Like get_match, default optimized for topic recognition
        '''

        list_copy = []
        for option in list_of_options:
            list_copy.append(option.strip().replace('.', '').lower().strip('"').strip("'"))
        prompt_template = """Respond with one of the options on this list: {list_of_options}
        Content to classify: "{content}"  \n\nClassifiy the content above based on which topic it is mostly related to one topic: {list_of_options}"""

        prompt = prompt_template.format(content=text, list_of_options=list_copy)
        topic = self.retry_llm(prompt, model, loop_limit, timeout=timeout, temperature=temperature)
        print(f"Topic Answer: {topic}") if self.verbose else 0

        if topic is not None:
            topic = list_of_options[list_copy.index(topic)]  # return original topic

        return topic


    def match_or_make(self, text, list_of_options: list = [], direction='Make a simple and general category to classify content like this', number_of_words_in_category_name=2, model=None, loop_limit=20) -> str:
        '''
            "M&M" Returns exact match or new option. Input text and list_of_options.
            If no list is input, then one will be made and be output

            Internally, decides whether or not to make a new option.
            Then decides on match is no new option.
            If new option, create it, then finalize it
        '''
        if not list_of_options:
            answer = self.make_option_from_zero(text, direction, model=model)
            binary = 'yes'
        else:
            yn_prompt = f'''Is this content able to be categorized in one of the provided categories? Categories: {list_of_options}
            Respond "No" if a new category should be made.
            Respond "Yes" if the right category already exists in the list'''
            binary = self.get_yes_no(text, yn_prompt, model=model)

            if binary == 'yes':
                answer = self.get_match(text, list_of_options, model=model)

            if binary == 'no':
                answer = self.make_option(text, list_of_options, model=model)

        if self.verbose == True:
            print(f"M&M Initial Answer: {answer}")

        if binary == 'yes':
            return answer
        else:
            loops = 0
            while True:
                if loops >= loop_limit:
                    break
                answer = self.finalize_category(text, answer, number_of_words_in_category_name, model=model)
                if self.verbose == True:
                    print(f"M&M Answer {loops}: {answer}")
                loops += 1
                if (len(answer.split())) <= 2:
                    break

        return answer


    # internal function
    def make_option(self, text, list_of_options: list, direction='Make a simple and general category to classify content like this', model=None, timeout=None, temperature=None) -> str:
        prompt_template = """Content to classify: "{content}"  \n\n
        Create a new category for the content based on these other categories in this list: {list_of_options}, 
        and this classification direction: {direction}"""

        prompt = prompt_template.format(content=text, list_of_options=list_of_options, direction=direction)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def make_option_from_zero(self, text, direction='Make a simple and general category to classify content like this', model=None, timeout=None, temperature=None):
        '''
            Option without anything to go off of but the text input
        '''
        prompt_template = """Given the following content: {content}
        {direction}. Respond only with the category, and
        no explination before or after, just the name of the catagory. \n\nThe name of the category is: """

        prompt = prompt_template.format(content=text, direction=direction)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def finalize_category(self, text, prev_answer, number_of_words=2, model=None, timeout=None, temperature=None):
        prompt_template = """Given the following category suggestion: "{prev_answer}"
        \nand this text: "{text}" The final and simple 1 to {number_of_words} word category name I created for it is: """

        prompt = prompt_template.format(prev_answer=prev_answer, text=text, number_of_words=number_of_words)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def isolate_yes_no(self, content, question: str, model=None, timeout=None, temperature=None):
        '''Not recommended for external use. Internal function'''
        prompt_template = """Do not respond with anything before the yes or no. Do not add anything after the "yes" or "no".
        Example question 1: 'Is the Eiffel tower located in Paris?' Example answer 1: 'Yes' Example question 2: 'Do you think I am fat?'
        Example answer 2: 'No' Example question 3: 'Should I use Matplotlib in Python to draw a graph of csv information I have' Example answer 3: 'Yes'
        Example question 4: 'As an ai language model, I can't tell you yes or no, but I it does have a tendency to work sometimes.' Example answer 4: 'Yes'
        Example question 5: 'Will this happen if it's 19 percent likely to happen?' Example answer 5: 'No'
        \nRespond with a "yes" or "no" to following: "{question}"  """

        prompt = prompt_template.format(content=content, question=question)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def yay_or_nay(self, content, question: str, model=None, timeout=None, temperature=None):
        '''Not recommended for external use. Internal function'''
        prompt_template = """Do not respond with anything before the yes or no. Do not add anything after the "yes" or "no".
        Example question 1: 'Is the Eiffel tower located in Paris?' Example answer 1: 'Yes' Example question 2: 'Do you think I am fat?'
        Example answer 2: 'No' Example question 3: 'Should I use Matplotlib in Python to draw a graph of csv information I have' Example answer 3: 'Yes'
        Example question 4: 'As an ai language model, I can't tell you yes or no, but I it does have a tendency to work sometimes.' Example answer 4: 'Yes'
        Example question 5: 'Will this happen if it's 19 percent likely to happen?' Example answer 5: 'No'
        \nGiven this content: "{content}", Respond with a "yes" or "no" to following question: "{question}"  """

        prompt = prompt_template.format(content=content, question=question)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def yay_or_nay_question_in_content(self, content: str, model=None, timeout=None, temperature=None):
        '''Not recommended for external use. Internal function'''
        prompt_template = """Do not respond with anything before the yes or no. Do not add anything after the "yes" or "no".
        Example question 1: 'Is the Eiffel tower located in Paris?' Example answer 1: 'Yes' Example question 2: 'Do you think I am fat?'
        Example answer 2: 'No' Example question 3: 'Should I use Matplotlib in Python to draw a graph of csv information I have' Example answer 3: 'Yes'
        Example question 4: 'As an ai language model, I can't tell you yes or no, but I it does have a tendency to work sometimes.' Example answer 4: 'Yes'
        Example question 5: 'Will this happen if it's 19 percent likely to happen?' Example answer 5: 'No'
        User: "{content}"

        Respond with a "yes" or "no"
        Agent:"""

        prompt = prompt_template.format(content=content)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def zero_or_one(self, content, zero_if: str, one_if: str, model=None, timeout=None, temperature=None):
        '''Not recommended for external use. Internal function'''
        prompt_template = """Do not respond with anything before the 1 or 0. Do not add anything after the "1" or "0".
        Example question 1: 'Is the Eiffel tower located in Paris?' Example answer 1: '1' Example question 2: 'Do you think I am fat?'
        Example answer 2: '0' Example question 3: 'Should I use Matplotlib in Python to draw a graph of csv information I have' Example answer 3: '1'
        Example question 4: 'As an ai language model, I can't tell you yes or no, but I it does have a tendency to work sometimes.' Example answer 4: '1'
        Example question 5: 'Will this happen if it's 19 percent likely to happen?' Example answer 5: '0'
        \nGiven this content: "{content}", Respond with a "0" if {zero_if} \n... or "1" if: "{one_if}"  """

        prompt = prompt_template.format(content=content, zero_if=zero_if, one_if=one_if)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # internal function
    def isolate_zero_one(self, content, model=None, timeout=None, temperature=None):
        '''Not recommended for external use. Internal function'''
        prompt_template = """Do not respond with anything before the 1 or 0. Do not add anything after the "1" or "0".
        Example question 1: 'Is the Eiffel tower located in Paris?' Example answer 1: '1' Example question 2: 'Do you think I am fat?'
        Example answer 2: '0' Example question 3: 'Should I use Matplotlib in Python to draw a graph of csv information I have' Example answer 3: '1'
        Example question 4: 'As an ai language model, I can't tell you yes or no, but I it does have a tendency to work sometimes.' Example answer 4: '1'
        Example question 5: 'Will this happen if it's 19 percent likely to happen?' Example answer 5: '0'
        \nGiven this content: "{content}", Respond with a "0" or "1": """

        prompt = prompt_template.format(content=content)

        return self.retry_llm(custom_prompt=prompt, model=model, timeout=timeout, temperature=temperature)


    # This function is called by the others to handle retries:
    def retry_llm(self, custom_prompt, model=None, loop_limit=2, temperature=0, timeout=None):
        for i in range(loop_limit):
            try:
                response_queue = queue.Queue()
                def call_llm(response_queue, prompt, model, temperature):
                    try:
                        response = self.llm(custom_prompt=prompt, model=model, temperature=temperature)
                        response_queue.put(response)
                    except Exception as e:
                        response_queue.put(e)

                # Create and start the thread to call the LLM
                thread = threading.Thread(target=call_llm, args=(response_queue, custom_prompt, model, temperature))
                thread.start()

                # Wait for the response with a timeout
                timeout = self.timeout if timeout is None else timeout
                try:
                    response = response_queue.get(timeout=timeout)
                    if isinstance(response, Exception):
                        raise response
                    return response.strip().replace('.', '').lower().strip('"').strip("'")
                except queue.Empty:
                    print(f"Attempt {i+1}: Request timed out. Retrying...")
                    continue  # Continue to retry until loop_limit is reached

            except Exception as e:
                if i < loop_limit - 1:  # i is zero indexed
                    print(f"Attempt {i+1} failed with error: {str(e)}. Retrying...")
                else:
                    print(f"Final attempt {i+1} failed with error: {str(e)}. No more retries.")
                    raise e  # Optionally, re-raise the exception or handle it accordingly



    def perfect(self, content, instructions: str, model=None, timeout=None, temperature=None, yes_no_timeout=None):
        '''Wrapper function ensures that you get exactly what you wanted, and will not return until you get what you wanted'''
        output = self.get_yes_no(model=model, text=f"These are the instructions: {instructions} and this is the Output: {content}",
                    question=f"Does the output match the instructions?", timeout=yes_no_timeout) == 'no'

        while output:
            new_intstructions = f'''The following content does not match the instructions exactly. Your job is to return the content exactly as the instructions direct:
            Instructions: {instructions}

            Content: {content}

            Return the content exactly as the instructions direct'''

            content = self.llm(new_intstructions, model=model, timeout=timeout, temperature=temperature)
            if self.verbose == True:
                print("Content:", content)
            output = self.get_yes_no(model=model, text=f"These are the instructions: {instructions}",
                        question=f"This is the Output: {content} \n\nDoes this output match the instructions?", timeout=yes_no_timeout) == 'no'
        return content