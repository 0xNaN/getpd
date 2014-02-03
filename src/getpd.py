import argparse
import sys
import re
import logging

rules_re = []
rules_in = []
inputs = []

be_verbose = False

def main():

    # Option parsing
    args = parsing_init()

    init_rules(args.rules)

def init_rules(rules):

    for rule in rules:
        rule_match = re.match('^\[.*\]\[[0-9:+-]*\]', rule)

        if rule_match:
            # split Regex from Interval
            rule = rule[1:-1].rsplit('][')

            rule_regex = rule[0]
            rule_interval = rule[1]

            # check correctness of the Regex
            if not is_correct_regex(rule_regex):
                logging.warning('Invalid regex-> %s', rule_regex)
            else:
                global rules_re, rules_in
                rules_re.append(rule_regex)
                rules_in.append(rule_interval)

                if(be_verbose)
                    loggin.info("Rule loaded -> %s

def is_correct_regex (regex):

    correct = False
    try:
        re.compile(regex)
        correct = True
    except re.error as E:
        correct = False

    return correct



# Parsing input options
def parsing_init():

    parser = argparse.ArgumentParser('getpd')
    parser.add_argument('-r', '--rules', nargs='+', required=True,
            help='Rules to perform the analysis')
    parser.add_argument('-i', '--input', nargs='+', required=True,
            help='Input data')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose')

    return parser.parse_args()

if __name__ == '__main__':
    main()
