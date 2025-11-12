from flask import Flask, render_template, request, send_file, flash
from io import BytesIO
from werkzeug.utils import secure_filename
from steganography_methods.lsb import Lsb
from PIL import Image
import tempfile
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

ALLOWED_EXTENSIONS = {"png"}
MAX_FILE_SIZE_MB = 5

# przechowywanie obrazu w pamięci
tmp = None
processed = False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def clear_tmp_before_request():
    """Czyści bufor przed nowym żądaniem GET (z wyjątkiem /download)."""
    global tmp, processed
    if request.method == "GET" and request.endpoint not in ["download_file", "static"]:
        tmp = None
        processed = False


@app.route("/", methods=["GET", "POST"])
def index():
    global tmp, processed
    decoded_message = None
    processed = False
    mode = "encode"

    if request.method == "POST":
        action = request.form.get("action")
        mode = action

        if "file" not in request.files:
            flash("No file", "error")
            return render_template("index.html", decoded_message=decoded_message, processed=processed, mode=mode)

        file = request.files["file"]
        if file.filename == "":
            flash("No file", "error")
            return render_template("index.html", decoded_message=decoded_message, processed=processed, mode=mode)

        if file and allowed_file(file.filename):
            file.seek(0, os.SEEK_END)
            file_size = file.tell() / (1024 * 1024)
            file.seek(0)
            if file_size > MAX_FILE_SIZE_MB:
                flash(f"File too big! Max size: {MAX_FILE_SIZE_MB} MB.", "error")
                return render_template("index.html", decoded_message=decoded_message, processed=processed, mode=mode)

            lsb = Lsb()

            try:
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_in:
                    file.save(tmp_in)
                    tmp_in_path = tmp_in.name

                if action == "encode":
                    hidden_message = request.form.get("hidden_message", "").strip()
                    if not hidden_message:
                        flash("Message con't be empty", "error")
                        os.remove(tmp_in_path)
                        return render_template("index.html", decoded_message=decoded_message, processed=processed, mode=mode)

                    hidden_message = "**" + hidden_message
                    stego_img = lsb.codeMessageLSB(tmp_in_path, hidden_message)

                    tmp = BytesIO()
                    stego_img.save(tmp, format="PNG")
                    tmp.seek(0)
                    processed = True

                    flash("Image encoded correctly", "success")
                    os.remove(tmp_in_path)

                elif action == "decode":
                    decoded_message = lsb.decodeMessageLSB(tmp_in_path).lstrip("*")

                    if not decoded_message.strip():
                        decoded_message = "Nothing was hidden"
                        flash("Nothing was hidden", "info")
                    else:
                        flash("Message decoded correctly.", "success")

                    os.remove(tmp_in_path)


            except Exception as e:
                try:
                    os.remove(tmp_in_path)
                except Exception:
                    pass
                error_message = str(e) if str(e).strip() else "Unknown decoding error"
                flash(f"Error: {error_message}", "error")

        else:
            flash("Only .png files allowed.", "error")

    return render_template("index.html",
                           decoded_message=decoded_message,
                           processed=processed,
                           mode=mode)


@app.route("/download")
def download_file():
    global tmp
    if tmp is None:
        flash("No file to download", "error")
        return render_template("index.html")
    tmp.seek(0)
    return send_file(
        tmp,
        mimetype="image/png",
        as_attachment=True,
        download_name="stego_image.png"
    )


if __name__ == "__main__":
    tmp = None
    processed = False
    port = 8080
    app.run(debug=True, host="0.0.0.0", port=port)