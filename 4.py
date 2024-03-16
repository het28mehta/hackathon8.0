import os
import math
import requests

class AITextDetector:
    def _init_(self, token):
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(token),
        }

    def detect_text(self, text):
        data = {
            "prompt": text + ".\n<|disc_score|>",
            "max_tokens": 1,
            "temperature": 1,
            "top_p": 1,
            "n": 1,
            "logprobs": 5,
            "stop": "\n",
            "stream": False,
            "model": "model-detect-v2",
        }
        response = requests.post(
            "https://api.openai.com/v1/completions", headers=self.header, json=data
        )
        if response.status_code == 200:
            choices = response.json()["choices"][0]
            key_prob = choices["logprobs"]["top_logprobs"][0]["!"] or -10
            prob = math.exp(key_prob)
            e = 100 * (1 - (prob or 0))
            if e <= 10:
                return {"AI-Generated Probability": e, "Verdict": "Very unlikely"}
            elif e <= 45:
                return {"AI-Generated Probability": e, "Verdict": "Unlikely"}
            elif e <= 90:
                return {"AI-Generated Probability": e, "Verdict": "Possibly"}
            elif e <= 98:
                return {"AI-Generated Probability": e, "Verdict": "Likely"}
            else:
                return {"AI-Generated Probability": e, "Verdict": "Very likely"}
        else:
            return "Error: {0}".format(response.status_code)

    def detect_code(self, code):
        data = {
            "prompt": "" + code + "\n<|disc_score|>",
            "max_tokens": 1,
            "temperature": 1,
            "top_p": 1,
            "n": 1,
            "logprobs": 5,
            "stop": "\n",
            "stream": False,
            "model": "code-davinci-002",
        }
        response = requests.post(
            "https://api.openai.com/v1/completions", headers=self.header, json=data
        )
        if response.status_code == 200:
            choices = response.json()["choices"][0]
            key_prob = choices["logprobs"]["top_logprobs"][0]["!"] or -10
            prob = math.exp(key_prob)
            e = 100 * (1 - (prob or 0))
            if e <= 10:
                return {"AI-Generated Probability": e, "Verdict": "Very unlikely"}
            elif e <= 45:
                return {"AI-Generated Probability": e, "Verdict": "Unlikely"}
            elif e <= 90:
                return {"AI-Generated Probability": e, "Verdict": "Possibly"}
            elif e <= 98:
                return {"AI-Generated Probability": e, "Verdict": "Likely"}
            else:
                return {"AI-Generated Probability": e, "Verdict": "Very likely"}
        else:
            return "Error: {0}".format(response.status_code)

app = Flask(_name_)

@app.route("/detect", methods=["POST"])
def detect_ai_text():
    if "text" in request.json:
        text = request.json["text"]
        detector = AITextDetector(os.environ["OPENAI_API_KEY"])
        if "code" in request.json:
            code = request.json["code"]
            result = detector.detect_code(code)
        else:
            result = detector.detect_text(text)
        return result
    else:
        return "Error: Missing 'text' parameter"

if _name_ == "_main_":
    app.run(debug=True)