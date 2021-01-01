"""
References:
https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
https://pythonbasics.org/flask-upload-file/
https://www.youtube.com/watch?v=6WruncSoCdI
https://pythonise.com/series/learning-flask/flask-uploading-files
https://hackersandslackers.com/configure-flask-applications/

"""

from os import environ
from flask import Flask, flash, jsonify, redirect, render_template,\
    request, session, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField,\
    SubmitField
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
#import csvmidi
import rawdata

# Configure application
app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Parse data submited using input form
        text_form = request.form.get("formInput")
        formOutput = rawdata.parse(text_form)
        data = formOutput[0]
        columnNames = formOutput[1]

        # Convert values from string to float
        print(f"data = \n{data}\n")
        for row in data:
            for header_index in range(1,len(columnNames)):
                try:
                    row[columnNames[header_index]] = float(row[columnNames[header_index]])
                except ValueError:
                    flash("Invalid data detected. Data must be numerical.")
                    return redirect(request.url)

        print(data)

        return redirect("/sonification")

    else:
        return render_template("index.html")

@app.route("/sonification", methods=["GET", "POST"])
def sonification():
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 4, 8, 16]
    return render_template("sonification.html", x=x, y=y)


"""
----------------------------------------------------------
Code for file uploading - future implementation
----------------------------------------------------------
UPLOAD_FOLDER = "/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["CSV", "TXT"]

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Limit size of upload, 1 MB
app.config["MAX_CONTENT_PATH"] = 1024 * 1024

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def allowed_file(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

def index():
    if request.method == "POST":
        # check if file was submited (might not implement in time)
        if request.files:
            
            data = request.files["file"]
            
            if data.filename == "":
                print("File must have a filename")
                flash("File must have a filename")
                return redirect(request.url)
            
            if not allowed_file(data.filename):
                print("This file extension is not allowed")
                flash("This file extension is not allowed")
                return redirect("/")

            else:
                #filename = secure_filename(data.filename)
                #data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                print("file accepted")
                print(data)
                return redirect("/sonification")
            print(csv)
            return redirect(request.url)


@app.route("/sonification", methods=["GET", "POST"])
def sonification():
    return render_template("sonification.html")


        if "file" not in request.files:
            flash("No file part")
            return redirect("/")
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect("/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return render_template("sonification.html")
            #return redirect(url_for("uploaded_file",
                                    #filename=filename))
"""

if __name__ == "__main__":
    app.run()