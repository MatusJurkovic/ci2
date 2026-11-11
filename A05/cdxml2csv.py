import csv
import sys
from pathlib import Path


def find_cdxml_files(arguments=None):
    if arguments is not None:
        input_arguments = [
            Path(argument)
            for argument in arguments
            if Path(argument).suffix.lower() == ".cdxml"
        ]
        if input_arguments:
            return sorted(
                path.resolve() for path in input_arguments if path.is_file()
            )

    search_directory = Path.cwd()
    files = sorted(
        path
        for path in search_directory.rglob("*")
        if path.is_file() and path.suffix.lower() == ".cdxml"
    )
    if not files and search_directory != Path(__file__).resolve().parent:
        search_directory = Path(__file__).resolve().parent
        files = sorted(
            path
            for path in search_directory.rglob("*")
            if path.is_file() and path.suffix.lower() == ".cdxml"
        )
    return files


def output_path(arguments):
    for argument in arguments:
        if Path(argument).suffix.lower() == ".csv":
            candidate = Path(argument)
            if not candidate.exists():
                return candidate
    return Path.cwd() / "cdxml2csv.csv"


def convert_files(files, pybel):
    rows = []
    most_bits = None

    for file_path in files:
        molecules = list(pybel.readfile("cdxml", str(file_path)))
        if not molecules:
            raise ValueError(f"No molecules were found in {file_path.name}")

        for molecule in molecules:
            smiles_output = molecule.write("smi").split()
            if not smiles_output:
                raise ValueError(f"No SMILES was produced for {file_path.name}")
            smiles = smiles_output[0]
            bits = molecule.calcfp("maccs").bits
            rows.append((file_path.name, smiles, bits))
            if most_bits is None or len(bits) > most_bits[1]:
                most_bits = (file_path.name, len(bits))

    return rows, most_bits


def convert_files_with_rdkit(files, chem, maccs_keys):
    rows = []
    most_bits = None

    for file_path in files:
        cdxml = file_path.read_text(encoding="utf-8-sig")
        molecules = chem.MolsFromCDXML(cdxml, sanitize=False)
        if not molecules:
            raise ValueError(f"No molecules were found in {file_path.name}")

        for molecule in molecules:
            molecule.UpdatePropertyCache(strict=False)
            problems = chem.DetectChemistryProblems(molecule)
            unsupported_problems = [
                problem
                for problem in problems
                if not (
                    problem.GetType() == "AtomValenceException"
                    and molecule.GetAtomWithIdx(problem.GetAtomIdx()).GetSymbol()
                    == "Al"
                )
            ]
            has_al_valence_issue = len(problems) != len(unsupported_problems)
            if unsupported_problems:
                details = "; ".join(
                    problem.Message() for problem in unsupported_problems
                )
                raise ValueError(f"Invalid structure in {file_path.name}: {details}")

            sanitize_ops = chem.SanitizeFlags.SANITIZE_ALL
            if has_al_valence_issue:
                print(
                    f"Warning: accepting aluminum valence in {file_path.name}; "
                    "RDKit's standard valence rules reject this structure.",
                    file=sys.stderr,
                )
                sanitize_ops ^= chem.SanitizeFlags.SANITIZE_PROPERTIES
            chem.SanitizeMol(molecule, sanitizeOps=sanitize_ops)
            smiles = chem.MolToSmiles(molecule)
            bits = list(maccs_keys.GenMACCSKeys(molecule).GetOnBits())
            rows.append((file_path.name, smiles, bits))
            if most_bits is None or len(bits) > most_bits[1]:
                most_bits = (file_path.name, len(bits))

    return rows, most_bits


def main(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]

    files = find_cdxml_files(arguments)
    if not files:
        print("Error: no .cdxml files were found.", file=sys.stderr)
        return 1

    try:
        from openbabel import pybel
    except ImportError:
        pybel = None

    if pybel is None:
        try:
            from rdkit import Chem
            from rdkit.Chem import MACCSkeys
        except ImportError:
            print(
                "Error: Open Babel with Pybel or RDKit is required to read .cdxml "
                "files. Install the dependency with: "
                "python -m pip install -r requirements.txt",
                file=sys.stderr,
            )
            return 1

    try:
        if pybel is None:
            rows, most_bits = convert_files_with_rdkit(files, Chem, MACCSkeys)
        else:
            rows, most_bits = convert_files(files, pybel)
        destination = output_path(arguments)
        with destination.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(("name", "smiles", "maccs"))
            writer.writerows(rows)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"{most_bits[0]}: {most_bits[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
