import os
os.environ["KMP_DUPLICATE_LIB_OK"] = 'TRUE'

import warnings
from dataclasses import replace
from spellchecker import SpellChecker
from googletrans import Translator
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from extract_date import extract_dates_and_range

print("loading LLM..")

# hide warning
warnings.simplefilter(action='ignore', category=FutureWarning)

# using SBERT:Similar Models
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
def text_to_vector(text):
    vector = model.encode([text])
    return vector / np.linalg.norm(vector, axis=1, keepdims=True)


# calling data models
from models import ReportTypes
from models import Employees
from models import Companies

report_types = ReportTypes.report_types
report_types = [replace(rt, vector=text_to_vector(rt.vector).flatten()) for rt in report_types]

report_employees = Employees.employees
report_employees = [replace(re, vector=text_to_vector(re.vector).flatten()) for re in report_employees]

report_companies = Companies.companies
report_companies = [replace(re, vector=text_to_vector(re.vector).flatten()) for re in report_companies]

# initialize requirement libraries
spell = SpellChecker()
translator = Translator()

# perform search
def run_algorithm(data, word_vector, total_results, similarity_scores):
    # collects vectors
    vectors = np.array([v.vector for v in data])
    keys = [v.key for v in data]
    dimension = vectors.shape[1] # dimension of vectors

    # initialize Faiss index
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    # start searching
    D, I = index.search(np.array([word_vector]), k=total_results)

    # return the key
    return [keys[index] for index, score in zip(I[0], D[0]) if score >= similarity_scores]


def check_word(word: str, res_report_types: [str], res_report_employees: [str], res_report_companies: [str]):
    # translate string into vector
    word_vector = text_to_vector(word.lower().strip()).flatten()

    # run algorithm for report types
    _rrt = run_algorithm(report_types, word_vector, 1, 0.6)
    if len(_rrt) > 0:
        for i in range(len(_rrt)):
            if _rrt[i] not in res_report_types:
                res_report_types.append(_rrt[i])

    # run algorithm for report employees
    _rre = run_algorithm(report_employees, word_vector, 10, 0.5)
    if len(_rre) > 0:
        for i in range(len(_rre)):
            if _rre[i] not in res_report_employees:
                res_report_employees.append(_rre[i])

    # run algorithm for report companies
    _rrc = run_algorithm(report_companies, word_vector, 10, 0.5)
    if len(_rrc) > 0:
        for i in range(len(_rrc)):
            if _rrc[i] not in res_report_companies:
                res_report_companies.append(_rrc[i])
    
    return res_report_types, res_report_employees, res_report_companies


def extraction(words: str):
    # split by space(s) into single word before generate:check the vector
    words = user_input.split(" ")

    res_report_types = []
    res_report_employees = []
    res_report_companies = []
    for i in range(len(words)):
        word = words[i]
        typo_possibility = False
        diff_lang_possibility = False

        while True:
            if typo_possibility:
                word = str(spell.candidates(word)) # check for the typo (now only support for english words)

            # perform to check each words
            res_report_types, res_report_employees, res_report_companies = check_word(word, res_report_types, res_report_employees, res_report_companies)
            if len(res_report_types) > 0 or len(res_report_employees) > 0 or len(res_report_companies) > 0:
                break
            else:
                # loop steps
                # 1. maybe language is different, so translate it
                # 2. check typo in original word:lang
                if diff_lang_possibility is False:
                    translated = translator.translate(words[i], dest="en") # use `words[i]` because I want to translate original word
                    if translated is not None:
                        word = translated.text

                    diff_lang_possibility = True
                elif diff_lang_possibility and typo_possibility is False:
                    word = words[i] # change word with original word (before translated)
                    typo_possibility = True
                elif typo_possibility and diff_lang_possibility:
                    break

    # response
    return res_report_types, res_report_employees, res_report_companies


def init(words: str, debug=True):
    if debug:
        print("user inputted: ", user_input)

    # run algorithm for main data
    res_report_types, res_report_employees, res_report_companies = extraction(user_input)

    if debug:
        # print response for core data
        print("\nReport types possibility: ", res_report_types)
        print("Employees possibility: ", res_report_employees)
        print("Companies possibility: ", res_report_companies)

    # run algorithm for date extraction
    user_input_translated = translator.translate(user_input).text.replace("'s","") # remove possesive pronoun
    date_extracted = extract_dates_and_range(user_input_translated)

    if debug:
        # log response for date extracted
        print("user input translatted: ", user_input_translated)
        print("Date parameter: ", date_extracted)

    if debug is False:
        # return as data for service purpose
        return {
            "cores": {
                "report_types": res_report_types,
                "report_employees": res_report_employees,
                "report_companies": res_report_companies,
            },
            "date_extraction": date_extracted
        }


# handle when user run from file directly
if __name__ == "__main__":
    while True:
        user_input: str = input("\nTell me what do u want?: ")

        # stop process condition
        if user_input.lower() == "exit":
            exit()
        
        # perform algorithm
        init(user_input)