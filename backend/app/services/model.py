import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Weaviate
from langchain_core.prompts import PromptTemplate
import weaviate
from weaviate.embedded import EmbeddedOptions

# Initialize Weaviate client
client = weaviate.Client(
    embedded_options=EmbeddedOptions()
)

# Specify embedding model (using huggingface sentence transformer)
embedding_model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "mps"}
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name, model_kwargs=model_kwargs
)

# Load and initialize model and tokenizer
model_name = "Qwen/Qwen2-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, return_token_type_ids=False)
tokenizer.bos_token_id = 1
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
)

# Build huggingface pipeline
hf_pipeline = pipeline(
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

llm = HuggingFacePipeline(pipeline=hf_pipeline)

qa_chain = None
vector_db = None

def train_model(split_docs):
    global qa_chain, vector_db
    vector_db = Weaviate.from_documents(
        split_docs, embeddings, client=client, by_text=False
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vector_db.as_retriever()
    )

def qa_chain(query):
    if not qa_chain or not hasattr(qa_chain, 'run'):
        return None

    prompt_template = "You are a helpful AI agent that is an expert on climate change. You will use the information to answer the user's questions: {query}"
    prompt = PromptTemplate(template=prompt_template)
    formatted_prompt = prompt.format(query=query)
    response = qa_chain.run(formatted_prompt)

    # split response and return only part after "Helpful Answer:
    response = response.split("Helpful Answer: ")[1]
    return response
