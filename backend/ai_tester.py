from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

aiml_api_key = os.getenv("AIML_API_KEY")
aiml_base_url = os.getenv("AIML_API_BASE_URL")
print("Loded API config:\nAIML API Key:", aiml_api_key, "\nAIML Base URL:", aiml_base_url)

api = OpenAI(
        api_key=aiml_api_key,
        base_url=aiml_base_url,
)

system_prompt = "You are a helpful AI assistant that replies consisely in one or few words, never more than a sentence."
# user_prompt = "What are the minimum requirements to completely define a simple wordpress plugin?"
# user_prompt = input("User: ")

# while user_prompt.strip() != "":
#     print("Calling AI...")
#     api = OpenAI(
#         api_key=aiml_api_key,
#         base_url=aiml_base_url,
#     )
#     completion = api.chat.completions.create(
#         model="openai/gpt-5-2025-08-07",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         # max_tokens=100,
#         temperature=0.2,
#         verbosity="high"
#     )
#     response = completion.choices[0].message.content
#     print("AI: ", response)
#     print()
#     user_prompt = input("User: ")



messages= [
            {"role": "system", "content": "You are a maths AI bot that does calculation and directly returns answer, no working showed."},
            {"role": "assistant", "content": "How may i help?"},
            {"role": "user", "content": "Please do 2+ 1090"},
]

messages1 = messages + [{"role": "assistant", "content": "For sure, please wait while i pull out my calc"}]

messages2 = messages1 + [{"role": "assistant", "content": "1092"},  {"role": "user", "content": "Now subtract 100 from it"}]

# # messages
# print(messages1)
# exit()
completion = api.chat.completions.create(
    model="openai/gpt-5-2025-08-07",
    messages=messages2,
    max_tokens=1000,
    temperature=0.2,
    # verbosity="high"
)
print()
print(completion.to_json())
print()
response = completion.choices[0].message.content
for message in messages2:
    print(f"{message['role']}: {message['content']}")

print(f"AI: {response}")