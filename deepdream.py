# from deepdreamer.deepdreamer import deepdream
import runpod
import os
import time
import urllib.request

RUNPODKEY = os.getenv("RUNPOD_API_KEY")
runpod.api_key = RUNPODKEY
## load your model(s) into vram here


def handler(event):
    print(event)
    urllib.request.urlretrieve(event.get("input", {}).get("source"), "input.jpg")
    return "Image recieved"


runpod.serverless.start({"handler": handler})
