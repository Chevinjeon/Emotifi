import os, dotenv
import base64

from langchain_community.vectorstores import faiss
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print("Model: ", 'models/embedding-001')
print("API Key: ", GEMINI_API_KEY)
print("Task Type: ", 'retrieval_query')
print(os.getenv('GEMINI_API_KEY')) 

""" RAG SETUP """
loader = DirectoryLoader(path='articles/', glob='*.txt')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200,
    separators=['\n\n\n', '\n\n', '\n', ' ', '']
)

text = text_splitter.split_documents(documents=docs)

faiss_vectors = faiss.FAISS.from_documents(
    documents=text,
    embedding=GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=GEMINI_API_KEY, task_type='retrieval_query')
)
faiss_vectors.save_local('faiss')



""" LLM SETUP """

llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=GEMINI_API_KEY, convert_system_message_to_human=True)


""" PROMPT SETUP """

raw_prompt_template = """You are a medical professional who will give useful advice to a ADHD patient who is feeling {mood}
Use the provided context on ADHD treatments and therapy to give advice in bullet point form.
Be sure to include a kind introduction and closing.

context: {context}
"""

prompt_template = PromptTemplate(
    input_variables=['mood', 'context'],
    template=raw_prompt_template
)


def get_advice(mood):

    relevant_content = faiss_vectors.similarity_search(mood, k=10)
    context = ''
    for doc in relevant_content:
        context += doc.page_content + '\n\n'
    prompt = prompt_template.format(
        mood=mood,
        context=context
    )
    for chunk in llm.stream(prompt):
        print(chunk.content)
        yield chunk.content




def get_analysis(img):
    pass
def get_melody():
    pass

from langchain_openai import ChatOpenAI
llm2 = ChatOpenAI(model='gpt-4', temperature=0, streaming=True)
def get_test_response():
    for chunk in llm2.stream('tell me a story in 30 words'):
        print(chunk.content)
        yield chunk.content