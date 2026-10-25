Useage: git clone https://github.com/MatusJurkovic/ci2.git
cd ci2
cd A03
python3 -m venv .venv
. .venv/bin/activate
pip install Beatifulsoup4
python nist_parser.py nist_benzidine.html