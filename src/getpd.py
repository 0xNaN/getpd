import argparse
import sys
import logging

be_verbose = False

def main():

    # Option parsing
    args = parsing_init()



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
