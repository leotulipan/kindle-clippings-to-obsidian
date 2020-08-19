#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os
import re
import random

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"output"
HIGHLIGHT_FILE = u"highlights.json"
NOTE_FILE = u"notes.json"
ARTICLE_FILE = u"articles.json"



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

def load_title_clips():
    """
    Load previous clips from NOTE_FILE
    """
    try:
        with open(ARTICLE_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def main():
    # for highlights
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_highlight_clips())

    n_clips = collections.defaultdict(dict)
    n_clips.update(load_note_clips())

    title_clips = collections.defaultdict(dict)
    title_clips.update(load_title_clips())    

    # loop through highlights

    rand_book = random.choice(list(clips.keys()))

    rand_highlight = random.choice(list(clips[rand_book].keys()))
    note = clips[rand_book][rand_highlight]

    # check for note
    hl_range = rand_highlight.split("-")
    for loc in n_clips[rand_book]:
        if int(loc) >= int(hl_range[0]) and int(loc) <= int(hl_range[1]):
            note = note + "\n\nNOTE: " + n_clips[rand_book][loc]
            note_loc = loc
    title = ''
    # check if article
    match = re.search('Instapaper: ', rand_book)
    if match:
        if rand_book in title_clips:
            title_loc = sorted(title_clips[rand_book])
            print("HELLO THERE")
            for x in range(len(title_loc)-2):
                print("range is: " + str(x))
                if (int(hl_range[0]) >= int(title_loc[x])) and (int(hl_range[0]) <= int(title_loc[x+1])):
                    title = title_clips[rand_book][str(title_loc[x])]
            if int(hl_range[0]) >= int(title_loc[len(title_loc)-1]):
                title = title_clips[rand_book][title_loc[len(title_loc)-1]]
    
    output = rand_book + '\n' + title + '\n' + note
    print(output)



if __name__ == '__main__':
    main()