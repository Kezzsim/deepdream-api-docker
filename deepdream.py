# from deepdreamer.deepdreamer import deepdream
import runpod
from imgurpython import ImgurClient
from deepdreamer.deepdreamer import deepdream
import pathlib
import os
import time
import urllib.request

## RUNPODKEY = os.getenv("RUNPOD_API_KEY")
IMGURCLIENT_ID = os.getenv("IMGURCLIENT_ID")
IMGURCLIENT_SECRET = os.getenv("IMGURCLIENT_SECRET")
## runpod.api_key = RUNPODKEY
## load your model(s) into vram here

client = None
## Output option 1 : Imgur Client
if IMGURCLIENT_ID is not None and IMGURCLIENT_SECRET is not None:
    client = ImgurClient(IMGURCLIENT_ID, IMGURCLIENT_SECRET)


def handler(event):
    ## introspect the event
    print(event)

    ## Step 1 : Set Deep Dream parameters (With defaults or JSON)
    zoom = event.get("input", {}).get("zoom", True)
    scale = event.get("input", {}).get("scale", 0.05)
    itern = event.get("input", {}).get("itern", 10)
    octaves = event.get("input", {}).get("octaves", 4)
    octave_scale = event.get("input", {}).get("octave-scale", 1.4)
    layers = event.get("input", {}).get("layers", "inception_4c/output")
    clip = event.get("input", {}).get("clip", True)
    network = event.get("input", {}).get("network", "bvlc_googlenet")

    ## Step 2 : Download from URL
    urllib.request.urlretrieve(event.get("input", {}).get("source"), "input.jpg")

    ## Step 3 : Run Deep Dream
    deepdream(
        os.path.abspath("input.jpg"),
        zoom,
        scale,
        1,
        itern,
        octaves,
        octave_scale,
        layers,
        clip,
        network,
    )

    ## Confirm output file
    print(os.listdir(os.curdir))
    
    ## Option 1 : Upload to Imgur
    if client is not None:
        upload = client.upload_from_path(
            os.path.abspath("input_0.jpg"), config=None, anon=True
        )
        return upload
    else:
        return "No output option specified. Result generated sucessfully but was not saved."


runpod.serverless.start({"handler": handler})
