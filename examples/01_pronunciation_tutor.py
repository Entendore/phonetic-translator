"""Use Case 1: L2 Pronunciation Tutor"""
from translator import PhoneticTranslator

class PronunciationTutor:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def check_pronunciation(self, target_word: str, student_said: str, lang: str = 'en'):
        target_ipa = self.translator.text_to_ipa(target_word, lang)
        student_ipa = self.translator.text_to_ipa(student_said, lang)
        target_phonemes = self.translator.ipa_to_phonemes(target_ipa)
        student_phonemes = self.translator.ipa_to_phonemes(student_ipa)
        
        feedback = []
        for i, (t, s) in enumerate(zip(target_phonemes, student_phonemes)):
            if t != s:
                distance = self.translator.phonetic_distance(t, s)
                feedback.append({
                    'position': i, 'expected': t, 'actual': s,
                    'distance': distance,
                    'severity': 'high' if distance > 5 else 'medium' if distance > 2 else 'low'
                })
        
        return {
            'target': target_word, 'target_ipa': target_ipa,
            'student_said': student_said, 'student_ipa': student_ipa,
            'feedback': feedback, 'score': max(0, 100 - len(feedback) * 10)
        }

if __name__ == "__main__":
    tutor = PronunciationTutor()
    result = tutor.check_pronunciation("think", "sink")
    print(f"Target: {result['target']} ({result['target_ipa']})")
    print(f"You said: {result['student_said']} ({result['student_ipa']})")
    print(f"Score: {result['score']}/100\n")
    for fb in result['feedback']:
        print(f"Position {fb['position']}: Expected /{fb['expected']}/ but said /{fb['actual']}/")
