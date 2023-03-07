import argparse

# Default stack of papers is 8, so total number of A5
# pages fitting on an A4 paper is 32
def page_range(start=1, total_pages=32, verbose=False, delim=','):
    res = []

    if verbose:
        print("Pages to be printed per piece of paper:")

    # For every A4 piece of paper, 4 pages can be printed out
    # Not intended to work with odd numbers
    for seq in range(total_pages // 4):
        # Generate list [a, b, c, d] where pages (a, b)
        # should be printed on one side, and pages (c, d)
        # should be printed on the other
        paper_print = [
                start + total_pages - 1 - 2 * seq,
                start + 2*seq,
                start + 2*seq + 1,
                start + total_pages - 2 - 2*seq
                ]

        # Print the resultant list if desired
        if verbose:
            print(paper_print)
        res += paper_print

    if delim is not None:
        res = [str(item) for item in res]
        print("\nResult:")
        print(delim.join(res))

    return res

# The 'verbose' flag prints in sets of papers per stack
# Imma be real with you - I have ZERO clue as to what to
# name this function
def page_stack(total_pages, papers_per_stack=8, verbose=False, delim=',', indexed=False):
    res = []

    # 4 * A5 pages per A4 paper
    pages_per_stack = papers_per_stack*4

    # If there is a remainder, the total number of pages in print
    # will extend (or overflow) to the next multiple (or rep) by 
    # adding the respective number of blank pages
    reps, rem = divmod(total_pages, pages_per_stack)

    # If there is a remainder in dividing the total pages by the
    # number of pages in a stack, the range of blank pages in the
    # overflow will be reflected
    if rem > 0 and verbose:
        print("Warning: Extra blank pages from {} to {}".format(
                total_pages + 1,
                pages_per_stack * (reps + 1)
            ))

    # TODO: Decide if there is a better way to structure this data
    for rep in range(reps + (rem > 0)):
        if verbose:
            print(f"STACK #{rep + 1}\n")
        res += page_range(rep * pages_per_stack + 1 - indexed,
                          total_pages = pages_per_stack,
                          verbose = verbose,
                          delim=None)
        if verbose:
            print("-"*50)

    if delim is not None:
        res = [str(item) for item in res]
        print("Result:")
        print(delim.join(res))

    if verbose:
        print("Page_stack call result:")
        print(res)
    return res

def rearrange_pdf(filename, papers_per_stack, verbose, output='new_pdf.pdf'):
    import pikepdf

    new_pdf = pikepdf.Pdf.new()

    with pikepdf.Pdf.open(filename) as read_pdf:
        total_pages = len(read_pdf.pages)
        new_arrangement = page_stack(total_pages, papers_per_stack, verbose, delim=None, indexed=True)
        counter = 0
        while len(read_pdf.pages) < len(new_arrangement) and counter < 150:
            read_pdf.add_blank_page()
            counter += 1
            if verbose:
                print("Blank page added to buffer...")
                print("Now at {} out of {} pages".format(len(read_pdf.pages), len(new_arrangement)))
        for page_no in new_arrangement:
            new_pdf.pages.append(read_pdf.pages[page_no])
    
    new_pdf.save(output)
        

# Filter keys for args
def filter_keys(args: dict, *keys):
    arg_keys = list(args.keys())
    for key in arg_keys:
        if key not in keys:
            args.pop(key)
    return args

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate page order to fit a booklet based on the current page value and the total number of pages to be printed')

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-S', '--set', action='store_true')
    parser.add_argument('-A', '--arrangement', action='store_true')
    parser.add_argument('-R', '--rearrange-file', action='store_true')
    parser.add_argument('-i', '--indexed', action='store_true')

    # Properly ordered for humour's sake
    parser.add_argument('-p', '--papers-per-stack', type=int, default=8)
    parser.add_argument('-t', '--total-pages', type=int, default=32)
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-d', '--delim', type=str, default=',')
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-o', '--output', type=str, default='new_pdf.pdf')

    args = vars(parser.parse_args())

    # Program will stop when there is more than or less than one
    # arg selected between -R, S, and -A
    if args['arrangement'] + args['set'] + args['rearrange_file'] != 1:
        print('Either the -S, -A, or -R flag must be set (and not zero, two or more simultaneously)')
        exit()

    if args['set']:
        args = filter_keys(args, 'start', 'total_pages', 'verbose', 'delim')
        page_range(**args)
    
    elif args['arrangement']:
        args = filter_keys(args, 'total_pages', 'papers_per_stack', 'verbose', 'delim', 'indexed')
        page_stack(**args)

    elif args['rearrange_file']:
        if args['filename'] is None:
            print('A file is required (using the -f flag) to rearrange')
            return
        args = filter_keys(args, 'filename', 'output', 'papers_per_stack', 'verbose')
        rearrange_pdf(**args)
