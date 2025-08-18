import openai
import pandas as pd
import re
import time
from typing import List, Tuple, Optional
import read_data
import numpy as np
from openai import OpenAI


class BedroomBathroomEstimator:
    def __init__(self, client, model: str = "gpt-4.1"):
        """
        Initialize the GPT-based estimator.
        
        Args:
            api_key (str): OpenAI API key.
            model (str): GPT model to use (default: "gpt-4.1").
            model gpt-4o doesn't work
        """
        self.client = client
        self.model = model
        self.context_messages = []  # Holds history of system/user setup

    
    def general_input(self, sentence):
        '''
        This part is to input some general sentence but not collecting the results
        For example: 'Please help me analyze the following things.' or 'Please be consice'
        '''
        self.context_messages.append({"role": "user", "content": sentence})
        print(f"📝 Added general input: '{sentence}'")


    def query_gpt(self, question, use_context) -> str:
        """
        Send a question to GPT and return the model's response.

        Args:
            question (str): The user question (e.g., an address-related query).
            use_context (bool): Whether to include context_messages.

        Returns:
            Tuple[str, int | None, float | None]:
                - GPT's response text (str)
                - Total token usage (int) if available, else None
                - Elapsed time in seconds (float) if successful, else None
        """
        # Start with existing context if enabled
        messages = self.context_messages.copy() if use_context else []
        # Append the user query as the latest message
        messages.append({"role": "user", "content": question})
        start = time.time()


        try:
            # Make API call to GPT model
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            # Extract response text from the first returned choice
            text =  response.choices[0].message.content.strip()
            elapsed = round(time.time() - start, 2)
            # Retrieve total tokens used if available
            tokens = response.usage.total_tokens if hasattr(response, "usage") else None
            return text, tokens, elapsed
        except Exception as e:
            print(f"⚠️ GPT query failed: {e}")
            return "", None, None

    def extract_bed_bath(self, text):
        """
        Extract bedroom and bathroom counts from GPT response using regular expressions.

        Args:
            text (str): The text response from GPT that may include bed/bath counts.

        Returns:
            Tuple[float | None, float | None]: 
                - beds: extracted number of bedrooms as float (or None if not found)
                - baths: extracted number of bathrooms as float (or None if not found)
        """       
        # Match patterns like "2 beds", "3 bedrooms", "bedrooms: 4" (case-insensitive)
        bed_match = re.search(r'bed(?:room)?s?:?\s*(\d+)', text, re.IGNORECASE)
        bath_match = re.search(r'bath(?:room)?s?:?\s*(\d+)', text, re.IGNORECASE)

        # Convert matched strings to float if found; otherwise return None
        beds = float(bed_match.group(1)) if bed_match else None
        baths = float(bath_match.group(1)) if bath_match else None
        return beds, baths

    def estimate_all(self, questions: pd.Series, qpid) -> pd.DataFrame:
        """
        Loop through each question, query GPT, and extract results.

        Args:
            questions (pd.Series): One question per row (e.g. address-based)
            qpid: Unique property IDs corresponding to each question.

        Returns:
            pd.DataFrame: With question, GPT response, bedroom and bathroom counts
        """
        results  = []
        for i, question, qpid_i in zip(range(len(questions)), questions, qpid):
            # Print progress every 100 entries
            if i % 100 == 0:
                print(f'Now is the loop {i}')

            # Handle missing input question
            if question == 'NaN':
                results.append({
                    "question": question,
                    "gpt_response": 'NaN',
                    "qpid": qpid_i,
                    "bathrooms": 'NaN',
                    "bedrooms": 'NaN',
                    "tokens_used": 'NaN',
                    "time_seconds": 'NaN'
                })
                continue

            # Query GPT and extract result
            response, tokens, elapsed = self.query_gpt(question, True)
            beds, baths = self.extract_bed_bath(response)

            # Retry until a valid number of bedrooms is extracted
            while beds == None or beds == 'NaN':
                response, tokens, elapsed = self.query_gpt(question, True)
                beds, baths = self.extract_bed_bath(response)
            # record results
            results.append({
                "question": question,
                "gpt_response": response,
                "qpid": qpid_i,
                "bathrooms": baths,
                "bedrooms": beds,
                "tokens_used": tokens,
                "time_seconds": elapsed
            })
        return pd.DataFrame(results)



if __name__ == "__main__":


    sample_path = 's3://pr-home-datascience/Projects/AdHoc/InternProjects/2025/2025_Summer_AI_Property_Attributes/property_list_NJ_sample.csv'

    # Use the class in read_data.py to load the sample data
    df_samples = read_data.DataReader(sample_path)
    df_samples.preview()

    # Load the question file 
    # Load the question txt 
    print('The promps for the GPT will be as follows:')
    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = np.array(f.read().splitlines(), dtype=str)
    for line in questions:
        print(line)


    # Load the address txt
    # address     city state   zip5  zip4
    df_samples.data["full_address"] = df_samples.data["address"] + ", " + df_samples.data["city"] + ", " + df_samples.data["state"] +\
                                ", " + df_samples.data["zip5"] + '-' + df_samples.data["zip4"] 
                                


    print('\nThe final questions for the GPT that will be recorded are:')

    df_samples.data['questions'] = questions[2] + df_samples.data["full_address"]
    print(df_samples.data['questions'][0])
    print(df_samples.data['questions'][1])

        
    client  = OpenAI(api_key = "")

    estimator = BedroomBathroomEstimator(client=client, model="gpt-4.1")
    estimator.general_input("Please respond in format: 'Bedrooms: X, Bathrooms: Y'")
    #estimator.general_input(questions[1])

    df = estimator.estimate_all(df_samples.data['questions'][0:5], df_samples.data['qpid'][0:5])

    print(df.head())
