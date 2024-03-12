import torch
from upstash_vector import Vector, Index
from datasets import load_dataset
from tqdm import tqdm, trange
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoTokenizer, pipeline
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA


def ask_question(question):
    # Get the embedding for the question
    question_embedding = embeddings.encode(doc)

    # Search for similar vectors
    res = index.query(vector=question_embedding, top_k=5, include_metadata=True)

    # Collect the results in a context
    context = "\n".join([r.metadata['text'] for r in res])

    prompt = f"Question:{question}\n\nContext: {context}"

    # Generate the answer using the LLM
    answer = llm(prompt)

    # Return the generated answer
    return answer[0]['generated_text']


data = load_dataset("HuggingFaceTB/cosmopedia", "stanford", split="train")

data = data.to_pandas()
data.to_csv("stanford_dataset.csv")
data.head()

loader = CSVLoader(file_path='./stanford_dataset.csv')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)

modelPath = "sentence-transformers/all-MiniLM-l6-v2"
model_kwargs = {'device':'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
 model_name=modelPath,
 model_kwargs=model_kwargs,
 encode_kwargs=encode_kwargs
)

# Generate embeddings for each chunk of text
chunk_embeddings = []
for doc in docs:
    # Generate embeddings for each chunk
    chunk_embedding = embeddings.encode(doc)
    chunk_embeddings.append(chunk_embedding)

# https://upstash.com/docs/redis/overall/getstarted
# https://www.youtube.com/watch?v=lK2DmL7t5R8
# https://upstash.com/

UPSTASH_VECTOR_REST_URL="<YOUR_UPSTASH_VECTOR_REST_URL>"
UPSTASH_VECTOR_REST_TOKEN="<YOUR_UPSTASH_VECTOR_REST_TOKEN>"

vectors = []

# generate the vectors in batches of 10
batch_count = 10

for i in trange(0, len(chunks), batch_count):   # Analisar a falta de referência
    batch = chunks[i:i+batch_count]             # Analisar a falta de referência

    embeddings = chunk_embedding[batch]

    for i, chunk in enumerate(batch):
        vec = Vector(id=f"chunk-{i}", vector=embeddings[i], metadata={
            "text": chunk
        })

        vectors.append(vec)

index = Index(
    url=UPSTASH_VECTOR_REST_URL,
    token=UPSTASH_VECTOR_REST_TOKEN
)

# If you want to reset your index beforehand uncomment this
# index.reset()

index.upsert(vectors)

from huggingface_hub import notebook_login
notebook_login()

model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", padding=True, truncation=True, max_length=512)

pipe = pipeline(
 "text-generation",
 model=model,
 tokenizer=tokenizer,
 return_tensors='pt',
 max_length=512,
 max_new_tokens=512,
 model_kwargs={"torch_dtype": torch.bfloat16},
 device="cuda"
)

llm = HuggingFacePipeline(
 pipeline=pipe,
 model_kwargs={"temperature": 0.7, "max_length": 512},
)

ask_question("Write an educational story for young children.")
