from flask import Flask, render_template, request, send_file, flash, session, redirect, url_for
from io import BytesIO
from werkzeug.utils import secure_filename
from steganography_methods.lsb import Lsb
from steganography_methods.huffman import Huffman
from steganography_methods.random_lsb import RandomLsb
from PIL import Image
import tempfile
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

ALLOWED_EXTENSIONS = {"png"}
MAX_FILE_SIZE_MB = 5

tmp = None
processed = False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def reset_state():
    """Czyści stan aplikacji."""
    global tmp, processed
    tmp = None
    processed = False


@app.route("/", methods=["GET", "POST"])
def index():
    global tmp, processed

    # ------------------ GET ------------------
    if request.method == "GET":
        mode = request.args.get("mode", "encode")
        reset_state()
        session["mode"] = mode
        return render_template(
            "index.html",
            decoded_message=None,
            processed=False,
            mode=mode,
            method="lsb"
        )

    # ------------------ POST ------------------
    decoded_message = None
    processed = False

    mode = request.form.get("action", "encode")
    method = request.form.get("method", "lsb")

    # przełączenie trybu
    previous_mode = session.get("mode")
    session["mode"] = mode
    if previous_mode and previous_mode != mode:
        reset_state()

    # walidacja przesłanego pliku
    if "file" not in request.files:
        flash("No file provided.", "error")
        return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

    file = request.files["file"]
    if file.filename == "":
        flash("No file provided.", "error")
        return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

    if file and allowed_file(file.filename):

        # kontrola rozmiaru
        file.seek(0, os.SEEK_END)
        file_size = file.tell() / (1024 * 1024)
        file.seek(0)
        if file_size > MAX_FILE_SIZE_MB:
            flash(f"File too big! Max size: {MAX_FILE_SIZE_MB} MB.", "error")
            return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

        # wybór klasy kodującej
        if method == "lsb":
            stego_method = Lsb()
        elif method == "huffman":
            stego_method = Huffman()
        elif method == "random_lsb":
            stego_method = RandomLsb()
        else:
            flash("Unknown encoding method selected.", "error")
            return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

        try:
            # zapisujemy przesłany plik do pliku tymczasowego
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_in:
                file.save(tmp_in)
                tmp_in_path = tmp_in.name

            # --------------------- ENCODE ---------------------
            if mode == "encode":
                hidden_message = request.form.get("hidden_message", "").strip()
                password = request.form.get("passphrase", "").strip()

                if not hidden_message:
                    flash("Message can't be empty", "error")
                    os.remove(tmp_in_path)
                    return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

                if not password:
                    flash("Passphrase can't be empty", "error")
                    os.remove(tmp_in_path)
                    return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

                hidden_message = "**" + hidden_message  # prefix dla LSB

                # kodowanie obrazka odpowiednią metodą
                stego_img = stego_method.codeMessage(tmp_in_path, hidden_message, password)

                # zapis stego jako PNG do pamięci
                tmp = BytesIO()
                stego_img.save(tmp, format="PNG")
                tmp.seek(0)
                processed = True

                flash(f"Image encoded correctly using {method.upper()}", "success")
                os.remove(tmp_in_path)

            # --------------------- DECODE ---------------------
            elif mode == "decode":
                password = request.form.get("passphrase", "").strip()

                if not password:
                    flash("Passphrase can't be empty", "error")
                    os.remove(tmp_in_path)
                    return render_template("index.html", decoded_message=None, processed=False, mode=mode, method=method)

                decoded_message = stego_method.decodeMessage(tmp_in_path, password)
                decoded_message = decoded_message.lstrip("*")

                if not decoded_message.strip():
                    decoded_message = "Nothing was hidden"
                    flash("Nothing was hidden", "info")
                else:
                    flash(f"Message decoded correctly using {method.upper()}", "success")

                os.remove(tmp_in_path)

        except Exception as e:
            try:
                os.remove(tmp_in_path)
            except:
                pass

            error_message = str(e) if str(e).strip() else "Unknown error"
            flash(f"Error: {error_message}", "error")

    else:
        flash("Only .png files allowed.", "error")

    return render_template(
        "index.html",
        decoded_message=decoded_message,
        processed=processed,
        mode=mode,
        method=method
    )


@app.route("/download")
def download_file():
    global tmp
    if tmp is None:
        flash("No file to download", "error")
        return redirect(url_for("index", mode=session.get("mode", "encode")))

    tmp.seek(0)
    return send_file(
        tmp,
        mimetype="image/png",
        as_attachment=True,
        download_name="stego_image.png"
    )


if __name__ == "__main__":
    reset_state()
    app.run(debug=True, host="0.0.0.0", port=8080)
