# ♟♞♝♜♛♚ chess_agent ♔♕♖♗♘♙
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

> AI Chess Chatbot configured to use local llms and an updatable local RAG database referencing a customizable set of chess documentation.  

## Dependencies

> [!WARNING]
> Currently Langchain seems to be having problems with python dependencies from version 3.12.  It is recommended to use python 3.11 until this is resolved upstream.  

The app uses ollama to serve the local llms and is a prerequesite.  
> https://ollama.com/download  

After installing ollama, start the server with the following command:
```sh
ollama serve
```

The embedding model used is https://ollama.com/library/mxbai-embed-large and can be installed with:
```sh
ollama pull mxbai-embed-large
```

The llm is https://ollama.com/library/llama3 and can be installed with:
```sh
ollama pull llama3
```

> [!NOTE]    
> Any llm from ollama can be used for the natural language processing, RAG, or vector embedding and can be configured in the [set_llm.py](set_llm.py) or [set_embedding_model.py](set_embedding_model.py) methods by changing string variable `model_name = "llama3"`.

All other dependencies should be installed in a virtual environment with.
```sh
python3.11 -m venv ai
source ai/bin/activate
pip install -r requirements.txt
```

## Usage
To illustrate the usage, the repo contains a preconfigured `data` directory with a single PDF doc about chess.  We first create our vector database by running the following command:
```sh
python create_database.py
```

This will scan the `data` directory for all new PDFs, parse and split the text into digestably referencable chunks, and create a vector database in the `database` directory.  This database is what the chatbot will use to answer questions.

>  [!WARNING]  
>  This database creation can take a while depending on your system, the embedding-llm used, and the total number of PDFs in the `data` directory.

In the `data_sample` directory, there is a sample of other chess related PDFs that can be added to the `data` directory.  Running the `create_database.py` will add these new files to the current database without overwriting the existing data.  This allows for the database to be easily updated with new information by simply adding it to the `data` directory.

To remove the database and start fresh, run the following command:
```sh
python create_database.py --delete
```

Finally, query the chatbot directly with your question quoted in the prompt.
```sh
python chatbot.py "Define a checkmate?"
```

The output will be a response based based solely on the information in the database.  The last line in the output will reference exactly which files the llm is basing its response on.  The quality of the response will be largely dependent on the quality of the data used in the database.  Poorly OCR scanned PDFs will be difficult to digest leading to a lower quality vector database.

The ultimate quality of the responses will depend on the llms used, the quality of the input data, and the quality of the text splitting and vector embedding.  The current configuration is a good starting point, but can be improved by adding more chess related PDFs to the `data` directory and re-running the `create_database.py` script.  Also note that the chunk_size and chunk_overlap can be adjusted in the `create_database.py` script to improve the quality of the text splitting and vector embedding.  The default values are 1000 and 20 respectively.

```python
text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
```


## Evaluating the quality of reponses  
This is incredibly important as the quality of the responses will depend on an number of factors including the llms used, the quality of the input data, and the quality of the text splitting and vector embedding.  Tests are preconfigured in the `test_chess_bot.py` file and can be run with the following command:

```sh
pytest -sxv
```

The tests will again use the llms to generate a response to some precofigured questions and compare the response to the expected response.  Although we are attempting to constrain the responses of the llm into repeatable values, the llm is still a neural network and can produce different results for the same input.  Therefore the llm is used to make a qualatative determination as to whether the response is correct or not.  The test should produce a pass fail response for the following questions:

```
QUESTION: How many squares are on a chess board?  ANSWER: 64
QUESTION: Is the King a chess piece?  ANSWER: Yes
QUESTION: Is the Pope a chess piece?  ANSWER: No
```


## Author

👤 **Darrell Bird**

* Website: https://github.com/dribllerrad
* Github: [@dribllerrad](https://github.com/dribllerrad)

## Show your support

Give a ⭐️ if this project helped you!
