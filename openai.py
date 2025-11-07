import openai

openai.api_key = "your_openai_api_key"

def parse_reminder(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract the date and time from this reminder: '{input_text}'",
        max_tokens=50
    )
    return response.choices[0].text.strip()

user_input = "Remind me to call mom tomorrow at 6 PM"
parsed_data = parse_reminder(user_input)
print(parsed_data)  # Output: "Date: Tomorrow, Time: 6 PM"
