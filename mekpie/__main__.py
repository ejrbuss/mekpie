import sys
import argparse
import config

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    # Parse the command line arguments
    parsedargs = argparse.parse(args)
    # Dispatch the command
    parsedargs.command(parsedargs.options, parsedargs.args)

if __name__ == "__main__":
    main()