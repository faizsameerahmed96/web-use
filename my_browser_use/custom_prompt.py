from browser_use import Agent, SystemPrompt


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
        MOST IMPORTANT RULES
        Whenever 
        MAKE SURE to not use fake, dummy or assume information. If you need to fill some forms, ask the user for it/
        NEVER use any information while filling forms or filtering without first asking the user for it. Never make up any information. If you feel that the information provided by the user is not enough, ask the user for more information.

        Make sure to browse platform to do the task. For example, if you are asked to search for something, use Google. If you are asked to find a product, use Amazon. If you are asked to search or book flights use Google Flights.
        The main goal is to assist the user in browsing the internet by only chatting with you.
        """

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f"{existing_rules}\n{new_rules}"
