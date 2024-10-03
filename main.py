# fixing unicode error in google colab
import locale
locale.getpreferredencoding = lambda: "UTF-8"

# import dependencies
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    BitsAndBytesConfig,
)
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.vectorstores import Weaviate
from langchain_core.prompts import PromptTemplate

import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(
    embedded_options=EmbeddedOptions()
)

# specify embedding model (using huggingface sentence transformer)
embedding_model_name = "BAAI/bge-base-en-v1.5"

# arguments that are used to configure the model, these will be different for most models.
# model_kwargs = {"device": "cuda"}
# model_kwargs = {"device": "cpu"}
model_kwargs = {"device": "mps"}
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name, model_kwargs=model_kwargs
)


'''
This parameter can be one of the following options
pdf
youtube
'''
rag_dataset = 'youtube'

if rag_dataset == 'pdf':
    from langchain.document_loaders import PyPDFLoader

    # IPCC 2023 Climate change report
    pdf_url = 'https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_FullVolume.pdf'

    loader = PyPDFLoader(pdf_url)
    pages = loader.load()

    # We chuck the document in basis 1028 token chunks without overlap to load into Weaviate
    text_splitter = TokenTextSplitter(chunk_size=1028, chunk_overlap=0)
    split_docs = text_splitter.split_documents(pages)

if rag_dataset == 'youtube':
    import requests
    import xml.etree.ElementTree as ET

    # Techlinked channel RSS feed
    URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCeeFfhMcJa1kjtfZAGskOCA"

    response = requests.get(URL)
    xml_data = response.content

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Define the namespace
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/",
    }

    # Extract YouTube links
    youtube_links = [
                        link.get("href")
                        for link in root.findall(".//atom:link[@rel='alternate']", namespaces)
                    ][1:]

    # Download and split the captions of the collected youtube videos
    from langchain.document_loaders import YoutubeLoader

    all_docs = []
    for link in youtube_links:
        loader = YoutubeLoader.from_youtube_url(link)
        docs = loader.load()
        all_docs.extend(docs)
    text_splitter = TokenTextSplitter(chunk_size=128, chunk_overlap=0)
    split_docs = text_splitter.split_documents(all_docs)

if rag_dataset == "csv":
    from langchain.document_loaders import CSVLoader
    csv_url = "https://raw.githubusercontent.com/sayjeyhi/RAG_boilerplate/main/data/csv/test.csv"
    loader = CSVLoader(csv_url)
    docs = loader.load()
    text_splitter = TokenTextSplitter(chunk_size=1028, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)


vector_db = Weaviate.from_documents(
    split_docs, embeddings, client=client, by_text=False
)


res = vector_db.similarity_search(
    "What's the most promising new technology to preserve marine biodiversity", k=3)

print("==========")
print(res)


from transformers import pipeline

# specify model huggingface mode name
#model_name = "cognitivecomputations/dolphin-2.6-mistral-7b"
model_name = "Qwen/Qwen2-0.5B-Instruct"


# function for loading 4-bit quantized model
def load_quantized_model(model_name: str):
    """
    :param model_name: Name or path of the model to be loaded.
    :return: Loaded quantized model.
    """
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        # quantization_config=bnb_config
    )
    return model

# function for initializing tokenizer
def initialize_tokenizer(model_name: str):
    """
    Initialize the tokenizer with the specified model_name.

    :param model_name: Name or path of the model for tokenizer initialization.
    :return: Initialized tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name, return_token_type_ids=False)
    tokenizer.bos_token_id = 1  # Set beginning of sentence token id
    return tokenizer

# initialize tokenizer
tokenizer = initialize_tokenizer(model_name)
# load model
model = load_quantized_model(model_name)
# specify stop token ids
stop_token_ids = [0]

# build huggingface pipeline
pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    use_cache=True,
    max_length=2048,
    do_sample=True,
    top_k=5,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)

# specify the llm
llm = HuggingFacePipeline(pipeline=pipeline)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=vector_db.as_retriever()
)

# Define the pre-prompt template
template = """You are a helpful AI agent that is an expert on climate change.
  You will use the information from IPCC to anwser the user's questions on climate change: {query}"""
prompt = PromptTemplate(template=template)


# The user's question
question = "What's the best way to save the climate?"

# Use the prompt template to format the question
formatted_prompt = prompt.format(query=question)
response = qa_chain.run(formatted_prompt)
print(response)


