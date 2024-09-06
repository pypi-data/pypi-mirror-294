from openai import OpenAI

class NLIF():
    def __init__(self, API_key) -> None:
        try:
            self.client = OpenAI(api_key = API_key)
        except Exception as e:
            print(f"An error occurred: {e}")

    def nlif(self, proposition):
        try:
            setting_prompt = "You are a system that returns 1 when the given proposition is true, and 0 when it is false or unknown."
            messages = [{"role": "system", "content": setting_prompt, }, 
                        {"role": "user", "content": proposition, }, ]
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
            )
            return int(response.choices[0].message.content)
        except Exception as e:
            print(f"An error occurred: {e}")