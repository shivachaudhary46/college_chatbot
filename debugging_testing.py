import streamlit as st 
from pathlib import Path

def load_document(file):
    import os
    name, extension = os.path.splitext(file)

    if extension == ".pdf":
        from langchain.document_loaders import PyPDFLoader
        print(f"Loading PDF file ......{file}")
        loader = PyPDFLoader(file)
        print(f"Done........")

    elif extension == ".docx":
        from langchain.document_loaders import Docx2txtLoader
        print(f"Loading docx file.......{file}")
        loader = Docx2txtLoader(file)
        print(f"Done.......")

    elif extension == ".txt":
        print(f"loading txt file.......{file}")
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file, encoding='utf-8')
        print(f"Done.......")

    else:
        print("Document format is not supported!")
        return None 

    data = loader.load()
    return data

def chunk_data(data, chunk_size=256):

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=20)
    chunks = text_splitter.split_documents(data)
    return chunks

def ask_with_memory(vector_store, question, chat_history=[]):
    from langchain.chains import ConversationalRetrievalChain
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash' , temperature=1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})

    crc = ConversationalRetrievalChain.from_llm(llm, retriever)
    result = crc({'question': question, 'chat_history': chat_history})
    chat_history.append((question, result['answer']))
    return result, chat_history

with st.sidebar : 
    uploaded_file = st.file_uploader("Upload a file: ", type=['pdf', 'docx', 'txt'])
    chunk_size = st.number_input('chunk_size: ', min_value=100, max_value=1536, value=256)
    k = st.number_input("k :", min_value=1, max_value=5, value=3)

    add_data = st.button("Add Data")

    if uploaded_file and add_data:
        st.text("file is going to be saved......loading")
        save_folder = "./"
        save_path = Path(save_folder, uploaded_file.name)
        bytesdata = uploaded_file.read()
        with open(save_path, 'wb') as w:
            w.write(bytesdata)
            st.text(f"file written into the path {save_path} successfully")

        if save_path.exists():
            st.success(f"File {uploaded_file.name} is successfuly saved")

        document = load_document(save_path)
        st.text(f"document: {document}")

        chunks = chunk_data(document)
        st.text(f"chunks : {len(chunks)}")

        