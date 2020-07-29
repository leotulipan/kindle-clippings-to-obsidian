#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os
import re

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"output"
HIGHLIGHT_FILE = u"highlights.json"
NOTE_FILE = u"notes.json"
ARTICLE_FILE = u"articles.json"

def get_sections(filename):
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_highlight_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return
    # position = match.group(1)
    position = match.group(0)

    # clip['position'] = int(position)
    clip['position'] = position
    clip['content'] = lines[2]

    return clip

def get_note_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    match = re.search('- Your Note on', lines[1])
    if not match:
        return
    line = lines[1]
    index = line.find('Location')
    new_line = line[index:len(line)-1]
    numbers = [int(s) for s in new_line.split() if s.isdigit()]
    position = numbers[0]

    clip['position'] = position
    clip['content'] = lines[2]

    return clip


def export_txt(clips):
    """
    Export each book's clips to single text.
    """
    for book in clips:
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos].encode('utf-8'))

        filename = os.path.join(OUTPUT_DIR, u"%s.md" % book)
        with open(filename, 'wb') as f:
            f.write("\n\n---\n\n".join(lines))


def load_highlight_clips():
    """
    Load previous clips from HIGHLIGHT_FILE
    """
    try:
        with open(HIGHLIGHT_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}

def load_note_clips():
    """
    Load previous clips from NOTE_FILE
    """
    try:
        with open(NOTE_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def save_highlight_clips(clips):
    """
    Save new clips to HIGHLIGHT_FILE
    """
    with open(HIGHLIGHT_FILE, 'wb') as f:
        json.dump(clips, f)

def save_note_clips(clips):
    """
    Save new clips to NOTE_FILE
    """
    with open(NOTE_FILE, 'wb') as f:
        json.dump(clips, f)


def main():
    # for highlights
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_highlight_clips())

    n_clips = collections.defaultdict(dict)
    n_clips.update(load_note_clips())
    # extract clips
    sections = get_sections(u'My Clippings.txt')
    for section in sections:
        clip = get_highlight_clip(section)
        if clip:
            clips[clip['book']][str(clip['position'])] = clip['content']
        
        n_clip = get_note_clip(section)
        if n_clip:
            n_clips[n_clip['book']][str(n_clip['position'])] = n_clip['content']

    # remove key with empty value
    clips = {k: v for k, v in clips.items() if v}
    n_clips = {x: y for x, y in n_clips.items() if y}

    # save/export clips
    save_highlight_clips(clips)
    save_note_clips(n_clips)
    
    export_txt(clips)


if __name__ == '__main__':
    main()
