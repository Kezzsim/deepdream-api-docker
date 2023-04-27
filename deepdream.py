# from deepdreamer.deepdreamer import deepdream
import runpod
from imgurpython import ImgurClient
import pathlib 
import os
import time
import urllib.request

RUNPODKEY = os.getenv("RUNPOD_API_KEY")
IMGURCLIENT_ID = os.getenv("IMGURCLIENT_ID")
IMGURCLIENT_SECRET = os.getenv("IMGURCLIENT_SECRET")
runpod.api_key = RUNPODKEY
## load your model(s) into vram here

client = ImgurClient(IMGURCLIENT_ID, IMGURCLIENT_SECRET)

def handler(event):
    print(event)
    urllib.request.urlretrieve(event.get("input", {}).get("source"), "input.jpg")
    upload = client.upload_from_path(os.path.abspath("input.jpg"), config=None, anon=True)
    return upload


runpod.serverless.start({"handler": handler})
