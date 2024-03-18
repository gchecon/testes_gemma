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

'''
Neste ponto do programa foi utilizado a biblioteca Cosmopedia. Avaliar o uso de
Arquivos próprios para aprimorar o uso do RAG 
'''

data = load_dataset("HuggingFaceTB/cosmopedia", "stanford", split="train")

data = data.to_pandas()
data.to_csv("stanford_dataset.csv")
data.head()

loader = CSVLoader(file_path='./stanford_dataset.csv', encoding='utf-8')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)

'''
Aqui é usado o modelo all-MiniLM-l6-v4. Avaliar a utilização de outros modelos
'''

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

'''
Nesta parte do código é utilizado o vector database Upstash
Avaliar o uso do PostgreSQL
'''

UPSTASH_VECTOR_REST_URL="https://precise-kangaroo-41875.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="AaOTACQgNzlkNmIyM2UtZDUyYS00NDQwLWJiMzEtZGJjZThlMjBkZWJhNmNkY2Q3ZDNhNzI2NDBhMjlhM2RkMmRjZGFiYzk1MTk="

vectors = []

# generate the vectors in batches of 10
batch_count = 10

# correção do texto original -> chunks para docs

for idx in trange(0, len(docs), batch_count):  # Usar 'idx' ao invés de 'i' para o loop externo
    batch = docs[idx:idx+batch_count]
    # A linha abaixo precisa ser corrigida para algo que faça sentido, como gerar embeddings para 'batch'
    # embeddings = chunk_embedding[batch]  # Esta linha parece incorreta conforme a explicação anterior.
    for i, chunk in enumerate(batch):
        # Supondo que 'embeddings' seja uma lista de vetores de embeddings gerados para cada 'chunk' no 'batch'
        vec = Vector(id=f"chunk-{idx+i}", vector=embeddings[i], metadata={"text": chunk})
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
