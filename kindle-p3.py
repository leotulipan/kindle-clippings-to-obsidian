
import collections
import json
import re
import os

BOUNDARY = "\n==========\n"
OUTPUT_DIR = "output"
HIGHLIGHT_FILE = "highlights.json"
NOTE_FILE = "notes.json"
ARTICLE_FILE = "articles.json"

def SplitClippings(filename):
    f = open(filename, "r")
    content = f.read()
    content = content.replace('\ufeff', '')
    return content.split(BOUNDARY)

def GetHighlightClip(clipping):
    highlightClip = {}

    lines = [l for l in clipping.split('\n') if l]
    
    # return if not a clipping
    if len(lines) != 3:
        return
    
    # return if not a highlight
    if lines[1].find("- Your Highlight") == -1:
        return
    
    highlightClip['book'] = lines[0]
    match = re.search('(\d+)-\d+', lines[1]) # searching for a range of numbers
    if not match:
        return
    
    # get the range of location
    position = match.group(0)

    # clip['position'] = int(position)
    highlightClip['position'] = position
    highlightClip['content'] = lines[2]

    return highlightClip

def GetNoteClip(clipping):
    noteClip = {}

    lines = [l for l in clipping.split('\n') if l]
    
    # return if not a clip
    if len(lines) != 3:
        return
    
    # return if not a note
    if lines[1].find("- Your Note") == -1:
        return

    noteClip['book'] = lines[0]

    # find all numbers in line after substring 'Location', pick the first one at the location
    line = lines[1]
    index = line.find('Location')
    newLine = line[index:len(line)-1]
    numbers = [int(s) for s in newLine.split() if s.isdigit()]
    position = numbers[0]

    noteClip['position'] = str(position)
    noteClip['content'] = lines[2]

    return noteClip

def main():
    highlightClips = collections.defaultdict(dict)
    noteClips = collections.defaultdict(dict)
    clippings = SplitClippings('My Clippings test.txt')

    for clipping in clippings:
        highlightClip = GetHighlightClip(clipping)
        noteClip = GetNoteClip(clipping)

        if highlightClip:
            highlightClips[highlightClip['book']][(highlightClip['position'])] = highlightClip['content']
        
        if noteClip:
            noteClips[noteClip['book']][(noteClip['position'])] = noteClip['content']

    print(highlightClips)
    print(noteClips)

main()