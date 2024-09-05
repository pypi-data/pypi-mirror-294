from typing import Any, Dict

class DynamicResponder:
    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile

    def get_system_prompt(self, channel: str = "email") -> str:
        return self._build_prompt(channel)

    def _build_prompt(self, channel: str) -> str:
        return f"""
You are {self.profile['name']}, a {self.profile['role']} at {self.profile['company']}. Your task is to respond to messages as if you were {self.profile['name']}, maintaining their persona and adhering to the following policy and restrictions.

Key Information:
{self._format_key_info()}

Policy:
{self._format_list(self.profile.get('policy', []))}

Restrictions:
{self._format_list(self.profile.get('restrictions', []))}

Response Format for {channel.capitalize()}:
{self._get_channel_format(channel)}

Remember: You are embodying {self.profile['name']}. Respond thoughtfully and in alignment with the provided policy and restrictions, while directly addressing the specific message received.
"""

    def _format_key_info(self) -> str:
        return '\n'.join(f"- {key.capitalize()}: {value}" for key, value in self.profile.items() if key in ['nickname', 'role', 'company', 'email', 'calendar_link'])

    def _format_list(self, items: list) -> str:
        return '\n'.join(f"- {item}" for item in items)

    def _get_channel_format(self, channel: str) -> str:
        if channel == "email":
            return """
- Start with a greeting: "Hi [Name],"
- End with a professional sign-off: "Best regards, [Your Name]"
- Use proper email etiquette and formatting
- Include any necessary email signatures or disclaimers
"""
        elif channel == "slack":
            return """
- Use a more casual tone, but remain professional
- Start with a friendly greeting, like "Hey [Name]!"
- Use appropriate Slack formatting (bold, italics, etc.), Mention users with @username
- More straight forward and concise, very human like, no need to be too fancy or wordy, keep it short and to the point, no need for closing remarks.
"""
        else:
            return "Adapt your response format to the specific channel's norms and expectations."