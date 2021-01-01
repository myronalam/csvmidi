# Original command-line version of the program

import csv
from sys import argv, exit
from midiutil import MIDIFile
# https://midiutil.readthedocs.io/en/1.2.1/index.html?highlight=license#introduction

def main():
"""
Code here for command line operation.
    # Check usage, correct # of commmand line args
    if len(argv) != 3:
        print("Usage: python csvmidi.py data.csv outfile.mid")
        exit(1)
    # Get outfile name
    outfile_name = argv[2]
    
"""



    # Import csv file
    # (1) Get column names
    with open(argv[1], "r") as csvhead:
        reader = csv.DictReader(csvhead)
        column_names = reader.fieldnames
    
    # (1a) Check # of series of data
    # Assumptions: Col1 = Timestamp, Col2, 3, etc are Data Series
    """ Uncomment to impose restrictions on number of columns
    if len(column_names) > 4:
        print("Sorry, only 4 time series are supported at this time.")
        exit(2)
    """

    # (2) Create ordered dictionary from CSV
    data = []
    with open(argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Dictonary to store lists of scale degrees
    score = {}
    for track in range(len(column_names)-1):
        
        # TODO Need error handling to ensure non-numeric values filtered
        values = [] # list of floats
        for row in data:
            values.append(float(row[column_names[track + 1]]))
        
        # Linear map from raw data to MIDI notes #36 (C2) to #96 (C7)
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
                
        score[track] = degrees

    #print(score)
    
    # Create number of tracks equal to num of CSV series inputed
    MyMIDI = MIDIFile(len(column_names) - 1)

    for track in score:
        midi(MyMIDI, score[track], track)
    
    # Output MIDI file
    with open(outfile_name, "wb") as output_file:
        MyMIDI.writeFile(output_file)
    

def midi(MyMIDI, degrees, track):
    print(f"Midi function called, writing track #{track}")
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 90   # In BPM
    volume   = 110  # 0-127, as per the MIDI standard

    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(degrees):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
    
main()