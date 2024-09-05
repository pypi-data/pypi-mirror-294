    """
    Loads data from an XLSX file into a table in a SQL Server database.

    parameters:
    - path_folder: Path to the folder where the XLSX file is located.
    - file_name: Name of the XLSX file to be loaded.
    - table_name: Name of the target table in the database.
    - schema: Schema of the table in the database.
    - server: Name or address of the SQL server.
    - database: Name of the database.
    - user: Username for connecting to the database.
    - password: Password for connecting to the database.
    - driver: (Opcional) Driver ODBC a ser utilizado. Padrão: "ODBC Driver 17 for SQL Server".
    """