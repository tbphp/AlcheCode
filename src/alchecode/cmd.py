import argparse
import sys

from .app import Application


class Command:
    def run(self):
        parser = argparse.ArgumentParser(description="AlcheCode CLI mode")
        parser.add_argument("input", type=str, help="Input string to process")

        args = parser.parse_args()

        app = Application(input=args.input, is_cli=True)
        result = app.run()
        sys.stdout.write(result + "\n")
