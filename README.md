# Kindle Clippings To Obsidian
*NOTE: This project is still under development and is not well documented, and is tailored for my specific use-case. I hope to make it more understandable and extensible so it is easier for others to use.*

A script to extract highlights and notes from kindle clippings (`My Clippings.txt`) and add them to a separate markdown file for each book/article.
Tailored for use with [Obsidian](https://obsidian.md/) (note-taking app).

## Instapaper Integration
[Instapaper](https://www.instapaper.com/) is a Read-It-Later app. I like to save articles that I would like to read to Instapaper, which can then automatically send a digest of articles to my kindle (I have it send a digest everyday as long as there is 1 new article since the last digest). The issue with this is that there is no distinction between articles in a digest. This program splits up the articles from each Instapaper digest and each article gets a markdown file with all highlights and notes.

## Features
Clippings (highlights and notes) are stored in a python dict with this structure

```python
clips = {'book': {'position': 'clipping'}}
```

Each new `My Clippings.txt` will add clips to previous archive automatically.

Clips will be export to `output` directory, find them there.


## Usage

Clone project and put `My Clippings.txt` to project's root. I keep the project files inside my obsidian vault.

Run `kindle-to-markdown.py`

```
$ python kindle.py
```
### Instapaper Users
To get separate markdown files per article, highlight the title of an article and at the note `.Title.`. 
![title highlight example](https://github.com/WFinck97/kindle-clippings-to-obsidian/blob/master/images/title_highlight_example.JPG)
Make sure to also highlight the source web link, as this gets removed and added to the header of the markdown file.

## Demo

Example output files tree:

```
$ tree .
.
├── My Clippings.txt
├── README.md
├── kindle-to-obsidian.py
└── output
    ├── Book Title (Paul Graham).md
    ├── Article Title.md
```

Example output file contet:

    Nerds aren't losers. They're just playing a different game, and a game much closer to the one played in the real world. Adults know this. It's hard to find successful adults now who don't claim to have been nerds in high school.

    ---

    What hackers and painters have in common is that they're both makers. Along with composers, architects, and writers, what hackers and painters are trying to do is make good things. They're not doing research per se, though if in the course of trying to make good things they discover some new technique, so much the better.

    ---

    This is not a problem for big companies, because they don't win by making great products. Big companies win by sucking less than other big companies.

