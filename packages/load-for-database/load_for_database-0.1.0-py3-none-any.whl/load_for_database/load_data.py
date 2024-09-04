import pandas as pd
import urllib
from sqlalchemy import create_engine

def load_data(path_folder, file_name, table_name, schema, server, database, user, password, driver="ODBC Driver 17 for SQL Server"):
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
    try:
        # Construir o caminho completo do arquivo
        caminho_arquivo = f"{path_folder}/{file_name}"

        # Ler o arquivo XLSX em um DataFrame
        df = pd.read_excel(caminho_arquivo)

        # Construir a string de conexão
        params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}")
        conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

        # Criar o engine de conexão
        engine = create_engine(conn_str)

        # Carregar os dados para a tabela no banco de dados
        df.to_sql(name=table_name, con=engine, schema=schema, if_exists="append", index=False)

        print(f"Data successfully loaded into the table {schema}.{table_name}.")

    except Exception as e:
        print(f"An error occurred while loading data: {e}")
