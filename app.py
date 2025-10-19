from flask import Flask, render_template, request, send_from_directory, flash
import os
from steganography_methods.temp_file import convert_to_blackwhite
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"  #getting this key should be secured somehow

#Settings
UPLOAD_FOLDER = "static/img"
ALLOWED_EXTENSIONS = {"png"}
MAX_FILE_SIZE_MB = 5  #max 5 MB
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    processed_filename = None

    if request.method == "POST":
        if "file" not in request.files:
            flash("Nie wybrano pliku.")
            return render_template("index.html")

        file = request.files["file"]

        if file.filename == "":
            flash("Nie wybrano pliku.")
            return render_template("index.html")

        if file and allowed_file(file.filename):
            #checking Mb limits
            file.seek(0, os.SEEK_END)
            file_size = file.tell() / (1024 * 1024)
            file.seek(0)
            if file_size > MAX_FILE_SIZE_MB:
                flash(f"Plik jest za duży! Maksymalny rozmiar: {MAX_FILE_SIZE_MB} MB.")
                return render_template("index.html")

            #Saving file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            #Black and white conversion
            processed_filename = convert_to_blackwhite(filepath, app.config["UPLOAD_FOLDER"])

            if processed_filename:
                flash("Obraz został przetworzony pomyślnie.")
            else:
                flash("Błąd podczas przetwarzania obrazu.")
        else:
            flash("Dozwolone są tylko pliki .png.")

    return render_template("index.html", processed_filename=processed_filename)


@app.route("/download/<filename>")
def download_file(filename):
    """Allows to download the file"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
