import argparse
import sys
import re

rules = []
inputs = []

def main():

    # Option parsing
    args = parsing_init()
    check_input(args)

# Check input
def check_input(args):
    for rule in args.rules:

        #check the rule with regex
        match = re.match('^\[.*\]\[[0-9:+-]*\]', rule)

        if match:
            rule =  re.split('^\[.*]\[', rule)
            print(rule[0], rule[1])
            # Check the regex specified and the interval

            # put in a table
        else:
            print(rule, "<- Malformed")
            # malformed input



# Parsing input options
def parsing_init():
    parser = argparse.ArgumentParser('getpd')
    parser.add_argument('-r', '--rules', nargs='+', required=True,
            help='Rules to perform the analysis')
    parser.add_argument('-i', '--input', nargs='+', required=True,
            help='Input data')
    return parser.parse_args()

if __name__ == '__main__':
    main()
