#!/usr/bin/env python3
import argparse
import re
# The script demonstrates using of Factory method design pattern
# where matcher using factory method and receives appropriate matcher based on the user flags

man_page = """ 
        Search Helper
        The script will find regex in the provided list of files to search in. 
        and will print in the following format 'file_name line_number line'
        
        The flag -r is mandatory 
        
        If --files parameter is missing, the script will take input from STDIN.
        When --files is provided it is mandatory to specify existing filename
        
        Example: Search any letter in STDIN           >>>python3 SearchHelper.py -r [a-z]
        Example: Search any letter in provided Files  >>>python3 SearchHelper.py -r [a-z] -f input.txt input2.txt
        """

# Output in the format: 'file_name line_number line'
class DefaultMatcher:

    def print_result(self, filename, file, pattern):
        for ind, line in enumerate(file):
            for match in re.finditer(pattern, line):
                print("{} {} {}".format(filename, ind + 1, line))


# Output in the format: 'file_name:line_number:start_position:matched_text'
class MachineMatcher:

    def print_result(self, filename, file, pattern):
        for ind, line in enumerate(file):
            for match in re.finditer(pattern, line):
                start = match.start()
                end = match.end()
                print("{}:{}:{}:{}".format(filename, ind + 1, line, line[start:end]))


# Output in the format: 'file_name line_number line' matched text is highlighted in color
class ColorMatcher:

    def print_result(self, filename, file, pattern):
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        for ind, line in enumerate(file):
            for match in re.finditer(pattern, line):
                start = match.start()
                end = match.end()
                print("{} {} {}".format(filename, ind + 1
                                        , line[:start] + OKGREEN + line[start:end] + ENDC + line[end:]))


# Output in the format: 'file_name line_number line' '^' is printed underneath the matched text
class UnderLineMatcher:

    def print_result(self, filename, file, pattern):
        for ind, line in enumerate(file):
            for match in re.finditer(pattern, line):
                start = match.start()
                end = match.end()
                prefix = "{} {} {}".format(filename, (ind + 1), line[:start])
                suffix = "{}".format(line[end:])
                print("{}{}{}".format(prefix, line[start:end], suffix))
                print("{}{}".format(" " * len(prefix), "^" * len(line[start:end]) + " " * len(suffix)))


def matcher_factory(args):
    if args.underline:
        match = UnderLineMatcher()
    elif args.color:
        match = ColorMatcher()
    elif args.machine:
        match = MachineMatcher()
    else:
        match = DefaultMatcher()
    return match


def main(args):
    match = matcher_factory(args)
    if args.files:
        for file in args.files:
            match.print_result(file.name, file, args.regex)
    else:
        STDIN = input("Please add the content to search:\n")
        match.print_result('STDIN', STDIN.split('\n'), args.regex)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(man_page)
    mandatory = parser.add_argument_group("mandatory arguments")
    mandatory.add_argument("-r", "--regex", required=True, help="the regular expression to search for.")

    parser.add_argument("-f", "--files", nargs='+', type=argparse.FileType('r'),
                        help="a list of files to search in.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--underline", action="store_true",
                       help="'^' is printed underneath the matched text")
    group.add_argument("-c", "--color", action="store_true",
                       help="the matched text is highlighted in color [1].")
    group.add_argument("-m", "--machine", action="store_true",
                       help="print the output in the format: 'file_name:line_number:start_position:matched_text'.")

    args = parser.parse_args()

    main(args)
