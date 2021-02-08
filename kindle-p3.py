
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

def ExportBookClippings(highlightClips, noteClips):
    """
    Export each book's clips to single text.
    """
    for book in highlightClips:
        if book.find("Instapaper: ") == -1:
            lines = []
            sortedHighlights = {}
            for pos in highlightClips[book]:
                # lines.append(clips[book][pos].encode('utf-8'))
                text = highlightClips[book][pos]
                locationRange = pos
                text = text + " (" + locationRange + ")"
                rangeSplit = locationRange.split("-")
                if book in noteClips:
                    for loc in noteClips[book]:
                        if int(loc) >= int(rangeSplit[0]) and int(loc) <= int(rangeSplit[1]):
                            text = text + "\n\nNOTE: " + noteClips[book][loc] + " (" + loc + ")"

                sortedHighlights[int(rangeSplit[0])] = text
            lines = []
            for position in sorted(sortedHighlights):
                lines.append(sortedHighlights[position])
            filename = os.path.join(OUTPUT_DIR, "%s.md" % book)
            fname = book + ".md"
            f = open(filename,"w")
            f.write("\n\n---\n\n".join(lines))

def SeparateArticleHighlights(highlightClips, noteClips, articleTitles, _articleHighlightClips):
    # create a dictionary of articles
    # return that dictionary
    articleHighlightClips = collections.defaultdict(dict)
    articleHighlightClips.update(_articleHighlightClips)
    # for each book name in articles.json, do stuff, nothing else matters

    for book in articleTitles:
        titleLocations = []
        for titleLocationRange in articleTitles[book]:
            titleLocations.append(titleLocationRange)

        titleLocations = sorted(titleLocations)
        for highlightLocationRange in highlightClips[book]:
            # check location of highlight against the title locations
            found = 0
            for i in range(len(titleLocations)-1):
                # this is where the comparison is happening
                if int(highlightLocationRange.split("-")[1]) >= int(titleLocations[i].split("-")[0]) and int(highlightLocationRange.split("-")[1]) < int(titleLocations[i+1].split("-")[0]):
                    articleTitle = articleTitles[book][titleLocations[i]]
                    articleHighlightClips[articleTitle][highlightLocationRange] = highlightClips[book][highlightLocationRange]
                    found = 1
            if found == 0:
                articleTitle = articleTitles[book][titleLocations[len(titleLocations)-1]]
                articleHighlightClips[articleTitle][highlightLocationRange] = highlightClips[book][highlightLocationRange]
    return articleHighlightClips
            
def SeparateArticleNotes(highlightClips, noteClips, articleTitles, _articleNoteClips):
    # create a dictionary of articles
    # return that dictionary
    articleNoteClips = collections.defaultdict(dict)
    articleNoteClips.update(_articleNoteClips)
    # for each book name in articles.json, do stuff, nothing else matters

    for book in articleTitles:
        titleLocations = []
        for titleLocationRange in articleTitles[book]:
            titleLocations.append(titleLocationRange)

        titleLocations = sorted(titleLocations)
        for noteLocationRange in noteClips[book]:
            # check location of highlight against the title locations
            found = 0
            for i in range(len(titleLocations)-1):
                # this is where the comparison is happening
                if int(noteLocationRange) >= int(titleLocations[i].split("-")[0]) and int(noteLocationRange) < int(titleLocations[i+1].split("-")[0]):
                    articleTitle = articleTitles[book][titleLocations[i]]
                    articleNoteClips[articleTitle][noteLocationRange] = noteClips[book][noteLocationRange]
                    found = 1
            if found == 0:
                articleTitle = articleTitles[book][titleLocations[len(titleLocations)-1]]
                articleNoteClips[articleTitle][noteLocationRange] = noteClips[book][noteLocationRange]
    return articleNoteClips

def main():
    highlightClips = collections.defaultdict(dict)
    highlightClips.update(LoadHighlightClips())

    noteClips = collections.defaultdict(dict)
    noteClips.update(LoadNoteClips())

    articleTitles = collections.defaultdict(dict)
    articleTitles.update(LoadArticleTitles())

    articleHighlightClips = collections.defaultdict(dict)
    articleNoteClips = collections.defaultdict(dict)
    
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

    ExportBookClippings(highlightClips, noteClips)
    
    articleHighlightClips = SeparateArticleHighlights(highlightClips, noteClips, articleTitles, articleHighlightClips)
    articleNoteClips = SeparateArticleNotes(highlightClips, noteClips, articleTitles, articleNoteClips)


main()