from pathlib import Path

from bs4 import BeautifulSoup


def main():
    results_file = Path(__file__).with_name("nist_benzidine.html")
    with results_file.open(encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    for compound in soup.find_all(
        "a", href=lambda value: value and "/cgi/cbook.cgi" in value
    ):
        print(compound.get_text(strip=True))


if __name__ == "__main__":
    main()
