import argparse
import sys


class Texter:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        """Count and display the vowels and consonants in the file."""
        try:
            with open(self.filename, encoding="utf-8") as text_file:
                content = text_file.read()
        except OSError as error:
            print(
                f"Error: cannot read '{self.filename}': {error}",
                file=sys.stderr,
            )
            return 1

        vowel_count = sum(
            character.lower() in "aeiou" for character in content
        )
        letter_count = sum(character.isalpha() for character in content)
        consonant_count = letter_count - vowel_count

        print(f"Vowel count: {vowel_count}")
        print(f"Consonant count: {consonant_count}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Count vowels and consonants in a text file."
    )
    parser.add_argument("filename", nargs="?", help="the text file to process")
    args = parser.parse_args()

    if args.filename is None:
        parser.print_help()
        return 0

    return Texter(args.filename).run()


if __name__ == "__main__":
    sys.exit(main())
