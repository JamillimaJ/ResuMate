import re
import spacy
import pdfplumber  
import docx
import os

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip() 



def extract_text_from_docx(docx_path):
    doc =docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_name(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if names:
        cleaned_name = names[0].split("\n")[0]  
        cleaned_name = re.sub(r'\b(Phone|Email|Address|Skills)\b.*', '', cleaned_name, flags=re.IGNORECASE)         
        # cleaned_name = " ".join(cleaned_name.split()[:3])
        
        return cleaned_name.strip()

    return "Not Found"

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else "Not Found"

def extract_phone(text):
    match = re.search(r"\+?\d{1,3}[\s-]?\d{5,12}", text)
    return match.group() if match else "Not Found"

TECH_SKILLS_DB = [
    "Python", "Java", "JavaScript", "SQL", "C++", "Machine Learning", "Cloud", 
    "React", "Django", "HTML", "CSS", "Linux", "macOS", "Windows", "Documentation", 
    "Custom ROM", "Troubleshooting", "Technical Support"
]

def extract_skills(text):
    found_skills = [skill for skill in TECH_SKILLS_DB if skill.lower() in text.lower()]
    return found_skills if found_skills else "Not Found"

# Process Resume
def process_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"

    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
    }


file_path = input(" Enter the full path of the resume file (PDF or DOCX): ").strip()

if os.path.exists(file_path):
    print("\n File found! Extracting information...\n")
    resume_data = process_resume(file_path)

    print(" Extracted Resume Information:")
    for key, value in resume_data.items():
        print(f"{key}: {value}")

else:
    print("\n Error: File not found! Please check the file path and try again.")
