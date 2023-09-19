import pandas as pd
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import warnings

from app import prompt

warnings.filterwarnings("ignore")

# Importem dataset
df = pd.read_csv("Nashville Housing.csv")
df.head()

# Creem base de dades
import sqlite3
sqlite_db_path = "base_de_dades.sqlite"
conn = sqlite3.connect(sqlite_db_path)
df.to_sql('taula', conn, if_exists='replace', index=False)
conn.close()

# Conectem a OpenAI
db = SQLDatabase.from_uri("sqlite:///base_de_dades.sqlite")
OPENAI_API_KEY = "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"
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

db_chain.run(prompt)