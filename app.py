"""
References:
https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
https://pythonbasics.org/flask-upload-file/
https://www.youtube.com/watch?v=6WruncSoCdI
https://pythonise.com/series/learning-flask/flask-uploading-files
https://hackersandslackers.com/configure-flask-applications/

"""
import os
from os import environ
from flask import Flask, flash, jsonify, redirect, render_template,\
    request, session, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField,\
    SubmitField
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from midiutil import MIDIFile
import rawdata

# Configure application
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

app.secret_key = environ.get('SECRET_KEY')

@app.route("/", methods=["GET", "POST"])
def index():
    session['data2sound'] = []
    session['columns'] = []

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
        
        # Transfer this stuff to sonification route
        session['data2sound'] = data
        session['columns'] = columnNames

        return redirect("/sonification")

    else:
        return render_template("index.html")

@app.route("/sonification", methods=["GET", "POST"])
def sonification():
    data2sound = session['data2sound']
    columnNames = session['columns']

    # variables to feed into csvmidi.py and scatter plot
    x = [] 
    y = [] # list of floats

    for row in data2sound:
        for column_index in range(1,len(columnNames)):
            y.append(row[columnNames[column_index]])

    # Generate x-axis intervals
    for i in range(len(y)):
        x.append(i)

    # ---------------- Generate MIDI file ---------------------
    values = y
    # Change these variable number based on desired range of notes
    low_note = 36 # y1
    high_note = 96 # y2
    min_values = min(values) # x1
    max_values = max(values) # x2
    slope = (high_note - low_note) / (max_values - min_values)

    degrees = [] # list of int (MIDI note #)
    for element in values:
        degrees.append(int(round(slope * (element - min_values) + low_note)))

    
    # (1) preferences
    track    = 0
    channel  = 0
    time     = 0   # In beats
    duration = 1   # In beats
    tempo    = 90  # In BPM
    volume   = 100 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                        # automatically created)
    MyMIDI.addTempo(track,time,tempo)

    for pitch in degrees:
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        time = time + 1

    with open("static/midi/sonification.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

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