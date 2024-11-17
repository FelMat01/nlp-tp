from langchain_huggingface import HuggingFaceEndpoint
from collections import defaultdict

PROMPT_TEMPLATE = """
        <|system|>
        Generate a paragraph for the class WITHOUT NAMING THE CLASS based on the context. DO NOT REPEAT THE CLASS IN THE PARAGRAPH. In {number_of_words} words.
        Context:
        {context}
        
        Class: 
        {specific_class}

        Examples:
        {examples}

        Note: Deviate from examples.

        </s>
        <|assistant|>
        """

class DatasetGenerator:
    def __init__(self, model_repo:str) -> None:
        self.llm = HuggingFaceEndpoint(repo_id=model_repo, max_new_tokens=1000, repetition_penalty=1.03, timeout = 300)
         
    def generate(self, context:str, classes:list[str], samples_per_class : int = 5, number_of_words : int = 50) -> dict[str,str]:
        responses = defaultdict(list)
            
        for specific_class in classes:
            examples= ""
            for _ in range(samples_per_class):
                prompt = PROMPT_TEMPLATE.format(context=context, specific_class=specific_class, number_of_words=number_of_words, examples=examples)
                response = self.llm.invoke(prompt)

                print(response)

                responses[specific_class].append(response)
                examples += f"{response}\n\n"
                

        return responses