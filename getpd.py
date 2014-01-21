import argparse
import sys
import re

rules_re = []
rules_in = []
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
            # separate regex from interval
            rule =  rule[1:-1].rsplit('][')

            rule_regex = rule[0]
            rule_interval = rule[1]

            # compute the regex to know if it's valid
            try:
                re.compile(rule_regex)
            except re.error as Error:
                print(rule_regex + " Malformed: " + str(Error))
                exit()

            # put in a table
            global rules_re, rules_in
            rules_re.append(rule_regex)
            rules_in.append(rule_interval)
        else:
            print(rule, "<- Malformed")
            # malformed input

    print(rules_re)
    print(rules_in)


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
