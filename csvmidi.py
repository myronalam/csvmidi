import csv
from sys import argv, exit
from midiutil import MIDIFile
# https://midiutil.readthedocs.io/en/1.2.1/index.html?highlight=license#introduction

def main():
    # Check usage, correct # of commmand line args
    if len(argv) != 3:
        print("Usage: python csvmidi.py data.csv outfile")
        exit(1)

    # Get outfile name
    outfile_name = argv[2]
    
    # Import csv file
    # (1) Get column names
    with open(argv[1], "r") as csvhead:
        reader = csv.DictReader(csvhead)
        column_names = reader.fieldnames
    
    # (1a) Check # of series of data
    if len(column_names) > 2:
        print("Sorry, this program only handles 1 time series at this time.")
        exit(2)

    # (2) Create ordered dictionary from CSV
    data = []
    with open(argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)


    # TODO Need error handling to ensure non-numeric values filtered
    values = []
    for row in data:
        values.append(float(row['Value']))
    
    # Linear map from raw data to midi notes #36 (C2) to #96 (C7)
    # y = m(x - x1) + y1
    # Middle C is note #60

    # Change these variable number based on desired range of notes
    low_note = 36 # y1
    high_note = 96 # y2
    min_values = min(values) # x1
    max_values = max(values) # x2
    slope = (high_note - low_note) / (max_values - min_values)

    degrees = [] # list of int (MIDI #)
    for element in values:
        degrees.append(int(round(slope * (element - min_values) + low_note)))
    
    print(degrees)

    midi(degrees, outfile_name)


def midi(degrees, outfile_name):
    print("Midi function called")
    print(outfile_name)
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 90   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(degrees):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    with open(outfile_name, "wb") as output_file:
        MyMIDI.writeFile(output_file)
    
main()