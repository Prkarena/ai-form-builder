import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI

from htmlTemplates import bot_template, user_template, css
from config import OPENAI_API_KEY, OPENAI_MODEL_NAME, OPENAI_EMBEDDING_MODEL_NAME, OLLAMA_EMBEDDING_MODEL_NAME

# Ensure you load your .env file
load_dotenv()

def get_pdf_text(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_chunk_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    # embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=OPENAI_EMBEDDING_MODEL_NAME)
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL_NAME)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL_NAME, temperature=0)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    system_template = """
        You are a highly skilled form generator assistant.
        Your task is to create an HTML form based on the provided context and chat history.
        If you don't get any details from the context, just say that you don't know and don't try to make up an answer. If you get details, then the form should include appropriate input fields with labels and default values if applicable.
        The input fields can be checkboxes or radio buttons depending on the context and chat history details. The form should also include a submit button.
        When the submit button is clicked, the form should console.log() the details submitted by the user.

        Context: {context}

        Chat history: {chat_history}

        Based on the context and chat history, generate an HTML form with the following requirements:
        1. Include input fields with appropriate labels and types (checkboxes, radio buttons, etc.).
        2. Field type should be based on form context and input. If the form is regarding any steps performed by the user (like installation steps or maintenance steps), then input fields should be checkboxes. If the form is regarding steps completed or not (maintenance or installation steps), then input fields should be radio buttons.
        3. Ensure each input field has a label, also a default value if applicable, a placeholder if applicable, and indicate if the field is required or not.
        4. Include a submit button at the end of the form. On click of that button, we will check the form fields validations.
        5. When the form is submitted, it should console.log() the details submitted by the user.
        6. Add proper styles to this generated form so that it looks good.
        7. Make sure not to add any unwanted tags and elements in the form. The form should be in HTML format with proper coding standards.

        Question: {question}

        Generate the complete HTML form with submit button:

        Response format:
        <!DOCTYPE html>
        <html>
        <head>
            <title>Form Title</title>
            <style>
                <!-- style should be here -->
                <!-- make sure form background color is transparent and form border should be transparant -->
            </style>
        </head>
        <body>
            <h2>Form Title</h2>
            <p>Brief description of the form</p>
            <form id="generatedForm">
                <!-- Form fields will be populated here based on context -->
            </form>
            <script>
                <!-- add login to  console submittedData -->
            </script>
        </body>
        </html>
        """

    custom_prompt = PromptTemplate(
        template=system_template,
        input_variables=["context", "question",  "chat_history"],
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        verbose = True,
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    return conversation_chain

def handle_user_input(question):
    try: 
        response = st.session_state.conversation({'question': question})
        st.session_state.chat_history = response['chat_history']
    except Exception as e:
        st.error('Please select PDF and click on OK.')

def display_chat_history():
    if st.session_state.chat_history:
         # Reverse the chat history to display latest on top
        reversed_history = st.session_state.chat_history[::-1]

        # Create a new list to store formatted chat history
        formatted_history = []
        for i in range(0, len(reversed_history), 2):
            # Combine user and bot messages into a dictionary
            chat_pair = {
                "AIMessage": reversed_history[i].content,
                "HumanMessage": reversed_history[i + 1].content
            }
            formatted_history.append(chat_pair)

        for i, message in enumerate(formatted_history):
            st.write(user_template.replace("{{MSG}}", message['HumanMessage']), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", message['AIMessage']), unsafe_allow_html=True)
  
def main():
    st.set_page_config(page_title='Generate a Form from your PDFs', page_icon=':books:')
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header('Generate a Form from your PDFs :books:')

    question = st.text_input("Ask anything to your PDF:")
    if question:
        handle_user_input(question)

    if st.session_state.chat_history is not None:
        display_chat_history()
      
    with st.sidebar:
        st.subheader("Upload your Documents Here: ")
        pdf_files = st.file_uploader("Choose your PDF Files and Press OK", type=['pdf'], accept_multiple_files=True)
        
        if pdf_files and st.button("OK"):
            with st.spinner("Processing your PDFs..."):
                try:
                    # Get PDF Text
                    raw_text = get_pdf_text(pdf_files)
                    # Get Text Chunks
                    text_chunks = get_chunk_text(raw_text)
                    # Create Vector Store
                    vector_store = get_vector_store(text_chunks)
                    st.success("Your PDFs have been processed successfully. You can ask questions now.")
                    # Create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
    
