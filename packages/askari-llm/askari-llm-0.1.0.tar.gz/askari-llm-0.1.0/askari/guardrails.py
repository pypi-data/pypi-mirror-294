# askari/guardrails.py

import yaml

class PolicyGuardrails:
    def __init__(self, policy_file="policies.yaml"):
        # Load the policies from a YAML file
        with open(policy_file, 'r') as file:
            self.policies = yaml.safe_load(file)['policies']

    def check_input(self, user_input):
        """
        Checks if the user input follows the predefined policies.
        
        Args:
            user_input (str): The user's input message.
        
        Returns:
            bool: True if the input follows the policies, False otherwise.
            str: The policy violated or an empty string.
        """
        # Example simple checks
        if any(word in user_input.lower() for word in ["offensive_word_1", "offensive_word_2"]):
            return False, "No offensive language"
        if "personal information" in user_input.lower():
            return False, "No asking for personal information"
        
        # You can add more complex checks here
        
        return True, ""

    def enforce_policy(self, user_input):
        """
        Enforces the policy by checking the user input.
        
        Args:
            user_input (str): The user's input message.
        
        Returns:
            str: A message indicating the result of the policy check.
        """
        follows_policy, violated_policy = self.check_input(user_input)
        if follows_policy:
            return "Input accepted"
        else:
            return f"Input rejected: This input violates the following policy: {violated_policy}"
