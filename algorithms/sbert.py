from dataclasses import replace
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = 'TRUE'

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# using SBERT:Similar Models
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
def text_to_vector(text):
    vector = model.encode([text])
    return vector / np.linalg.norm(vector, axis=1, keepdims=True)


# calling data models
from models import ReportTypes
from models import Employees

report_types = ReportTypes.report_types
report_types = [replace(rt, vector=text_to_vector(rt.vector).flatten()) for rt in report_types]

report_employees = Employees.employees
report_employees = [replace(re, vector=text_to_vector(re.vector).flatten()) for re in report_employees]


# perform search
def run_algorithm(data, user_vector, total_results, similarity_scores):
    # collects vectors
    vectors = np.array([v.vector for v in data])
    keys = [v.key for v in data]
    dimension = vectors.shape[1] # dimension of vectors

    # initialize Faiss index
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    # start searching
    D, I = index.search(np.array([user_vector]), k=total_results)

    # return the key
    return [keys[index] for index, score in zip(I[0], D[0]) if score >= similarity_scores]


# user input
# user_input = "show me attendance report for gusion, aamon"
user_input: str = input("Tell me what do u want?: ")
print("user inputted: ", user_input)
user_vector = text_to_vector(user_input.lower()).flatten()

# calling vectors
res_report_types = run_algorithm(report_types, user_vector, 1, 0.6)
res_report_employees = run_algorithm(report_employees, user_vector, 10, 0.2)

print("Report types possibility", res_report_types)
print("Employees possibility", res_report_employees)
