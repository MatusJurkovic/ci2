import csv
import io
import os
import sqlite3
import sys
import zipfile


class Database:
    archive_name = "world.zip"
    database_name = "db.sqlite"

    def __init__(self, parameters):
        self.parameters = parameters[1:]
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.connection = sqlite3.connect(self.database_name)

    def run(self):
        try:
            for file_name in self.parameters:
                table_name = os.path.splitext(os.path.basename(file_name))[0]
                if not self.table_exists(table_name):
                    self.import_csv(file_name, table_name)

            result = self.connection.execute(
                'SELECT COUNT(*) FROM "country" WHERE "Continent" = ?',
                ("Europe",),
            ).fetchone()
            print(result[0])
        finally:
            self.connection.close()

    def table_exists(self, table_name):
        result = self.connection.execute(
            "SELECT 1 FROM sqlite_master "
            "WHERE type = 'table' AND name = ? COLLATE NOCASE",
            (table_name,),
        ).fetchone()
        return result is not None

    def find_archive_member(self, archive, file_name):
        requested_name = file_name.replace("\\", "/")
        if not requested_name.lower().endswith(".csv"):
            requested_name += ".csv"

        archive_names = archive.namelist()
        if requested_name in archive_names:
            return requested_name

        base_name = os.path.basename(requested_name)
        matches = [
            name for name in archive_names
            if os.path.basename(name) == base_name
        ]
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise FileNotFoundError(
                f"{file_name!r} was not found in {self.archive_name}"
            )
        raise ValueError(
            f"{file_name!r} matches multiple files in {self.archive_name}"
        )

    def quote_identifier(self, identifier):
        return '"' + identifier.replace('"', '""') + '"'

    def find_csv_file(self, file_name):
        requested_name = file_name.replace("\\", os.sep).replace("/", os.sep)
        if not requested_name.lower().endswith(".csv"):
            requested_name += ".csv"

        candidates = [
            requested_name,
            os.path.join(self.script_directory, requested_name),
            os.path.join("world", os.path.basename(requested_name)),
            os.path.join(
                self.script_directory, "world", os.path.basename(requested_name)
            ),
        ]
        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate

        raise FileNotFoundError(
            f"{file_name!r} was not found in {self.archive_name} or an adjacent "
            "world directory"
        )

    def read_csv(self, csv_file, source_name):
        reader = csv.reader(csv_file, delimiter=";")
        try:
            headers = next(reader)
        except StopIteration as error:
            raise ValueError(f"{source_name!r} is empty") from error

        if not headers or any(not header for header in headers):
            raise ValueError(f"{source_name!r} contains an empty column name")
        if len(headers) != len(set(headers)):
            raise ValueError(f"{source_name!r} contains duplicate column names")

        records = []
        for row in reader:
            if len(row) != len(headers):
                raise ValueError(
                    f"{source_name!r}, line {reader.line_num}: "
                    f"expected {len(headers)} values, got {len(row)}"
                )
            records.append(
                tuple(None if value == "NULL" else value for value in row)
            )
        return headers, records

    def import_csv(self, file_name, table_name):
        archive_path = os.path.join(self.script_directory, self.archive_name)
        if os.path.isfile(self.archive_name):
            archive_path = self.archive_name
        elif not os.path.isfile(archive_path):
            csv_path = self.find_csv_file(file_name)
            with open(csv_path, "r", encoding="utf-8-sig", newline="") as csv_file:
                headers, records = self.read_csv(csv_file, csv_path)
        if os.path.isfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as archive:
                member_name = self.find_archive_member(archive, file_name)
                with archive.open(member_name, "r") as csv_binary:
                    with io.TextIOWrapper(
                        csv_binary, encoding="utf-8-sig", newline=""
                    ) as csv_file:
                        headers, records = self.read_csv(csv_file, member_name)

        quoted_table = self.quote_identifier(table_name)
        quoted_columns = ", ".join(
            self.quote_identifier(header) for header in headers
        )
        placeholders = ", ".join("?" for _ in headers)
        create_sql = (
            f"CREATE TABLE {quoted_table} ({quoted_columns})"
        )
        insert_sql = (
            f"INSERT INTO {quoted_table} ({quoted_columns}) "
            f"VALUES ({placeholders})"
        )

        with self.connection:
            self.connection.execute(create_sql)
            self.connection.executemany(insert_sql, records)


if __name__ == "__main__":
    Database(sys.argv).run()
