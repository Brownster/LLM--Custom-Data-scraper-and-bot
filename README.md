Knowledge Base and Chatbot

This repository contains code for preparing a knowledge base by extracting information from URLs and local PDF files, and a chatbot that can answer questions based on the prepared knowledge base. The chatbot uses OpenAI's GPT-3.5 model for answering questions and the Chroma vector store to search for relevant information in the knowledge base.
Dependencies

This project requires the following dependencies:

    bs4
    requests
    PyPDF2
    docx
    langchain
    tkinter
    tkinter.ttk
    openai

These can be installed via pip

How to Run

To prepare the knowledge base, run the prepare_kb() function by providing URLs to extract information from, the directory name where the vector store should be persisted, and the name of the collection. The max_level argument specifies how deep to extract links from the initial URLs. The documents_directory argument specifies the directory path to local PDF files that need to be included in the knowledge base. Once the function is run, the vector store will be persisted in the specified directory.

To run the chatbot, enter a question and click on the Ask button. The chatbot will use the prepared knowledge base to answer the question.
Functions
extract_links(url, level=1, max_level=1)

Extracts all the links from the given URL using Beautiful Soup recursively up to max_level.

    url (str): The URL to extract links from.
    level (int): The current level of recursion.
    max_level (int): The maximum level of recursion allowed.
    Returns:
        list[str]: A list of extracted links.

prepare_kb()

Extracts URLs from the input field, fetches documents from those URLs and local PDFs, and creates a vector store based on the documents. The collection_name argument specifies the name of the collection to create. The persist_directory argument specifies the directory path to persist the vector store. The max_level argument specifies the maximum level of recursion allowed when extracting links from the initial URLs. The documents_directory argument specifies the directory path to local PDF files that need to be included in the knowledge base.
ask_question()

Uses the prepared knowledge base to answer the question entered in the input field.
Modules
langchain

The langchain module provides tools for working with natural language data, including text splitting, embeddings, and vector stores.
tkinter

The tkinter module provides a graphical user interface (GUI) for the chatbot.
openai

The openai module provides access to OpenAI's GPT-3.5 model for generating text.
![Screenshot from 2023-04-10 23-17-34](https://user-images.githubusercontent.com/6543166/231009624-0916d24b-e699-4f26-8ad3-94df42971bef.png)
