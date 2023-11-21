# PDF Booklet Arranger
A simple command-line application written in python to reorder the pages in a pdf file so that double-sided mini-booklets can be printed in correct order to be binded into a full A5-sized book.

## Why?
I have many e-books that I want to print and physical copies are either scarce or non-existent. Additionally, I prefer to read on paper than on a screen (Weird, I know).

## How does this work?
On a standard A4-sized paper, four A5-sized sheets in total can be printed on both sides without overlap. To make the paper fold into a booklet, the pages have to be ordered in a particular manner:
<mockup1>
<mockup2>
  
On one side of the paper, the fourth and first pages are printed from right-to-left, whereas on the other side, the second and third pages are printed from left-to-right. Reading is normally done facing the side of pages 2 and 3, and so the order of traversal along the pages follows a particular pattern: back-left, front-left, front-right, back-right.

This is concept especially apparent when you stack multiple sheets of paper together.
<mockup3>
The pages are ordered from back-left to front-left from the furthest back page to the frontmost, followed by front-right to back-right from the frontmost page to the furthest back.
  
Although it is technically possible to print out a book in this manner, it may be challenging to actually bind it down the middle. A site I googled a few days ago (I don't remember which one, sue me) suggested that separate stacks of 8 sheets of paper can be combined and glued together for better binding. This means that books have to be divided into sets of 8*4 = 32 pages that are ordered in the abovementioned manner.

Using Bash on linux, you can input this command to rearrange all files within a directory (Assuming you are in that directory and `main.py` is also within that directory, adjust accordingly):
```bash
mkdir done;
for file in ./*.pdf; do python main.py -R -f $file -o "done/${file:2:-4}-rearr.pdf"; done
```
