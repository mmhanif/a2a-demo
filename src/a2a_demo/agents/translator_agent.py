"""Translator agent for language translation."""

from ..models import AgentCard, Skill, TaskMessage, InteractionMode
from .base_agent import BaseAgent


class TranslatorAgent(BaseAgent):
    """An agent that translates text between languages."""
    
    # Simple mock translations for demo purposes
    TRANSLATIONS = {
        "hello": {"spanish": "hola", "french": "bonjour", "german": "hallo"},
        "goodbye": {"spanish": "adiós", "french": "au revoir", "german": "auf wiedersehen"},
        "thank you": {"spanish": "gracias", "french": "merci", "german": "danke"},
        "yes": {"spanish": "sí", "french": "oui", "german": "ja"},
        "no": {"spanish": "no", "french": "non", "german": "nein"},
        "please": {"spanish": "por favor", "french": "s'il vous plaît", "german": "bitte"},
        "good morning": {"spanish": "buenos días", "french": "bonjour", "german": "guten morgen"},
        "good night": {"spanish": "buenas noches", "french": "bonne nuit", "german": "gute nacht"},
    }
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5002):
        """Initialize the translator agent."""
        super().__init__(
            name="TranslatorAgent",
            description="An agent that translates text between English and other languages",
            host=host,
            port=port
        )
    
    def get_agent_card(self) -> AgentCard:
        """Return the agent card for the translator."""
        return AgentCard(
            name=self.name,
            description=self.description,
            url=f"http://{self.host}:{self.port}",
            skills=[
                Skill(
                    name="translate",
                    description="Translate text from English to Spanish, French, or German",
                    parameters={
                        "text": {
                            "type": "string",
                            "description": "Text to translate"
                        },
                        "target_language": {
                            "type": "string",
                            "description": "Target language (spanish, french, or german)",
                            "enum": ["spanish", "french", "german"]
                        }
                    },
                    interaction_modes=[InteractionMode.TEXT]
                )
            ],
            supported_interaction_modes=[InteractionMode.TEXT],
            metadata={"version": "1.0.0", "type": "translator", "supported_languages": ["spanish", "french", "german"]}
        )
    
    def handle_task(self, task_id: str, message: TaskMessage) -> str:
        """Process a translation request.
        
        Args:
            task_id: The task ID
            message: The message containing the translation request
            
        Returns:
            The translated text
        """
        content = message.content.lower().strip()
        
        # Parse the request
        # Expected format: "translate <text> to <language>"
        if "translate" in content and " to " in content:
            parts = content.split(" to ")
            if len(parts) == 2:
                text_part = parts[0].replace("translate", "").strip()
                target_language = parts[1].strip()
                
                return self._translate(text_part, target_language)
        
        return "Please use format: 'translate <text> to <language>' where language is spanish, french, or german"
    
    def _translate(self, text: str, target_language: str) -> str:
        """Translate text to the target language.
        
        Args:
            text: Text to translate
            target_language: Target language
            
        Returns:
            Translation result
        """
        if target_language not in ["spanish", "french", "german"]:
            return f"Unsupported language: {target_language}. I support spanish, french, and german."
        
        # Look up translation
        text_lower = text.lower().strip()
        if text_lower in self.TRANSLATIONS:
            translation = self.TRANSLATIONS[text_lower][target_language]
            return f'"{text}" in {target_language} is "{translation}"'
        
        # Try to find partial matches
        for phrase, translations in self.TRANSLATIONS.items():
            if phrase in text_lower:
                translation = translations[target_language]
                return f'I found "{phrase}" which translates to "{translation}" in {target_language}. (Note: This is a demo with limited vocabulary)'
        
        return f'I don\'t have a translation for "{text}" in my vocabulary. (Note: This is a demo with limited phrases: {", ".join(self.TRANSLATIONS.keys())})'


if __name__ == "__main__":
    agent = TranslatorAgent()
    agent.run(debug=True)
