from openai import OpenAI


class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.party_membership = "Liberal" if self.role == "Liberal" else "Fascist"
        self.main_prompt = None

        self.client = OpenAI()
        self.messages = None

    def set_main_prompt(self, main_prompt):
        self.main_prompt = main_prompt
        self.messages = [{"role": "system", "content": self.main_prompt}]

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            stream=True
        )
        print(f"{self.name} ({self.role}) is saying:\n")
        output = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                output += chunk.choices[0].delta.content
        self.messages.append({"role": "assistant", "content": output})
