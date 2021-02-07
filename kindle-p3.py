
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

def SaveHighlightClips(highlightClips):
    """
    Save new highlights to HIGHLIGHT_FILE
    """
    f = open(HIGHLIGHT_FILE, "w")
    json.dump(highlightClips, f)

def SaveNoteClips(noteClips):
    """
    Save new clips to NOTE_FILE
    """
    f = open(NOTE_FILE, "w")
    json.dump(noteClips, f)

def SaveArticleTitles(articleTitles):
    """
    Save new clips to NOTE_FILE
    """
    f = open(ARTICLE_FILE, "w")
    json.dump(articleTitles, f)

def LoadHighlightClips():
    """
    Load previous clips from HIGHLIGHT_FILE
    """
    try:
        with open(HIGHLIGHT_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}

def LoadNoteClips():
    """
    Load previous clips from NOTE_FILE
    """
    try:
        with open(NOTE_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}

def LoadArticleTitles():
    """
    Load previous clips from NOTE_FILE
    """
    try:
        with open(ARTICLE_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}

def FindArticleTitles(highlightClips, noteClips, articleTitles):
    titleLocations = []
    # title_dic = {}
    for book in noteClips:
        
        if book.find("Instapaper: ") != -1:
            for location in noteClips[book]:
                if noteClips[book][location] == ".Title.":
                    titleLocations.append(location)
                    if book in articleTitles:
                        null = 0
                    else:
                        articleTitles[book] = {}
                    for position in highlightClips[book]:
                        locationRange = position
                        splitRange = locationRange.split("-")
                        if int(location) >= int(splitRange[0]) and int(location) <= int(splitRange[1]):
                            title = highlightClips[book][position]
                            articleTitles[book][locationRange] = title

    return articleTitles

def main():
    highlightClips = collections.defaultdict(dict)
    highlightClips.update(LoadHighlightClips())

    noteClips = collections.defaultdict(dict)
    noteClips.update(LoadNoteClips())

    articleTitles = collections.defaultdict(dict)
    articleTitles.update(LoadArticleTitles())
    
    clippings = SplitClippings('My Clippings test.txt')

    for clipping in clippings:
        highlightClip = GetHighlightClip(clipping)
        noteClip = GetNoteClip(clipping)

        if highlightClip:
            highlightClips[highlightClip['book']][(highlightClip['position'])] = highlightClip['content']
        
        if noteClip:
            noteClips[noteClip['book']][(noteClip['position'])] = noteClip['content']

    # remove key with empty value
    highlightClips = {k: v for k, v in highlightClips.items() if v}
    noteClips = {x: y for x, y in noteClips.items() if y}

    SaveHighlightClips(highlightClips)
    SaveNoteClips(noteClips)

    articleTitles = FindArticleTitles(highlightClips, noteClips, articleTitles)
    SaveArticleTitles(articleTitles)


main()