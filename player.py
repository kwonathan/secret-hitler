import prompts

from openai import OpenAI


class Player:
    def __init__(self, name, role, is_human, model):
        self.name = name
        self.role = role
        self.party_membership = "Liberal" if self.role == "a Liberal" else "Fascist"
        self.is_human = is_human
        self.model = model
        self.main_prompt = None

        self.client = OpenAI()
        self.messages = None

    def set_main_prompt(self, main_prompt):
        self.main_prompt = main_prompt
        self.messages = [{"role": "system", "content": self.main_prompt}]

    def chat(self, message):
        if self.is_human:
            return input(f"{self.name}, enter your response: ")
        else:
            self.messages.append({"role": "user", "content": message})
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            print(f"%%%%%%%%%% {self.name} ({self.role}) %%%%%%%%%%\n")
            output = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
                    output += chunk.choices[0].delta.content
            print("\n\n")
            self.messages.append({"role": "assistant", "content": output})
            input("[PRESS ENTER TO CONTINUE]")
            return self.messages[-1]["content"]

    def select_chancellor(self, message_history):
        additional_prompt = prompts.CHANCELLOR_NOMINATION_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I would like to discuss Chancellor options" in output:
            return False, output
        else:
            return True, output

    def vote(self, message_history, nominated_president, nominated_chancellor):
        additional_prompt = prompts.VOTE_PROMPT.replace("[INSERT PRESIDENT NAME]", nominated_president.name).replace("[INSERT CHANCELLOR NAME]", nominated_chancellor.name)
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "Ja!" in output:
            return "Ja!"
        elif "Nein!" in output:
            return "Nein!"

    def enact_policy_president(self, policy_candidates, message_history):
        additional_prompt = prompts.ENACT_POLICY_PROMPT_PRESIDENT.replace("[INSERT POLICY 1]", policy_candidates[0]).replace("[INSERT POLICY 2]", policy_candidates[1]).replace("[INSERT POLICY 3]", policy_candidates[2])
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if output.split("I discard a ")[1].split(" Policy")[0] == "Liberal":
            policy_candidates.remove("Liberal")
            return "Liberal", policy_candidates
        else:
            policy_candidates.remove("Fascist")
            return "Fascist", policy_candidates

    def enact_policy_chancellor(self, policy_candidates, message_history):
        additional_prompt = prompts.ENACT_POLICY_PROMPT_CHANCELLOR.replace("[INSERT POLICY 1]", policy_candidates[0]).replace("[INSERT POLICY 2]", policy_candidates[1])
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if output.split("I discard a ")[1].split(" Policy")[0] == "Liberal":
            policy_candidates.remove("Liberal")
            return "Liberal", policy_candidates[0]
        else:
            policy_candidates.remove("Fascist")
            return "Fascist", policy_candidates[0]

    def enact_policy_veto(self, policy_candidates, message_history):
        additional_prompt = prompts.ENACT_POLICY_PROMPT_CHANCELLOR.replace("[INSERT POLICY 1]", policy_candidates[0]).replace("[INSERT POLICY 2]", policy_candidates[1]) + "\n\n" + prompts.ENACT_POLICY_VETO_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I wish to veto this agenda" in output:
            return True, None, None
        else:
            if output.split("I discard a ")[1].split(" Policy")[0] == "Liberal":
                policy_candidates.remove("Liberal")
                return False, "Liberal", policy_candidates[0]
            else:
                policy_candidates.remove("Fascist")
                return False, "Fascist", policy_candidates[0]

    def veto_accepted(self, message_history):
        additional_prompt = prompts.VETO_ACCEPT_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I agree to the veto" in output:
            return True
        else:
            return False

    def reveal_policy(self, message_history):
        additional_prompt = prompts.REVEAL_ENACTED_POLICY_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I choose not to reveal my discarded Policy":
            return False, None
        else:
            return True, output

    def investigate_loyalty(self, message_history):
        additional_prompt = prompts.INVESTIGATE_LOYALTY_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I would like to discuss the Investigate Loyalty power" in output:
            return False, output
        else:
            return True, output

    def reveal_party_membership(self, message_history, investigated_player):
        additional_prompt = prompts.REVEAL_PARTY_MEMBERSHIP_PROMPT.replace("[INSERT INVESTIGATED PLAYER NAME]", investigated_player.name).replace("[INSERT INVESTIGATED PLAYER PARTY MEMBERSHIP]", investigated_player.party_membership)
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        return output

    def call_special_election(self, message_history):
        additional_prompt = prompts.SPECIAL_ELECTION_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I would like to discuss the Special Election power" in output:
            return False, output
        else:
            return True, output

    def policy_peek(self, message_history, top_three_policies):
        additional_prompt = prompts.POLICY_PEEK_PROMPT.replace("[INSERT POLICY 1]", top_three_policies[0]).replace("[INSERT POLICY 2]", top_three_policies[1]).replace("[INSERT POLICY 3]", top_three_policies[2])
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        self.messages.append({"role": "user", "content": message})

    def execute_player(self, message_history):
        additional_prompt = prompts.EXECUTION_PROMPT
        print(additional_prompt)
        message = message_history + "\n\n" + additional_prompt
        output = self.chat(message)
        if "I would like to discuss the Execution power" in output:
            return False, output
        else:
            return True, output
