import sys
import os
class Texter:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        """Perform the operations on the specified file."""
        if not os.path.exists(self.filename):
            print(f"Error: The file '{self.filename}' does not exist.")
            return

# Open the file and read its contents
        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

    def display_counts(self):
        """Display the counts of vowels and consonants in the file."""
        if not os.path.exists(self.filename):
            print(f"Error: The file '{self.filename}' does not exist.")
            return

        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()

        vowel_count = count_vowels(content)
        consonant_count = count_consonants(content)

        print(f"Vowel count: {vowel_count}")
        print(f"Consonant count: {consonant_count}")

    def count_vowels(text: str) -> int:
        """Count all vowels (a, e, i, o, u) in the given text, regardless of case."""
        vowels = 'aeiouAEIOU'
        return sum(1 for char in text if char in vowels)

    def count_consonants(text: str) -> int:
        """Count all consonants (letters that are not vowels) in the given text, regardless of case."""
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        return sum(1 for char in text if char in consonants)

    def print_usage():
        """Print the usage instructions for the script."""
        print("Usage: python texter.py <filename>")
        print("Counts the number of vowels and consonants in the specified text file.")

    def main():
        # Check if command-line argument (filename) was passed
        if __name__ == "__main__":
            if len(sys.argv) != 2:
                self.print_usage()
                sys.exit(1)

            filename = sys.argv[1]
            texter = Texter(filename)
            texter.display_counts()