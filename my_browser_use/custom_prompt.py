from browser_use import Agent, SystemPrompt


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
        9. MOST IMPORTANT RULE:
        - ALWAYS open first a new tab and go to wikipedia.com no matter the task!!!
        """

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f"{existing_rules}\n{new_rules}"
