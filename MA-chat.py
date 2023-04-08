import os
from tkinter import *
from tkinter import ttk
from pprint import pprint
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = 'your_open_api_key'

local_directory = "kb-h2o-wave"
persist_directory = os.path.join(os.getcwd(), local_directory)

# List of available collection names
collections = ["h2o_wave_knowledgebase"]


def submit_question():
    query_statement = question_entry.get()
    if query_statement == 'exit':
        window.quit()
    else:
        kb_db = Chroma.load(selected_collection.get(), persist_directory)

        kb_qa = ChatVectorDBChain.from_llm(
            OpenAI(temperature=0, model_name="gpt-3.5-turbo"),
            vectorstore=kb_db,
            top_k_docs_for_context=5,
            return_source_documents=True
        )

        result = kb_qa({"question": query_statement, "chat_history": []})
        answer_text.delete(1.0, END)
        answer_text.insert(INSERT, result["answer"])


# GUI setup
window = Tk()
window.title("Chatbot")

frame = Frame(window)
frame.pack(padx=20, pady=20)

collection_label = Label(frame, text="Select collection:")
collection_label.grid(row=0, column=0, sticky=W)

selected_collection = StringVar()
collection_dropdown = ttk.Combobox(frame, textvariable=selected_collection)
collection_dropdown['values'] = collections
collection_dropdown.grid(row=0, column=1, sticky=W)
collection_dropdown.current(0)

question_label = Label(frame, text="Enter your question:")
question_label.grid(row=1, column=0, sticky=W)

question_entry = Entry(frame, width=40)
question_entry.grid(row=1, column=1, sticky=W)

submit_button = Button(frame, text="Submit", command=submit_question)
submit_button.grid(row=1, column=2, padx=(10, 0), sticky=W)

answer_label = Label(frame, text="Answer:")
answer_label.grid(row=2, column=0, sticky=NW, pady=(10, 0))

answer_text = Text(frame, wrap=WORD, width=60, height=10)
answer_text.grid(row=2, column=1, columnspan=2, pady=(10, 0), sticky=W)

window.mainloop()

os.environ["OPENAI_API_KEY"] = ''
print("---------- Life is good ----------------")
