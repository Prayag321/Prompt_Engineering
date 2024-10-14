"""
  @Author: Prayag Bhoir
  @Date: 13-10-2024
  @Last Modified by: Prayag Bhoir
  @Last Modified time: 14-10-2024
  @Title: Product Review Processing - Sentiment Analysis and Product Identification using Google Generative AI.
"""

import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values
import pandas as pd
import time

# Load environment variables from .env file
config = dotenv_values() 

# Configure the API key directly using dotenv
api_key = config.get("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

def process_reviews(input_file, output_file, delimiter="|"):
    """
    Description:
      Processes a text file containing product reviews, identifies the product and analyzes the sentiment using the Google Gemini API.
      The results are saved in a CSV file.

    Parameters:
      input_file (str): The path to the input file containing product reviews separated by a delimiter.
      output_file (str): The path to the output CSV file where the results will be saved.
      delimiter (str): The delimiter used to separate reviews in the input file. Default is '|'.

    Returns:
      None: The results are saved in a CSV file.
    """
    results = []  # To store the results

    # Read reviews from the file
    with open(input_file, 'r') as file:
        reviews = file.read().split(delimiter)

    for review in reviews:
        review = review.strip()

        # Skip empty
        if not review:
            continue

        # Create prompts to identify the product, determine sentiment, Generate the replay
        product_prompt = f"From the following review, can you identify what product it is about in one word: '{review}'? If not clear, say 'Not Confirmed'."
        sentiment_prompt = f"Tell the sentiment of the following review in positive or negative? If unclear, say 'Neutral in one wordS'. Review: '{review}'"
        replay_prompt = f"From the following review, can you replay to the customer in a polite and concise manner. Review: '{review}'"

        # Request for product name
        product_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(product_prompt)
        product_name = product_response.text.strip()

        time.sleep(5) 

        # Request for sentiment analysis
        sentiment_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(sentiment_prompt)
        sentiment = sentiment_response.text.strip().lower()

        time.sleep(5) 

        # Request for re-play
        replay_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(replay_prompt)
        user_reply = replay_response.text.strip()


        results.append({
            'actual_review': review,
            'product_name': product_name,
            'sentiment': sentiment,
            'reply_to_user': user_reply
        })

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

def main():
    # Specify input and output files
    input_file = r'C:\Users\bhoir\OneDrive\Desktop\pratice_bl\Prompt_Engineering\infering_and_expanding\reviews.txt'
    output_file = r'C:\Users\bhoir\OneDrive\Desktop\pratice_bl\Prompt_Engineering\infering_and_expanding\processed_reviews.csv'

    process_reviews(input_file, output_file)
    print("Review processing complete. Check the output CSV file.")


if __name__ == "__main__":
    main()
