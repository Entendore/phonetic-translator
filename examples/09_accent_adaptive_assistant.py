"""Use Case 9: Accent-Adaptive Voice Assistant"""
from translator import PhoneticTranslator

class AccentAdaptiveAssistant:
    def __init__(self):
        self.translator = PhoneticTranslator()
        self.commands = {
            'turn on the lights': ['lights on', 'turn lights'],
            'play music': ['play song', 'start music'],
            'what time is it': ['time', 'current time'],
        }
    
    def understand_command(self, spoken_text: str):
        spoken_ipa = self.translator.text_to_ipa(spoken_text, 'en')
        spoken_phonemes = self.translator.ipa_to_phonemes(spoken_ipa)
        matches = []
        for command in self.commands:
            cmd_ipa = self.translator.text_to_ipa(command, 'en')
            cmd_phonemes = self.translator.ipa_to_phonemes(cmd_ipa)
            common = sum(1 for a, b in zip(spoken_phonemes, cmd_phonemes) if a == b)
            max_len = max(len(spoken_phonemes), len(cmd_phonemes))
            similarity = common / max_len if max_len > 0 else 0
            matches.append({'command': command, 'similarity': similarity})
        matches.sort(key=lambda x: -x['similarity'])
        return {'spoken': spoken_text, 'spoken_ipa': spoken_ipa, 'matches': matches[:3]}

if __name__ == "__main__":
    assistant = AccentAdaptiveAssistant()
    result = assistant.understand_command("torn on the lights")
    print(f"Spoken: {result['spoken']}")
    print(f"IPA: {result['spoken_ipa']}\n")
    print("Top matches:")
    for i, m in enumerate(result['matches'], 1):
        print(f"  {i}. {m['command']} ({m['similarity']:.1%})")
