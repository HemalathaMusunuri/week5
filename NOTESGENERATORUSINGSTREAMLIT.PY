import streamlit as st
import re
import nltk
import pdfplumber
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

nltk.download('punkt')
nltk.download('stopwords')




st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1A2980, #26D0CE);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Page Config

st.set_page_config(page_title="Notes Generator", layout="centered")
st.title("📘 Notes Generator")


# PDF Reader

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# Text Cleaning

def clean_text(text):
    return re.sub(r'\n+', ' ', text).strip()


# Notes Generator

def generate_notes(text, limit=5):
    return sent_tokenize(text)[:limit]


# Mind Map Keywords

def extract_keywords(text, top_n=8):
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stopwords.words('english')]
    return Counter(words).most_common(top_n)


# Formula Extraction

def extract_formulas(text):
    return re.findall(r'[A-Za-z]+\s*=\s*[^,\n]+', text)


# Question Generator

def generate_questions(keywords):
    easy, medium, hard = [], [], []

    for k, _ in keywords[:5]:
        easy.append(f"Define {k}.")
        medium.append(f"Explain the concept of {k}.")
        hard.append(f"Discuss the importance of {k} with examples.")

    return easy, medium, hard


# PDF Export

def export_pdf(notes):
    file_name = "generated_notes.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()
    content = [Paragraph(n, styles["Normal"]) for n in notes]
    doc.build(content)
    return file_name


# Upload PDF

uploaded_pdf = st.file_uploader("📁 Upload Textbook PDF", type=["pdf"])

chapter_text = ""
if uploaded_pdf:
    chapter_text = read_pdf(uploaded_pdf)
    st.success("PDF uploaded successfully!")


# Manual Input (Optional)

manual_text = st.text_area("Or paste chapter text", height=200)

final_text = manual_text if manual_text.strip() else chapter_text


# Generate Button

if st.button("Generate Notes"):
    if final_text.strip() == "":
        st.warning("Please upload a PDF or enter text")
    else:
        text = clean_text(final_text)

        notes = generate_notes(text)
        keywords = extract_keywords(text)
        formulas = extract_formulas(text)
        easy, medium, hard = generate_questions(keywords)

        
        # Display Results
        
        st.subheader("📝 Notes")
        for n in notes:
            st.write(f"- {n}")

        st.subheader("🧠 Mind Map (Keywords)")
        for k, v in keywords:
            st.write(f"- {k} ({v})")

        st.subheader("📐 Key Formulas")
        st.write(formulas if formulas else "No formulas found")

        st.subheader("❓ Expected Exam Questions")

        st.markdown("**⭐ Easy**")
        for q in easy:
            st.write(f"- {q}")

        st.markdown("**⭐⭐ Medium**")
        for q in medium:
            st.write(f"- {q}")

        st.markdown("**⭐⭐⭐ Hard**")
        for q in hard:
            st.write(f"- {q}")

        
        # Export PDF
        
        pdf_file = export_pdf(notes)
        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download Notes as PDF", f, file_name=pdf_file)
