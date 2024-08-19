import os
import re

# Set the environment variable to avoid OpenMP initialization issues
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import faiss

# Load pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def text_to_vector(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Define example documents
documents = [
    {"id": "report1", "text": "Attendance report for July 2024 for employee A.", "vector": text_to_vector("Attendance report for July 2024 for employee A.").flatten(), "month": "July", "employees": ["A"]},
    {"id": "report2", "text": "Attendance report for July 2024 for employee B.", "vector": text_to_vector("Attendance report for July 2024 for employee B.").flatten(), "month": "July", "employees": ["B"]},
    {"id": "report3", "text": "Attendance report for August 2024 for employee A.", "vector": text_to_vector("Attendance report for August 2024 for employee A.").flatten(), "month": "August", "employees": ["A"]},
]

# Convert vectors to numpy array
vectors = np.array([doc['vector'] for doc in documents])
ids = [doc['id'] for doc in documents]
d = vectors.shape[1]  # Dimension of vectors

# Initialize Faiss index
index = faiss.IndexFlatL2(d)
index.add(vectors)

# Function to extract filters from user query
def extract_filters(query_text):
    month_match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', query_text, re.IGNORECASE)
    month = month_match.group(0) if month_match else None
    
    employees = re.findall(r'\b(employee\s+[A-Z])\b', query_text, re.IGNORECASE)
    employees = [emp.split(' ')[-1] for emp in employees]
    
    return month, employees

# User Query
query_text = "Show me report for July for employee A, B and C"
query_vector = text_to_vector(query_text).flatten()

# Perform the search
D, I = index.search(np.array([query_vector]), k=10)  # Search for top 10 results

# Get IDs of the most similar documents
similar_ids = [ids[idx] for idx in I[0]]

# Extract filters from the query
month_filter, employee_filters = extract_filters(query_text)

# Filter results based on metadata
filtered_results = [
    doc for doc in documents
    if doc['id'] in similar_ids and (month_filter is None or doc['month'].lower() == month_filter.lower())
    and (not employee_filters or any(emp in employee_filters for emp in doc['employees']))
]

# Print results
for result in filtered_results:
    print("Filtered Document:", result)
