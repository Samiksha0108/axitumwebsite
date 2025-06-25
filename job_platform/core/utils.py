def is_candidate(request):
    """
    True if this request was authenticated via the 'candidates' DB.
    Your SplitLoginBackend already sets user._state.db.
    """
    return getattr(request.user._state, "db", "") == "candidates"

import os
import fitz  # PyMuPDF
from docx import Document
import spacy
import nltk
from nltk.corpus import stopwords
import string

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Ensure necessary NLTK resources are downloaded
# nltk.download("punkt")
# nltk.download("stopwords")

# Stopwords and punctuation
stop_words = set(stopwords.words("english"))
punctuation = set(string.punctuation)

# === Text Extraction ===
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

# === Hybrid Keyword Extractor ===
def extract_keywords(text):
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if (
                                
            token.lemma_ not in stop_words and    # remove stopwords
            token.lemma_ not in punctuation and
            len(token.lemma_) > 2 and             # filter very short words
            token.pos_ in ["PROPN"]       # retain only informative nouns
        ):
            keywords.add(token.lemma_)
    
    return keywords

# === Keyword Matcher ===
def match_resume_to_job(resume_text, job_desc_text):
    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(job_desc_text)
    matched = resume_kw & jd_kw
    score = len(matched)
    return round(score, 2), matched


# utils.py (or put in views.py directly if you don’t have utils)

import calendar
from datetime import date, timedelta

def get_month_days(year, month):
    cal = calendar.Calendar(firstweekday=6)
    month_days = []
    for week in cal.monthdatescalendar(year, month):
        month_days.append([
            {
                "date": day,
                "in_month": (day.month == month)
            }
            for day in week
        ])
    return month_days



# utils.py

from django.shortcuts import redirect

def company_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('company_user_id'):
            return redirect('company_login')  # <-- your company login URL name
        return view_func(request, *args, **kwargs)
    return wrapper
