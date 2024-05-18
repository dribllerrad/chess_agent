import os
import shutil
from langchain_chroma import Chroma
from set_embedding_model import set_embedding_model

database_path = "database"

def set_database():
    database = Chroma(
        database_path, embedding_function=set_embedding_model(), persist_directory=database_path
        )
    return database

def delete_database():
    if os.path.exists(database_path):
        shutil.rmtree(database_path)
        print("✅ Database deleted")
        exit()
    else:
        print("❌ Database does not exist")