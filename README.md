# csvmidi
## CSV to MIDI - CS50x Final Project Introduction

The goal of this project is to allow a user to convert a CSV file to a MIDI file in order to hear a sound. This program is inspired by two episodes of the Marketplace radio program, when Kai Ryssdal spoke with the information science Ph.D student Jordan Wirfs-Brock to hear a "sonification" of the [rising unemployment](https://www.marketplace.org/2020/06/24/heres-what-the-crescendo-of-unemployment-sounds-like/) and [volatily of the stock market](https://www.marketplace.org/2020/03/31/the-sounds-of-a-volatile-stock-market/) during the COVID-19 pandemic.  One of my interests is in music, so I decided use this as a theme to explore in this project.

## How to Use

As of Nov 8, 2020, `csvmidi.py` is only functional via command line in a terminal. The way to run the program is:

```
python csvmidi.py data.csv outfile.mid
```
where:
- `data.csv` is the input CSV file
- `outfile.mid` is the output MIDI file

Each data series is written as a separate MIDI track from left to right.

CSV file assumptions:
- The first column of data is a timestamp
- Subsequent column(s) are data series
- Each element in the data series is not null

Python Package Requirements:
- [MIDIUtil](https://midiutil.readthedocs.io/en/1.2.1/index.html)


## TODO list
These tasks will be refined as I encounter challenges beyond my current abilities.  After all, this project is expected to take the amount of effort as 2 problem sets in the course.  From my time spent on the previous assignments, I would imagine this project taking at least 24 hours of development time.

I envision the following tasks will need to be completed to have a web app I can deploy:
- [ ] Create python script to use MIDIUtil for generating MIDI files from CSV input
    - [x] Basic command line operation takes CSV input
    - [ ] Error checking of CSV file
    - [ ] Add some ability to modify parameters (tempo, time)
- [ ] Configure web server to run python with MIDIUtil installed and flask to serve webpage
- [ ] Create front end webpage for User Interface
- [ ] Figure out file uploads, error checking, size limits
- [ ] Implement (static) data visualization using Plotly

Nice to have:
- [ ] Maybe allow user to pick a key
- [ ] Consider 3rd party authentication for storing data
- [ ] Tie project back to the Marketplace inspriation by connecting to the public data API provided by the Bureau of Labor Statistics

