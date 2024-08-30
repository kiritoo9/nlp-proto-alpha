from datetime import datetime, timedelta
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# this function will convert from user date:string into date:format
def date_convertion_handler(word: str):
    value = None
    now = datetime.now()
    converter = [
        {
            "key": ["today", "this day"],
            "value": now.strftime("%Y-%m-%d")
        }, {
            "key": ["this month"],
            "value": now.strftime("%Y-%m")
        }, {
            "key": ["this year"],
            "value": now.strftime("%Y")
        }, {
            "key": ["this week"],
            "value": [(now - timedelta(days=7)).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")]
        }
    ]

    for i in range(len(converter)):
        if word.lower() in converter[i].get("key"):
            value = converter[i].get("value")
            break

    # assumed the date is already have format
    # case: "%d %B %Y
    if value is None:
        try:
            date_obj = datetime.strptime(word, "%d %B %Y")
            value = date_obj.strftime("%Y-%m-%d")
        except ValueError as e:
            # means the format of this date doesn't match so skip it
            pass
            
    # case: %B %d, %Y
    if value is None:
        try:
            date_obj = datetime.strptime(word, "%B %d, %Y")
            value = date_obj.strftime("%Y-%m-%d")
        except ValueError as e:
            # means the format of this date doesn't match so skip it
            pass

     # case: %B %Y
    if value is None:
        try:
            date_obj = datetime.strptime(word, "%B %Y")
            value = date_obj.strftime("%Y-%m")
        except ValueError as e:
            # means the format of this date doesn't match so skip it
            pass

    # response
    return value


def extract_dates_and_range(text):
    # process the text with spaCy
    doc = nlp(text)
    
    # extract date entities
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    
    # identify keywords indicating a normal date or range date
    response = []
    range_keywords = ["to ", "until", "and"]
    unnecessary_keywords = ["between"]

    for i in range(len(dates)):
        separator = None
        date_str = dates[i].lower()

        # remove unnecessary words
        for j in range(len(unnecessary_keywords)):
            if unnecessary_keywords[j].lower() in date_str:
                date_str = date_str.replace(unnecessary_keywords[j], "").strip()
                break

        # find separator
        for j in range(len(range_keywords)):
            if range_keywords[j].lower() in date_str:
                separator = range_keywords[j].lower()
                break
        
        if separator is not None:
            response = [date_convertion_handler(word.lower().strip()) for word in date_str.split(separator) if word is not None]
        else:
            response.append(date_convertion_handler(date_str))

    # send response
    return response


# run process below when file executed
if __name__ == "__main__":
    # test cases
    texts = [
        "Show me the report for July 15, 2024",
        "Show me the report from July 1, 2024 to July 31, 2024",
        "Show me the report until August 15, 2024",
        "Show me the report between July 1, 2024 and July 31, 2024",
        "Show me the report between July 1, 2024 until July 31, 2024",
        "attendance report from 12 april 2024 until 12 august 2024",
        "attendance report this month",
        "attendance report this year",
        "attendance report this week",
        "attendance report last 3 months",
        "attendance report today",
    ]

    for text in texts:
        print(f"Text: {text}")
        response = extract_dates_and_range(text)
        print(response)
        print()
