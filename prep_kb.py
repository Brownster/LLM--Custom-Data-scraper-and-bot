import os
from tkinter import *
from bs4 import BeautifulSoup
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from typing import List
from PyPDF2 import PdfReader
from docx import Document

os.environ["OPENAI_API_KEY"] = ''

def load_documents_from_directory(directory: str) -> List[str]:
    documents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith('.pdf'):
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    documents.append(text)
            except Exception as e:
                update_status(f"Error loading document {filename}, exception: {str(e)}")
        elif filename.endswith('.docx'):
            try:
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                documents.append(text)
            except Exception as e:
                update_status(f"Error loading document {filename}, exception: {str(e)}")
        else:
            continue

    return documents


def extract_links(url, level=1, max_level=1):
    """
    Extracts all the links from the given URL using Beautiful Soup recursively up to max_level.
    Args:
        url (str): The URL to extract links from.
        level (int): The current level of recursion.
        max_level (int): The maximum level of recursion allowed.
    Returns:
        list[str]: A list of extracted links.
    """
    if level > max_level:
        return []

    try:
        response = requests.get(url)
        if response.status_code != 200:
            update_status(f"Error fetching or processing {url}, status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        links = [link for link in links if link and link.startswith('http')]

        if level < max_level:
            child_links = []
            for link in links:
                child_links.extend(extract_links(link, level=level+1, max_level=max_level))
            links.extend(child_links)

        return links
    except Exception as e:
        update_status(f"Error extracting links from {url}, exception: {str(e)}")
        return []



def update_status(status_text):
    status_text_widget.config(state=NORMAL)
    status_text_widget.insert(END, status_text + "\n")
    status_text_widget.config(state=DISABLED)
    status_text_widget.yview(END)

def prepare_kb():
    """
    Prepares the knowledge base by loading documents from URLs, removing duplicates,
    and processing the documents with OpenAI embeddings.
    """
    # Extract URLs from the text widget and find all links within them
    start_urls = urls_text.get(1.0, END).strip().split("\n")
    all_urls = []

    # Get the documents directory from the GUI input fields
    documents_directory = documents_directory_entry.get()
    collection_name = collection_name_entry.get().lower()
    local_directory = directory_name_entry.get()
    max_level = int(max_level_entry.get()) if max_level_entry.get().isdigit() else 3
    persist_directory = os.path.join(os.getcwd(), local_directory)

    update_status("Extracting links...")
    for url in start_urls:
        links = extract_links(url, max_level=max_level)
        all_urls.extend(links)
        update_status(f"Extracted links from {url}")

    # Remove duplicates by converting the list of URLs to a set and then back to a list
    unique_urls = list(set(all_urls))

    # Load the documents from the unique URLs
    update_status("Loading documents from URLs...")
    loader = UnstructuredURLLoader(urls=unique_urls)
    
    try:
        kb_data = loader.load()
    except Exception as e:
        update_status(f"Error fetching or processing URL(s), exception: {str(e)}")
        return

    # Process the PDF and Word files from the directory
    update_status("Processing local files ...")
    documents = load_documents_from_directory(documents_directory)
    kb_data.extend(documents)

    # Split the documents into smaller chunks
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    kb_doc = text_splitter.split_documents(kb_data)

    # Generate embeddings for the documents
    embeddings = OpenAIEmbeddings()

    # Create a Chroma vector store from the documents and their embeddings
    kb_db = Chroma.from_documents(kb_doc,
                          embeddings,
                          collection_name=collection_name,
                          persist_directory=persist_directory
                          )
    # Persist the vector store
    update_status("Persisting the vector store...")
    kb_db.persist()

    update_status("Knowledge base preparation complete.")


# GUI setup
window = Tk()
window.title("Prepare Knowledge Base")

frame = Frame(window)
frame.pack(padx=20, pady=20)

urls_label = Label(frame, text="Enter URLs (one per line):")
urls_label.grid(row=0, column=0, sticky=NW)

urls_text = Text(frame, wrap=WORD, width=60, height=10)
urls_text.grid(row=0, column=1, pady=(0, 10), sticky=W)

collection_label = Label(frame, text="Collection Name:")
collection_label.grid(row=1, column=0, sticky=W)

collection_name_entry = Entry(frame, width=40)
collection_name_entry.grid(row=1, column=1, sticky=W)

directory_label = Label(frame, text="Directory Name:")
directory_label.grid(row=2, column=0, sticky=W)

directory_name_entry = Entry(frame, width=40)
directory_name_entry.grid(row=2, column=1, sticky=W)

max_level_label = Label(frame, text="Max Link Level:")
max_level_label.grid(row=3, column=0, sticky=W)

max_level_entry = Entry(frame, width=40)
max_level_entry.grid(row=3, column=1, sticky=W)

# Add a label and entry field for the documents directory
documents_directory_label = Label(frame, text="Documents Directory:")
documents_directory_label.grid(row=4, column=0, sticky=W)

documents_directory_entry = Entry(frame, width=40)
documents_directory_entry.grid(row=4, column=1, sticky=W)

prepare_button = Button(frame, text="Prepare", command=prepare_kb)
prepare_button.grid(row=5, column=1, pady=(10, 0), sticky=E)

status_label = Label(frame, text="")
status_label.grid(row=5, column=1, pady=(10, 0), sticky=W)

status_label = Label(frame, text="Status:")
status_label.grid(row=6, column=0, pady=(10, 0), sticky=W)

status_text_widget = Text(frame, wrap=WORD, width=60, height=10, state=DISABLED)
status_text_widget.grid(row=6, column=1, pady=(10, 0), sticky=W)

window.mainloop()

os.environ["OPENAI_API_KEY"] = ''
