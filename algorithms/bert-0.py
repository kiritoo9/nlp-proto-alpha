from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import faiss

# Set environment variable to handle OpenMP issue (if necessary)
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def encode(text):
    # Tokenize and encode the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    
    with torch.no_grad():
        # Get the last hidden state
        outputs = model(**inputs)
    
    # Average the token embeddings to get a single vector representation
    embeddings = outputs.last_hidden_state.mean(dim=1)
    
    return embeddings.numpy().astype(np.float32)

# NLP documents
documents = [
    "Attendance report for August",
    "Attendance report for July"
]

# NLP data models
nlp_models = {
    "1": {
        "table_name": "attendances",
        "month": 4
    },
    "0": {
        "table_name": "attendances",
        "month": 8
    },
}

# Encode documents
doc_vectors = np.vstack([encode(doc) for doc in documents])
print(doc_vectors)

# Create a Faiss index
dimension = doc_vectors.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add document vectors to the index
index.add(doc_vectors)

# Perform similarity search for each query
k = 2  # Number of nearest neighbors to retrieve

# Add user input and generate to query_vector
user_input = "show me for july"
query_vector = encode(user_input)

# Ensure query_vector is 2D
query_vector = query_vector.reshape(1, -1)

# Perform the search
result = index.search(query_vector, k)

# Handle the result
if isinstance(result, tuple) and len(result) == 2:
    distances, indices = result
    
    data_model_index = indices[0][0]
    print(nlp_models[str(data_model_index)])

    print("Nearest documents:")
    for j in range(k):
        print(f"Document: {documents[indices[0][j]]}, Distance: {distances[0][j]}")
else:
    print("Unexpected search result format:", result)

