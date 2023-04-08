# Knowledge Base Preparation and Chatbot

This project demonstrates how to create a custom knowledge base using OpenAI's GPT and langchain library and then use this knowledge base with a chatbot. The project contains two main parts: preparing the knowledge base and creating a chatbot.

## Installation

To run the code in this project, you'll need to install the following Python packages:

```sh
pip install langchain openai beautifulsoup4 requests

For Python 2.x users, you will also need to install the tkinter package:

sh

pip install python-tk

Usage
Preparing the Knowledge Base

    Run the prepare_kb.py script. A GUI window will appear, allowing you to input the URLs, collection name, and directory name.
    Provide the required information and click the "Prepare" button. The code will extract links from the URLs, remove duplicates, and create a knowledge base using the OpenAI API.

Creating a Chatbot

    Run the chatbot.py script. A GUI window will appear, allowing you to select the collection name and ask questions.
    Select the collection and type your question in the input field. Click the "Ask" button or press "Enter" to submit your question.
    The chatbot will respond with an answer based on the custom knowledge base.

License

This project is released under the MIT License.

Based on code from : https://github.com/prodramp/DeepWorks/blob/main/ChatGPT/LangChainOpenAI.md
