from flask import Flask, render_template, request, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from steganography_methods.lsb import Lsb

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/img"
ALLOWED_EXTENSIONS = {"png"}
MAX_FILE_SIZE_MB = 5
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    processed_filename = None
    decoded_message = None

    if request.method == "POST":
        action = request.form.get("action")
        if "file" not in request.files:
            flash("Nie wybrano pliku.")
            return render_template("index.html")

        file = request.files["file"]
        if file.filename == "":
            flash("Nie wybrano pliku.")
            return render_template("index.html")

        if file and allowed_file(file.filename):
            file.seek(0, os.SEEK_END)
            file_size = file.tell() / (1024 * 1024)
            file.seek(0)
            if file_size > MAX_FILE_SIZE_MB:
                flash(f"Plik jest za duży! Maksymalny rozmiar: {MAX_FILE_SIZE_MB} MB.")
                return render_template("index.html")

            #Saving file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            lsb = Lsb()

            try:
                if action == "encode":
                    hidden_message = request.form.get("hidden_message", "").strip()
                    if not hidden_message:
                        flash("Wiadomość nie może być pusta!")
                        return render_template("index.html")

                    hidden_message = "**" + hidden_message  # prefix for decoding
                    stego_img = lsb.codeMessageLSB(filepath, hidden_message)
                    processed_filename = f"stego_{filename.rsplit('.',1)[0]}.png"
                    stego_img.save(os.path.join(app.config["UPLOAD_FOLDER"], processed_filename), format="PNG")
                    flash("Obraz został zakodowany pomyślnie.")

                elif action == "decode":
                    decoded_message = lsb.decodeMessageLSB(filepath)
                    flash("Wiadomość została odczytana pomyślnie.")
            except Exception as e:
                flash(f"Błąd: {str(e)}")

        else:
            flash("Dozwolone są tylko pliki .png.")

    return render_template("index.html",
                           processed_filename=processed_filename,
                           decoded_message=decoded_message)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
