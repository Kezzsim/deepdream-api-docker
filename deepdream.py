import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from deepdreamer.deepdreamer import deepdream
from PIL import Image

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            # TODO: transform to .jpg if not jpg
            if not filename.endswith(".jpg") or filename.endswith(".jpeg"):
                print("Converting to .jpg");
                input_im = Image.open(filepath);
                output_im = input_im.convert('RGB');
                filename = "{}.jpg".format(filename.rsplit(".", 1)[0]);
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename);
                output_im.save(filepath);
                print("New Filepath: {}".format(filepath));

            # Get parameters from form request
            zoom = request.form.get("zoom", True);
            scale = request.form.get("scale", 0.05);
            itern = request.form.get("itern", 10);
            octaves = request.form.get("octaves", 4);
            octave_scale = request.form.get("octave-scale", 1.4);
            layers = request.form.get("layers", "inception_4c/output");
            clip = request.form.get("clip", True);
            network = request.form.get("network", "bvlc_googlenet");
            # run deep dream
            deepdream(filepath, zoom, scale, 1, itern, octaves, octave_scale, layers, clip, network)
            # Return generated deep dream image
            outputFilepath = os.path.join(
                app.config["UPLOAD_FOLDER"], "{}_0.jpg".format(filename)
            )
            return send_file(outputFilepath, mimetype="image/jpg")
    return """
    <!doctype html>
    <style>
    /* container */
    .responsive-two-column-grid {
        display:block;
    }
    /* columns */
    .responsive-two-column-grid > * {
        padding:0rem;
    }
    /* tablet breakpoint */
    @media (min-width:768px) {
        .responsive-two-column-grid {
            display: grid;
            grid-template-columns: 0.1fr 1fr;
        }
    }
    </style>
    <title>DeepDream</title>
    <h1>Upload new File to DeepDream</h1>
    <h3>(.jpg only for now)</h3>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <br>
      <div class="responsive-two-column-grid">
        <div><label for="zoom">Zoom: </label></div>
        <div><input type="checkbox" id="zoom" name="zoom" checked></div>
        <div><label for="scale">Scale: </label></div>
        <div><input type="number" id="scale" value="0.05" /></div>
        <div><label for="itern">iterations: </label></div>
        <div><input type="number" id="itern" value="10" /></div>
        <div><label for="octaves">Octaves: </label></div>
        <div><input type="number" id="octaves" value="4" /></div>
        <div><label for="octave-scale">Octave-scale: </label></div>
        <div><input type="number" id="octave-scale" value="1.4" step="0.1" /></div>
        <div><label for="layers">Layers: </label></div>
        <div><input type="text" id="layers" name="layers" value="inception_4c/output" /></div>
        <div><label for="clip">Clip: </label></div>
        <div><input type="checkbox" id="clip" name="clip" checked></div>
        <div><label for="network">Network:</label></div>
        <div><select name="network" id="network">
        <option value="bvlc_googlenet">bvlc_googlenet</option>
        <option value="googlenet_place205">googlenet_place205</option>
        </select></div>
      </div>
      <br>
      <input type=submit value=Upload>
    </form>
    """
