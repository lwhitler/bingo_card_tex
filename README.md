# Bingo Card LaTeX
Write a LaTeX file to construct bingo cards.

### Dependencies
- `numpy`

### Notes:

The only truly required command line argument is the file containing the entries to be used in the cards, which is assumed to have one entry per line.

As of March 29, 2024, the TeX file resulting from `make_bingo_card.py` compiles in Overleaf using pdfLaTeX and TeX Live 2023. Nothing else has been tested.

### Example usage:

If entries are stored in the the file `entries.txt`...

##### Create 10 cards, each with the default "BINGO" title, 5 columns, 4 rows, and a free space with the text "Free Space" and save the TeX to the default `bingo_card.tex` file:
`python make_bingo_card.py -e entries.txt -cards 10 -cols 5 -rows 4 -free_space_text "Free Space"`

##### Create the default 1 card titled "Title" with the default 5x5 grid and no free space, saved to `examples/example_card.tex`:
`python make_bingo_card.py -e entries.txt -title Title -save_file examples/example_card.tex`