
import collections
import json
import re
import os

BOUNDARY = "\n==========\n"
OUTPUT_DIR = "output"
HIGHLIGHT_FILE = "highlights.json"
NOTE_FILE = "notes.json"
ARTICLE_FILE = "articles.json"

def SplitSections(filename):
    f = open(filename, "r")
    content = f.read()
    content = content.replace('\ufeff', '')
    return content.split(BOUNDARY)

def main():
    sections = SplitSections('My Clippings test.txt')
    print(sections)
    print(sections[1])

main()