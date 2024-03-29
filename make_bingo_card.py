import numpy as np
import string
import random
import argparse


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(usage='Write TeX for bingo cards from ' +
                                     'a list of entries')
    parser.add_argument('--entry_file', '-e', type=str, help='The ' +
                        'path to the file containing the list of entries')
    parser.add_argument('--n_cards', '-cards', type=int, help='The number ' +
                        'of unique cards to generate (default: 1)')
    parser.add_argument('--title', '-title', type=str, help='The title to ' +
                        'print at the top of the cards (default: BINGO)')
    parser.add_argument('--n_rows', '-rows', type=int, help='The number of ' +
                        'rows for each card (default: 5)')
    parser.add_argument('--n_cols', '-cols', type=int, help='The number of ' +
                        'columns for each card (default: 5)')
    parser.add_argument('--free_space', '-free_space', action='store_true',
                        help='If flag is on, include a free space')
    parser.add_argument('--free_space_text', '-free_space_text', type=str,
                        help='The text for the free space (default "Free ' +
                        'Space")')
    parser.add_argument('--rng_seed', '-seed', type=int, help='The seed for ' +
                        'the random number generator that selects entries ' +
                        'for each card from the list of entries')
    parser.add_argument('--save_file', '-save_file', type=str, help='The ' +
                        'path to the file in which to save the bingo card ' +
                        'TeX (default: ./bingo_cards.tex)')
    parser.add_argument('--verbose', '-verbose', action='store_true',
                        help='If flag is on, print out information about ' +
                        'the cards')
    args = parser.parse_args()

    # Make sure we have a list of entries at all, otherwise this entire thing
    # is pointless
    assert args.entry_file is not None, ('\nA file containing the list of ' +
        'entries must be provided')
    # Now read in the entries
    with open(args.entry_file) as f:
        entries = f.read().splitlines()

    # Deal with default choices and tell the user what's happening if verbosity
    # is on
    if args.verbose:
        print('\nDefault choices:')
    if args.n_cards is None:
        args.n_cards = 1
        if args.verbose:
            print('  - Number of unique cards defaulting to 1')
    if args.title is None:
        args.title = 'BINGO'
        if args.verbose:
            print('  - Title defaulting to "BINGO"')
    if args.n_rows is None:
        args.n_rows = 5
        if args.verbose:
            print('  - Number of rows defaulting to 5')
    if args.n_cols is None:
        args.n_cols = 5
        if args.verbose:
            print('  - Number of columns defaulting to 5')
    if args.save_file is None:
        args.save_file = 'bingo_cards.tex'
        if args.verbose:
            print('  - Save file containing the TeX defaulting to ' +
                  './bingo_cards.tex')
    if args.free_space_text and not args.free_space:
        args.free_space = True
        if args.verbose:
            print('  - Free space text was provided but the free space flag ' +
                  'was not turned on - assuming that a free space is desired')
    if args.free_space and args.free_space_text is None:
        args.free_space_text = 'Free Space'
        if args.verbose:
            print('  - Free space text defaulting to "Free Space"')

    # It doesn't make sense to have duplicates on the same card, so we need
    # at least as many entries as there are spaces on the bingo card, or
    # (number of spaces - 1) if there's a free space
    if args.free_space:
        entries_n_min = args.n_rows * args.n_cols - 1
    else:
        entries_n_min = args.n_rows * args.n_cols
    assert len(entries) >= entries_n_min, (f'\n{len(entries)} were ' +
        'provided, but there must be at least as many entries as there are '+
        f'non-free space entries on the card ({entries_n_min})')

    if args.verbose:
        # Basic information about the cards
        if args.n_cards == 1:
            plural = ''
        else:
            plural = 's'
        if args.free_space:
            print(f'\nMaking {args.n_cards} card{plural} with {args.n_rows} ' +
                  f'rows, {args.n_cols} columns, and a free space with '
                  f'text "{args.free_space_text}"')
        else:
            print(f'\nMaking {args.n_cards} card{plural} with {args.n_rows} ' +
                  f'rows, {args.n_cols} columns, and no free space')
        # Tell the user if they've provided more entries than spaces on the
        # cards and how the code is handling it
        if len(entries) > entries_n_min:
            print(f'\nMore entries provided than space on the card{plural}, ' +
                  'not all entries will be included in every card')

    # If there is a free space, place it in the center. If the "center" is not
    # well-defined (either rows or columns is even), put it in the front half
    if args.free_space:
        # Behavior is different for even and odd numbers of rows and columns
        if args.n_rows % 2 == 0:
            free_row = int(args.n_rows / 2 - 1)
            if args.verbose:
                print('Number of rows is even, placing the free space in ' +
                      'the last of the first half of the rows')
        else:
            free_row = int(np.floor(args.n_rows / 2))
        if args.n_cols % 2 == 0:
            free_col = int(args.n_cols / 2 - 1)
            if args.verbose:
                print('Number of columns is even, placing the free space in ' +
                      'the last of the first half of the columns')
        else:
            free_col = int(np.floor(args.n_cols / 2))
        if args.verbose:
            print(f'\nFree space being placed in the card at row {free_row} ' +
                  f'and column {free_row}')
        # Get the index of the free space by constructing a grid of indices for
        # the card and grabbing the one corresponding to the (row, column)
        # ordered pair of the free space
        i_free = np.reshape(np.arange(0, args.n_rows * args.n_cols),
                            (args.n_rows, args.n_cols))[free_row, free_col]

    # Select entries from the list for the cards
    rng = np.random.default_rng(seed=args.rng_seed)
    all_cards = []
    for i in range(args.n_cards):
        # Draw from the list of entries without replacement. If the list of
        # entries is longer than the size of the card, this will not place
        # the same entries on every card
        card_entries = list(rng.choice(entries, replace=False,
                            size=entries_n_min))
        # If there's a free space, put it in the right place (and make it bold,
        # though it won't be bold in the final file if there's any math mode
        # in the free space text)
        if args.free_space:
            card_entries.insert(i_free, r'\textbf{' + args.free_space_text +
                                '}')
        all_cards.append(card_entries)

    # Write out the TeX for the bingo cards
    # First the header information (open the save file in write mode, which
    # will overwrite any existing text in the file) - need to do this because
    # the header includes information about the dimensions of the cards
    with open(args.save_file, 'w') as f:
        # A bunch of packages
        f.write(r'\documentclass{article}' + '\n')
        f.write(r'\usepackage[margin=0.25in]{geometry}' + '\n')
        f.write(r'\usepackage{tikz}' + '\n')
        f.write(r'\usetikzlibrary{calc}' + '\n\n')
        f.write(r'\pagenumbering{gobble}' + '\n\n')
        f.write(r'\newcommand{\Size}{3.5cm}' + '\n\n')

        # This is the part with the information about the dimensions
        # Make a sequence with the correct number of columns, to be unpacked
        # for each row later - this is the part with the information about the
        # dimensions (starts at 1, not zero)
        f.write('\def\Sequence{' + ', '.join([str(int(n_col+1))
                for n_col in range(args.n_cols)]) + '}' + '\n\n')
    
        # Now define the square for a given bingo entry
        f.write(r'\tikzset{Square/.style={' + '\n')
        f.write(r'    inner sep=0pt,' + '\n')
        f.write(r'    text width=0.9*\Size,' + '\n')
        f.write(r'    minimum size=\Size,' + '\n')
        f.write(r'    line width=1pt,' + '\n')
        f.write(r'    draw=black,' + '\n')
        f.write(r'    align=center' + '\n')
        f.write(r'    },' + '\n')
        f.write(r'    font={\fontsize{13pt}{16}\selectfont}' + '\n')
        f.write(r'}' + '\n\n')

        # Start the document
        f.write(r'\begin{document}' + '\n')
        f.write(r'\begin{center}' + '\n')

    # Now the actual cards
    # This was most of the hard work (figuring out the tikz), credit mostly to
    # https://tex.stackexchange.com/questions/49746/a-table-with-square-cells
    for i, card in enumerate(all_cards):
        # First construct the rows
        row_text = ['", "'.join(card[j*args.n_cols:j*args.n_cols+args.n_cols])
                    for j in range(args.n_rows)]
        row_text = ['"' + row + '"' for row in row_text]
        # And write each string for the row into the tikz picture
        with open(args.save_file, 'a') as f:
            # Write the title in bold, though as for the free space, it will
            # not compile as bold in the final file if the title has math mode
            f.write(r'\vspace*{\fill}{\huge\textbf{' + args.title + r'}} \\ ' +
                    r'\vspace{1.5em}' + '\n\n')
            f.write(r'\begin{tikzpicture}[draw=black, x=\Size,y=\Size]' +
                    '\n')
            f.write(r'\foreach \col in \Sequence {' + '\n')
            for i, row in enumerate(row_text):
                f.write(r'\def\row{{' + row + '}}\n')
                f.write(r'\node [Square] at ($(\col,-' + str(i+1) +
                        r')-(0.5,0.5)$) {\pgfmathparse{\row[\col-1]}' +
                        r'\pgfmathresult};' + '\n')
            f.write('}\n\end{tikzpicture}' +r'\vspace*{\fill}\newpage' +
                    '\n\n')

    with open(args.save_file, 'a') as f:
        # Now close the document
        f.write(r'\end{center}' + '\n')
        f.write(r'\end{document}')
    
    if args.verbose:
        print()