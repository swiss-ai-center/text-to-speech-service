import requests as r
import os

url = os.getenv("TTS_API_URL")
tts_endpoint = "/v1/audio/speech"

api_key = os.getenv("TTS_API_KEY")


def tts(json_parameters):
    header = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    rep = r.post(url+tts_endpoint, json=json_parameters, headers=header)
    return rep.content


if __name__ == '__main__':
    rr = tts({"input": "bonjour"})
    print(type(rr))
