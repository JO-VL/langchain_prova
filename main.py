import pandas as pd
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import warnings
import sqlite3

from app import prompt

warnings.filterwarnings("ignore")
OPENAI_API_KEY = "...."


def read_dataset(dataset_name: str) -> pd.DataFrame:
    df = pd.read_csv(dataset_name)
    df.head()

    return df


def create_db(dataset_df: pd.DataFrame):
    sqlite_db_path = "base_de_dades.sqlite"
    conn = sqlite3.connect(sqlite_db_path)
    dataset_df.to_sql('taula', conn, if_exists='replace', index=False)

    return conn


def connect_to_openai():
    return OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')


if __name__ == "__main__":
    dataset_df = read_dataset("Nashville Housing.csv")
    db_conn = create_db(dataset_df)
    openai_client = connect_to_openai()
    db_chain = SQLDatabaseChain(llm=openai_client, database=db_conn, verbose=True)
    db_chain.run(prompt)

# Conectem a OpenAI
db = SQLDatabase.from_uri("sqlite:///base_de_dades.sqlite")
OPENAI_API_KEY = "...."
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

db_chain.run(prompt)
