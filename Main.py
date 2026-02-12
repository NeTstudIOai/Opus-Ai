import re

class QuestionAnalyzerAI:
    def __init__(self):
        self.wh_words = ["what", "where", "when", "why", "who", "which", "whom", "whose", "how"]
        self.yes_no_starters = ["is", "are", "was", "were", "do", "does", "did", "can", "could",
                                "will", "would", "should", "has", "have", "had"]
        self.true_false_words = ["true or false", "true/false", "t/f"]

        self.positive_words = ["good", "great", "excellent", "amazing", "love"]
        self.negative_words = ["bad", "terrible", "worst", "hate", "awful"]

    def analyze(self, text):
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)

        result = {}

        # Detect WH word
        result["WH Word"] = next((w for w in self.wh_words if w in words), None)

        # Detect Yes/No Question
        result["Yes/No Question"] = words[0] in self.yes_no_starters if words else False

        # Detect True/False
        result["True/False Question"] = any(tf in text_lower for tf in self.true_false_words)

        # Detect Multiple Choice
        result["Multiple Choice"] = bool(re.search(r'\b[a-d]\)', text_lower))

        # Detect Tone
        if any(word in words for word in self.positive_words):
            result["Tone"] = "Positive"
        elif any(word in words for word in self.negative_words):
            result["Tone"] = "Negative"
        else:
            result["Tone"] = "Neutral"

        # Extract Keywords (remove common small words)
        stopwords = {"the", "is", "are", "a", "an", "in", "on", "at", "to", "for", "of", "and"}
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        result["Keywords"] = keywords

        # Question Type Summary
        if result["True/False Question"]:
            result["Question Type"] = "True/False"
        elif result["Multiple Choice"]:
            result["Question Type"] = "Multiple Choice"
        elif result["Yes/No Question"]:
            result["Question Type"] = "Yes/No"
        elif result["WH Word"]:
            result["Question Type"] = "WH Question"
        else:
            result["Question Type"] = "Unknown"

        return result


# ====== RUN AI ======
if __name__ == "__main__":
    ai = QuestionAnalyzerAI()
    while True:
        user_input = input("Enter your question: ")
        analysis = ai.analyze(user_input)

        print("\n🧠 AI Analysis Result:")
        for key, value in analysis.items():
            print(f"{key}: {value}")

