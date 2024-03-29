import requests
import math
import os
import json

# Load the OpenAI API key from environment variable
OPENAI_API_KEY = "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"

# Define the AITextDetector class
class AITextDetector:
    def __init__(self):
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(OPENAI_API_KEY),
        }

    def detect(self, text):
        data = {
            "prompt": text + ".\n",
            "max_tokens": 1,
            "temperature": 1,
            "top_p": 1,
            "n": 1,
            "logprobs": 5,
            "stop": "\n",
            "stream": False,
            "model": "LTSM",  # Updated model name
        }
        response = requests.post(
            "https://api.openai.com/v1/completions", headers=self.header, json=data
        )
        if response.status_code == 200:
            choices = response.json()["choices"][0]
            key_prob = choices["logprobs"]["top_logprobs"][0]["!"] or -10
            prob = math.exp(key_prob)
            e = 100 * (1 - (prob or 0))
            for _, item in enumerate(assessments):
                if e <= item.get("max_score"):
                    label = item.get("assessment")
                    break
            if label is None:
                label = assessments[-1].get("assessment")
            top_prob = {
                "Verdict": "The classifier considers the text to be {0}{1}{2} AI-generated.".format(
                    "\033[1m" if prob > 0.5 else "",
                    label,
                    "\033[0m" if prob > 0.5 else "",
                ),
                "Probability": prob,
            }
            return top_prob
        else:
            raise Exception("Error: {0}".format(response.text))

# Define the assessments
assessments = [
    {"assessment": "Definitely AI-generated", "max_score": 0},
    {"assessment": "Probably AI-generated", "max_score": 20},
    {"assessment": "Possibly AI-generated", "max_score": 50},
    {"assessment": "Probably not AI-generated", "max_score": 80},
    {"assessment": "Definitely not AI-generated", "max_score": 100},
]

# Initialize the detector
text_detector = AITextDetector()

# Test the detector
text = "This is a sample text generated by an AI language model."
print(text_detector.detect(text))
