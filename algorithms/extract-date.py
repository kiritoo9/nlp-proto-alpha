import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_dates_and_range(text):
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract date entities
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    
    # Identify keywords indicating a range
    date_keywords = ["from", "to", "until", "between", "and"]
    keyword = next((word for word in date_keywords if word in text.lower()), None)
    
    if keyword:
        # Handle different keywords and extract start and end dates
        if keyword in ["from", "between"]:
            parts = text.split(keyword)
            if len(parts) == 2:
                # extracting valid date
                detected_date = parse_date(parts[1].strip())

                # splitting range date
                print(detected_date)
                parts = detected_date.split(keyword)
                print(parts)

                # parsing into date
                if len(parts) == 2:
                    start_date = parse_date(parts[0].strip())
                    end_date = parse_date(parts[1].strip())
                    return start_date, end_date

        return None, None
    else:
        # Single date
        return parse_date(text), None

def parse_date(text):
    # Parse the date using spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text
    return None

# Test cases
texts = [
    "Show me the report for July 15, 2024",
    "Show me the report from July 1, 2024 to July 31, 2024",
    "Show me the report until August 15, 2024",
    "Show me the report between July 1, 2024 and July 31, 2024",
    "Show me the report between July 1, 2024 until July 31, 2024"
]

for text in texts:
    print(f"Text: {text}")
    start_date, end_date = extract_dates_and_range(text)
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print()
