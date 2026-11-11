Usage: git clone https://github.com/MatusJurkovic/ci2.git
wsl
cd/ci2/A05
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python cdxml2csv.py

Description:
The script first finds .cdxml file paths. 
Then it loads structures using Open Babel (Pybel), if this fails it tries RDKit (hence listed in requirements).
Using commands "write("smi")" and "calcfp("maccs")" the script gets SMILES and MACCS.
The script then creates the CSV file containing SMILES and MACCS, which is saved to the chosen path (in this case to the A05 folder).
If the run command contains a name for the resulting CSV file (run with command: "python cdxml2.py name.csv"), and such file does not yet exist, the script names the resulting files as specified. 
If otherwise (no name specified/file already exists) the resulting CSV file is named cdxml2csv.csv
Finally, the script prints the name of the file with the largest number of bits and also returns its name. 