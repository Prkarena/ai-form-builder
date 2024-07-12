## Requirements Document for AI Form Builder using Streamlit

### Overview
The AI Form Builder is an application designed to streamline the creation of forms from product-related PDFs using AI. The app allows users to upload PDF files, generate forms based on the PDF content, modify forms through AI suggestions, and save forms for future use. The application will be implemented as a multi-page Streamlit app.

### Functional Requirements

#### Step 1: Files Listing Screen
1. **File Upload and Storage**
   - **Display Uploaded Files:** Show a list of previously uploaded PDF files.
   - **Upload New File Button:** Allow users to upload a new PDF file.
     - On click, prompt the user to provide a file name and select a PDF file.
     - Call an API to store the file in the vector store.
   - **Update Existing File:** Allow users to update an existing file.
     - On click of an already uploaded file, allow the user to select a new file.
     - Update the vector store with the new file content.

2. **API Integration**
   - **Upload API:** Endpoint to upload and store PDF files in the vector store.
   - **Update API:** Endpoint to update the existing file content in the vector store.

#### Step 2: Forms Listing Screen
1. **Forms Management**
   - **Display Forms:** Show a list of forms that have been previously saved by the user.
   - **Create Form Button:** Allow users to create a new form.
     - On click, prompt the user to choose a file name from the list of uploaded files.
     - Redirect to the Form Builder screen.

2. **Form Builder Screen**
   - **Form Generation and Modification**
     - **Chat Interface:** Enable a chat interface where users can interact with AI to build and modify forms.
     - **Generate Form Sections:** Allow users to ask the AI to generate specific sections of the form (e.g., "Generate form for installation steps completed or not").
     - **Form Elements:** Support different input types such as radio buttons, text fields, checkboxes, and date inputs.
     - **Validation:** Support various validation rules (e.g., required fields).
   - **Save Button:** Save the generated form.
     - Show an alert with the response added by the user.
     - Store the final form in the database.

3. **Form Interaction**
   - **Open and Submit Forms:** Allow users to click on a form row in the list to open the form in a new tab.
     - Users can submit the form, and the responses will be stored in the database.

### Non-Functional Requirements

1. **Performance**
   - Ensure fast and efficient handling of large PDF files and generated forms.
   - Optimize API calls to handle concurrent uploads and updates.

2. **Usability**
   - Provide an intuitive user interface with clear prompts and feedback.
   - Ensure the form builder is user-friendly and responsive.

3. **Security**
   - Ensure secure file uploads and storage.
   - Implement proper validation and error handling for API calls.

### Technical Requirements

1. **Frontend**
   - Use Streamlit for the user interface.
   - Implement multi-page navigation in Streamlit.

2. **Backend**
   - Use a vector store for storing PDF file content and embeddings.
   - Implement APIs for file upload, update, and form storage.

3. **Database**
   - Store generated forms and user responses in a database.
   - Ensure data integrity and security.

### Implementation Plan

1. **Setup Streamlit Multi-Page App**
   - Configure Streamlit for multi-page navigation.
   - Implement the layout and navigation for Files Listing Screen and Forms Listing Screen.

2. **File Upload and Management**
   - Implement the file upload feature with API integration.
   - Display the list of uploaded files and handle file updates.

3. **Form Builder**
   - Develop the chat interface for interacting with AI.
   - Implement the form generation and modification features.
   - Add support for different form elements and validation rules.

4. **Form Storage and Interaction**
   - Implement the save functionality to store forms in the database.
   - Allow users to open and submit forms from the Forms Listing Screen.

5. **Testing and Deployment**
   - Test the application thoroughly for usability, performance, and security.
   - Deploy the application to a production environment.

### User Stories

1. **As a user, I want to upload a new PDF file so that I can store its content in the vector store.**
2. **As a user, I want to update an existing PDF file so that I can keep the content up to date.**
3. **As a user, I want to see a list of uploaded files so that I can manage them easily.**
4. **As a user, I want to create a new form based on a PDF file so that I can generate forms efficiently.**
5. **As a user, I want to interact with AI to build and modify forms so that I can get suggestions and improve the form quality.**
6. **As a user, I want to save the generated form so that I can use it later.**
7. **As a user, I want to submit a form and store the responses in the database so that I can keep track of the data.**

This requirements document outlines the key features and functionalities needed to develop the AI Form Builder using Streamlit. The document serves as a guide for the development team to implement the application efficiently.






# QueryPDFs

## Purpose: To Solve Problem in finding proper answer from PDF content.

PDF having many pages if user want to find any question's answer then they need to spend time to understand and find the answer. 

The purpose of this project is to create a chatbot that can interact with users and provide answers from a collection of PDF documents. The chatbot uses natural language processing and machine learning techniques to understand user queries and retrieve relevant information from the PDFs. By incorporating OpenAI models, the chatbot leverages powerful language models and embeddings to enhance its conversational abilities and improve the accuracy of responses.

## Features

- Multiple PDF Support: The chatbot supports uploading multiple PDF documents, allowing users to query information from a diverse range of sources.
- Conversational Retrieval: The chatbot uses conversational retrieval techniques to provide relevant and context-aware responses to user queries.
- Language Models: The project incorporates OpenAI models for natural language understanding and generation, enabling the chatbot to engage in meaningful conversations.
- PDF Text Extraction: The PDF documents are processed to extract the text content, which is used for indexing and retrieval.
- Text Chunking: The extracted text is split into smaller chunks to improve the efficiency of retrieval and provide more precise answers.

## Usage

-  Upload PDF documents: Use the sidebar in the application to upload one or more PDF files.
-  Ask questions: In the main chat interface, enter your questions related to the content of the uploaded PDFs.
-  Receive answers: The chatbot will generate responses based on the information extracted from the PDFs.

## Sample Output

![QueryPDF](https://github.com/Prkarena/langchain-chatbot-multiple-pdf/raw/development/QueryPDF.png?raw=true)

### ChatBot WorkFlow
![ChatBot WorkFlow](https://github.com/Prkarena/langchain-chatbot-multiple-pdf/raw/development/chat-bot-workflow.png?raw=true)

### QueryPDF Flow
![QueryPDF Flow](https://github.com/Prkarena/langchain-chatbot-multiple-pdf/raw/development/Query-PDF-Flow.png?raw=true)


## Installation

To install and run the Langchain Chatbot, follow these steps:

Clone the repository 

```
git clone https://github.com/Prkarena/langchain-chatbot-multiple-pdf.git
```

Add your OpenAI Key by creating a .env file in the folder and add the following within it:

```
OPENAI_API_KEY=
OPENAI_MODEL_NAME=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL_NAME=text-embedding-3-small
```

Create a Virtual Environment

```
pip install virtualenv
```

to run this app do activate environment and run app

```
 python3 -m venv pdf-builder-environment
```

```
source pdf-builder-environment/bin/activate
```

Install the dependencies using requirements.txt

```bash
pip install -r requirements.txt
```

```
streamlit run app.py
```

Install  OpenLLama
```
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
ps aux | grep  ollama (to check running process)
ollama pull mxbai-embed-large
ollama list  (to check already installed packages)
```
