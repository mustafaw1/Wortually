import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

def generate_assessment_questions(job_title, skills, max_retries=3):
    # Get the API key directly from the .env file
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 10000,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    def request_questions(remaining_questions):
        chat_session = model.start_chat(history=[])

        skills_str = ", ".join(skills)
        prompt = f"""
        Please generate exactly {remaining_questions} multiple-choice interview and assessment questions for the job title of {job_title}. 
        Focus specifically on the following skills: {skills_str}.
        Each question must have 4 options and one correct answer. Provide the response in JSON format with the following structure:
        {{
          "questions": [
            {{
              "question": "Question text",
              "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
              ],
              "correct_answer": "Option 2"
            }},
            ...
          ]
        }}
        It is imperative that the response contains exactly {remaining_questions} questions.
        Job Title: {job_title}
        Skills: {skills_str}
        """

        response = chat_session.send_message(prompt)
        return response

    # Reset the list of questions for each request
    all_questions = []

    for attempt in range(max_retries):
        remaining_questions = 30 - len(all_questions)
        response = request_questions(remaining_questions)
        try:
            questions = json.loads(response.text)["questions"]
            all_questions.extend(questions)
            if len(all_questions) == 30:
                # Ensure we return exactly 30 questions
                return all_questions[:30]
            else:
                print(
                    f"Attempt {attempt + 1}: The number of questions generated is {len(all_questions)}, which is not equal to 30."
                )
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1}: Failed to decode JSON response: {e}")
        except KeyError as e:
            print(
                f"Attempt {attempt + 1}: Key error: {e}. The response structure may be incorrect."
            )

    print("Failed to generate exactly 30 questions after several attempts.")
    # In case of failure to generate 30 questions, return what was generated
    return all_questions[:30]
