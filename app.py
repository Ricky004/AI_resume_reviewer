import streamlit as st
from utils.parser import extract_text_from_pdf
import google.generativeai as genai
import os


st.title("📄 Smart Resume Analyzer (Powered by Gemini)")

api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your Gemini API key to use the app.")
    st.stop()

# Step 2: Configure Gemini with user-provided API key
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Invalid API Key: {str(e)}")
    st.stop()

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text")
    st.text_area("", resume_text, height=300)

    if st.button("Analyze with Gemini AI"):
        with st.spinner("Analyzing..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = f"You are a career coach. Analyze the following resume:\n\n{resume_text}\n\nList the strengths, weaknesses, and suggestions to improve it."
                response = model.generate_content(prompt)
                st.success("✅ Analysis Complete")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    st.subheader("🔍 Match Resume to Job Description")

    job_desc = st.text_area("Paste a Job Description")

    if job_desc and st.button("Compare Resume to Job"):
        with st.spinner("Analyzing job fit..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = f"""
                    You're a hiring manager. Match the following resume to the job description.

                    1. Give a **fit score (0-100)** based on skill and experience alignment.
                    2. List **missing or weak skills**.
                    3. Suggest **how the resume can be improved to match** this job.

                    Resume:
                    {resume_text}

                    Job Description:
                    {job_desc}
                    """
                response = model.generate_content(prompt)
                st.success("✅ Match Analysis Complete")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")