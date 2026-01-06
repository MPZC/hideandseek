from flask import Flask, render_template, request, send_file, flash, session, redirect, url_for
from io import BytesIO
from steganography_methods.lsb import Lsb
from steganography_methods.huffman import Huffman
from steganography_methods.random_lsb import RandomLsb
from exceptions import *
import tempfile
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

ALLOWED_EXTENSIONS = {"png"}
MAX_FILE_SIZE_MB = 5

tmp = None  # przechowuje zakodowany obraz w RAM


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def reset_state():
    global tmp
    tmp = None


@app.route("/", methods=["GET", "POST"])
def index():
    global tmp

    # ================== GET ==================
    if request.method == "GET":
        mode = request.args.get("mode", "encode")

        # flaga jednorazowa (znika po refreshu)
        show_encoded = session.pop("encoded_success", False)
        method = session.pop("method", "lsb")

        if not show_encoded:
            reset_state()

        decoded_message = session.pop("decoded_message", None)

        return render_template(
            "index.html",
            processed=show_encoded,
            decoded_message=decoded_message,
            mode=mode,
            method=method
        )

    # ================== POST ==================
    mode = request.form.get("action", "encode")
    method = request.form.get("method", "lsb")

    if "file" not in request.files or request.files["file"].filename == "":
        flash("No file provided.", "error")
        return redirect(url_for("index", mode=mode))

    file = request.files["file"]

    if not allowed_file(file.filename):
        flash("Only .png files allowed.", "error")
        return redirect(url_for("index", mode=mode))

    file.seek(0, os.SEEK_END)
    if file.tell() / (1024 * 1024) > MAX_FILE_SIZE_MB:
        flash(f"File too big! Max size: {MAX_FILE_SIZE_MB} MB.", "error")
        return redirect(url_for("index", mode=mode))
    file.seek(0)

    if method == "lsb":
        stego_method = Lsb()
    elif method == "huffman":
        stego_method = Huffman()
    elif method == "random_lsb":
        stego_method = RandomLsb()
    else:
        flash("Unknown encoding method.", "error")
        return redirect(url_for("index", mode=mode))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_in:
        file.save(tmp_in)
        tmp_in_path = tmp_in.name

    try:
        # -------- ENCODE --------
        if mode == "encode":
            hidden_message = request.form.get("hidden_message", "").strip()
            password = request.form.get("passphrase", "").strip()

            if not hidden_message or not password:
                flash("Message and passphrase cannot be empty.", "error")
                return redirect(url_for("index", mode="encode"))

            stego_img = stego_method.codeMessage(
                tmp_in_path,
                "**" + hidden_message,
                password
            )

            tmp = BytesIO()
            stego_img.save(tmp, format="PNG")
            tmp.seek(0)

            session["encoded_success"] = True
            session["method"] = method

            flash(f"Image encoded correctly using {method.upper()}", "success")
            return redirect(url_for("index", mode="encode"))

        # -------- DECODE --------
        else:
            password = request.form.get("passphrase", "").strip()

            if not password:
                flash("Passphrase can't be empty.", "error")
                return redirect(url_for("index", mode="decode"))

            decoded = stego_method.decodeMessage(tmp_in_path, password).lstrip("*")

            if not decoded.strip():
                decoded = "Nothing was hidden"
                flash("Nothing was hidden", "info")
            else:
                flash(f"Message decoded correctly using {method.upper()}", "success")

            session["decoded_message"] = decoded
            return redirect(url_for("index", mode="decode"))

    except InvalidImageFormat:
        flash("Invalid or corrupted image file.", "error")
        return redirect(url_for("index", mode=mode))

    except MessageTooLarge:
        flash("Image is too small for this message.", "error")
        return redirect(url_for("index", mode=mode))

    except NoHiddenMessage:
        flash("No hidden message found in image.", "info")
        return redirect(url_for("index", mode=mode))

    except InvalidPassword:
        flash("Wrong passphrase.", "error")
        return redirect(url_for("index", mode=mode))
    
    except Exception as e:
        flash(f"Error: {str(e) or 'Unknown error'}", "error")
        return redirect(url_for("index", mode=mode))

    finally:
        try:
            os.remove(tmp_in_path)
        except:
            pass


@app.route("/download")
def download_file():
    global tmp

    if tmp is None:
        flash("No file to download.", "error")
        return redirect(url_for("index", mode="encode"))

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
