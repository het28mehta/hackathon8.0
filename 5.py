import pydub
from pydub.silence import split_on_silence
import numpy as np
import math

# Define the AIAudioDetector class
class AIAudioDetector:
    def __init__(self):
        self.threshold = 10

    def detect(self, audio_file):
        # Load the audio file
        audio = pydub.AudioSegment.from_file(audio_file, format=audio_file.split(".")[-1])

        # Split the audio into chunks based on silence
        chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=self.threshold)

        # Calculate the zero-crossing rate (ZCR) for each chunk
        zcrs = [self._zcr(chunk) for chunk in chunks]

        # Calculate the mean and standard deviation of the ZCRs
        mean_zcr = np.mean(zcrs)
        std_zcr = np.std(zcrs)

        # Calculate the probability of the audio being AI-generated
        prob = self._probability(zcrs, mean_zcr, std_zcr)
        # Return the probability and a verdict based on the probability
        if prob < 0.5:
            verdict = "Probably not AI-generated"
        elif prob < 0.8:
            verdict = "Possibly AI-generated"
        else:
            verdict = "Probably AI-generated"
        return {"Probability": prob, "Verdict": verdict}

    def _zcr(self, audio):
        # Calculate the zero-crossing rate (ZCR) of the audio
        zero_crossings = sum(abs(np.diff(np.sign(audio.get_array_of_samples()))) / 2)
        return zero_crossings / audio.duration_seconds

    def _probability(self, data, mean, std):
        # Calculate the probability of the data given the mean and standard deviation
        variance = std ** 2
        numerator = math.exp(-((np.mean(data) - mean) ** 2) / (2 * variance))
        denominator = math.sqrt(2 * math.pi * variance)
        prob = numerator / denominator
        return prob

# Initialize the AIAudioDetector
audio_detector = AIAudioDetector()

# Test the AIAudioDetector
audio_file = "path/to/your/audio/file.wav"
print(audio_detector.detect(audio_file))
