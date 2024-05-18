import argparse
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from set_database import set_database, delete_database
#from set_database import set_database

data_path = "data"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete", action="store_true", help="Deleting the database...")
    args = parser.parse_args()
    if args.delete:
        print("Deleting the database...")
        delete_database()
    
    documents = load_documents()
    chunks = split_text(documents)
    create_database(chunks)
    print("♟♞♝♜♛♚ Done! ♔♕♖♗♘♙")


def load_documents():
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def create_database(chunks: list[Document]):
    
    database = set_database()

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = database.get(include=[])  
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in database: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"➕ Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        database.add_documents(new_chunks, ids=new_chunk_ids)
        print("✅ New documents added successfully.")
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


if __name__ == "__main__":
    main()