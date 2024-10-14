"""
@Author: Prayag Bhoir
@Date: 13-10-2024
@Last Modified by: Prayag Bhoir
@Last Modified time: 14-10-2024
@Title: Email processing - Summarization and Translation using Google Generative AI.
"""

import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values
import pandas as pd
import time

config = dotenv_values()  # Load all variables into a dictionary

# Configure the API key directly using dotenv
api_key = config.get("API_KEY")
if api_key is None:
    raise ValueError("API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

def process_emails(input_file, output_file):
    """
    Description:
      Processes a text file containing emails, summarizes the email body, translates it into Hindi, and saves the results to a CSV file.
      
    Parameters:
      input_file (str): The path to the input file containing email data (from_email, to_email, mail_body).
      output_file (str): The path to the output CSV file where processed email data will be saved.

    Returns:
      None
    """
    results = []  # To store the results

    with open(input_file, 'r') as file:
        for line in file:
            from_email, to_email, mail_body = line.strip().split(',', 2)
            
            # Create prompt for summarization
            summarize_prompt = f"Summarize the following email: {mail_body}"

            # Summarize email body
            summary_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(summarize_prompt)
            summarized_body = summary_response.text.strip()

            time.sleep(2)
            
            # Create prompt for translation
            translate_prompt = f"Convert the following summarize email body in Spanish languange as it is. summarize email: {summarized_body}"

            # Translate email body to Spanish
            translation_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(translate_prompt)
            translated_body = translation_response.text.strip()
            
            time.sleep(2)

            # Store the result
            results.append({
                'from': from_email,
                'to': to_email,
                'body': mail_body,
                'summarized_body': summarized_body,
                'translated_body': translated_body
            })

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

def main():
    # Specify input and output files
    input_file = r'C:\Users\bhoir\OneDrive\Desktop\pratice_bl\Prompt_Engineering\summarization_and_tranformation\mails.txt'
    output_file = r'C:\Users\bhoir\OneDrive\Desktop\pratice_bl\Prompt_Engineering\summarization_and_tranformation\processed_emails.csv'

    process_emails(input_file, output_file)
    print("Email processing complete. Check the output CSV file.")


if __name__ == "__main__":
    main()
