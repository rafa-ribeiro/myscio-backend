import os

import google.generativeai as genai
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from chromadb import HttpClient

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Escolha um modelo. 'gemini-2.5-flash' é um ótimo ponto de partida.
model_name = "gemini-2.5-flash"
model = genai.GenerativeModel(model_name=model_name)

# Carregar documentos de um arquivo de texto
loader = TextLoader('../resources/document.txt')
documents = loader.load()
print(f"Número de documentos carregados: {len(documents)}")
# print(f"Conteúdo do primeiro documento:\n{documents[0].page_content[:200]}...")


# Dividir documentos em pedaços menores
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False
)

chunks = text_splitter.split_documents(documents)
print(f"Número de chunks criados: {len(chunks)}")
# print(f"Conteúdo do primeiro chunk:\n{chunks[0].page_content}")


# Inicializa o modelo de embedding do Gemini
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

chroma_client = HttpClient(host="localhost", port=9001)

# vector_store = Chroma.from_documents(
#     chunks,
#     embeddings,
#     client=chroma_client
# )

query = "Tem algum data scientist em algum time?"

vector_store = Chroma(
    collection_name="main_collection",
    embedding_function=embeddings,
    client=chroma_client
)

results = vector_store.similarity_search(query=query,k=3)

# for i, doc in enumerate(results):
    # print(f"Resultado {i+1}: {doc.page_content}")

context = results[0]


# Seu prompt
prompt = f"Context:\n{context} \n\nQuestion: {query}"

# Chamada para gerar o conteúdo
response = model.generate_content(prompt)

# Imprima a resposta do modelo
print(response.text)
