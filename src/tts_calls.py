import requests as r

url = "https://openai-edge-tts.kube.isc.heia-fr.ch"
tts_endpoint = "/v1/audio/speech"

api_key = "your_api_key_here"


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
