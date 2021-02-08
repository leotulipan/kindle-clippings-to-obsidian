# Kindle Clippings To Obsidian
*NOTE: This project is still under development and is not well documented, and is tailored for my specific use-case. I hope to make it more understandable and extensible so it is easier for others to use.*

A script to extract highlights and notes from kindle clippings (`My Clippings.txt`) and add them to a separate markdown file for each book/article.
Tailored for use with [Obsidian](https://obsidian.md/) (note-taking app).

There is also a script that picks a book and clipping at random to display in the command line, although it needs to be updated.

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
$ python kindle-to-markdown.py
```
### Instapaper Users
To get separate markdown files per article, highlight the title of an article and add the note `.Title.`. 
![title highlight example](https://github.com/WFinck97/kindle-clippings-to-obsidian/blob/master/images/title_highlight_example.JPG)
Make sure to also highlight the source web link, as this gets removed from the title and added to the header of the markdown file.

## Demo

Example output files tree:

```
$ tree .
.
├── My Clippings.txt
├── README.md
├── kindle-to-obsidian.py
└── output
    ├── B-Book Title.md
    ├── A-The Frontiers Of Digital Democracy - NOEMA.md
```

Example output file content (as you can see some notes are duplicated - it's not perfect but gets the job done!):

```markdown
#artcle
noemamag.com
Instapaper: Saturday, Feb. 6th (Instapaper)
- [ ] completed

---

The Frontiers Of Digital Democracy - NOEMA noemamag.com (27-28)

NOTE: .Title. (28)

---

I simply say that participation by citizens in such a process should be “fast, fun and fair.” Also, participation only works if there is a real effect on power. Most of the time, people agree on most of the issues around which they can reach a “rough consensus” as the basis for formulating policies that constitute and reflect the social norm. Polarization occurs on very few issues. (37-40)

NOTE: I likee the idea of participation in deliberation shouldd be fast easy and fun, and howw its only usrful if it shifts power (40)

---

should be “fast, fun and fair.” Also, participation only works if there is a real effect (38-38)

---

As a result of our practices of online deliberation, Taiwan’s president, Tsai Ing-wen, has said: “Before, democracy was a showdown between two opposing values. Now, democracy is a conversation between many diverse values.” (40-42)

NOTE: I likee the idea of participation in deliberation shouldd be fast easy and fun, and howw its only usrful if it shifts power (40)

NOTE: Great quote of how online partcipatory deliberation changes the dynamics of conversations around values (42)
```