import streamlit as st
import openai as ai
from PyPDF2 import PdfReader
import logging
import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO)

nltk.download('punkt')
nltk.download('stopwords')

ai.api_key = st.secrets["openai_key"]

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_file.getvalue()))
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return ""

def save_feedback_to_file(user_name, feedback):
    try:
        with open("feedback_data.csv", "a") as file:
            file.write(f"{user_name},{feedback}\n")
        logging.info("Feedback saved successfully")
    except Exception as e:
        logging.error("Error saving feedback: " + str(e))
        st.error("An error occurred while saving feedback.")

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    keywords = [word for word in word_tokens if word.isalpha() and word not in stop_words]
    return set(keywords)

# Function to calculate match percentage
def calculate_match(resume_keywords, job_desc_keywords):
    match_keywords = resume_keywords.intersection(job_desc_keywords)
    total_keywords = len(job_desc_keywords)
    if total_keywords == 0:
        return 0
    match_percentage = len(match_keywords) / total_keywords * 100
    return match_percentage, match_keywords

st.markdown("# 📝 MyCoverKraft - Your Personalized Cover Letter Generator")

tab1, tab2 = st.tabs(["Resume Parser and Editor", "Cover Letter Generator"])


if 'cover_letter_generated' not in st.session_state:
    st.session_state.cover_letter_generated = False
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False

with tab1:
    st.title("Resume Parser and Editor")

    with st.expander("Instructions"):
        st.write("""
            - Fields marked with an asterisk (*) are mandatory.
            - Upload your resume 
            - Edit your resume 
            - Copy paste this resume in the cover letter generator
        """)

    # Upload PDF resume
    uploaded_file = st.file_uploader("Upload your resume* (PDF format)", type="pdf")

    if uploaded_file:
        # Extract text from the uploaded PDF file
        extracted_text = extract_text_from_pdf(uploaded_file)

        # Display the extracted text in an editable text area
        st.subheader("Extracted Resume Text")
        st.write("Review and edit the extracted text from your resume:")
        editable_text = st.text_area("Edit the text as needed:", extracted_text, height=300)

        # Button to confirm the edited text
        if st.button("Confirm Edited Text"):
            st.session_state.edited_resume_text = editable_text
            st.success("Resume text updated!")

with tab2:
    st.markdown("## Cover Letter Generator")
    with st.expander("Instructions"):
        st.write("""
                    - Fields marked with an asterisk (*) are mandatory.
                    - Upload your resume or copy your resume/experiences.
                    - Paste a relevant job description.
                    - Input other relevant data.
                    - Choose a cover letter style.
                """)
    # radio for upload or copy paste option
    res_format = st.radio(
        "Resume Input Method",
        ('Upload', 'Paste'),
        help="Choose how you'd like to input your resume.")

    with st.container():
        if res_format == 'Upload':
                res_file = st.file_uploader('📁 Upload your resume in pdf format')
                if res_file:
                    try:
                        pdf_reader = PdfReader(res_file)
                        res_text = ""
                        for page in pdf_reader.pages:
                            res_text += page.extract_text()
                    except Exception as e:
                        st.error("Error reading PDF file: " + str(e))

        else:
            res_text = st.text_input('Pasted resume elements')


        st.info(
            "Your data privacy is important. Uploaded resumes are only used for generating the cover letter and are not stored or used for any other purposes.")

        # Tone adjustment
        tone = st.selectbox('Select the Tone of Your Cover Letter',
                            ['Professional', 'Friendly', 'Enthusiastic', 'Formal', 'Casual'],
                            help="Choose the tone that best suits the company culture or job role.")

        # Including specific achievements or skills
        achievements = st.text_area('Include Specific Achievements, Skills or Keywords',
                                    help="Mention any key achievements or skills that make you a strong candidate for the role.")

        # Different letter structures
        letter_structure = st.radio('Choose Your Cover Letter Structure',
                                    ('Standard', 'Skill-based', 'Story-telling'),
                                    help="Select a structure that aligns with how you want to present your information.")

        with st.form('input_form'):
            job_desc = st.text_input('Job description*')
            user_name = st.text_input('Name*')
            company = st.text_input('Company name*')
            manager = st.text_input('Hiring manager')
            role = st.text_input('Job Role*')
            referral = st.text_input('How did you find out about this opportunity?')

            submitted = st.form_submit_button("Generate Cover Letter")


    if submitted and res_text and job_desc and user_name and company and role:
        try:

            customization_prompt = f"""
            Tone: {tone.lower()}
            Achievements/Skills: {achievements}
            Structure: {letter_structure.lower()}
            """
            completion = ai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature=0.99,
            messages = [
                {"role": "user", "content" : f"You will need to generate a cover letter based on specific resume and a job description"},
                {"role": "user", "content" : f"My resume text: {res_text}"},
                {"role": "user", "content" : f"The job description is: {job_desc}"},
                {"role": "user", "content" : f"The candidate's name to include on the cover letter: {user_name}"},
                {"role": "user", "content" : f"The job title/role : {role}"},
                {"role": "user", "content" : f"The hiring manager is: {manager}"},
                {"role": "user", "content" : f"How you heard about the opportunity: {referral}"},
                {"role": "user", "content" : f"The company to which you are generating the cover letter for: {company}"},
                {"role": "user", "content": customization_prompt},
                {"role": "user", "content" : f"The cover letter should have three content paragraphs"},
                {"role": "user", "content" : f""" 
                In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
                about it, and summarize what you have to offer based on the above resume
                """},
                    {"role": "user", "content" : f""" 
                In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
                and the qualifications on the job description.
                """},
                        {"role": "user", "content" : f""" 
                In the 3RD PARAGRAPH: Conclusion
              Restate your interest in the organization and/or job and summarize what you have to offer and thank the reader for their time and consideration.
                """},
                {"role": "user", "content" : f""" 
                note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
                    """},
                {"role": "user", "content" : f"Use {user_name} as the candidate"},

                {"role": "user", "content" : f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
            ]
            )

            response_out = completion['choices'][0]['message']['content']
            st.write(response_out)

            st.download_button(
                label="Download Cover Letter",
                data=response_out,
                file_name=user_name + "_cover_letter.txt",
                mime="text/plain"
            )

            st.session_state.cover_letter_generated = True
        except Exception as e:
            logging.error("Error in cover letter generation: " + str(e))
            st.error("An error occurred while generating the cover letter.")


    if st.session_state.cover_letter_generated and not st.session_state.feedback_submitted:
        feedback = st.slider("Rate the quality of the generated cover letter (1-5)", 1, 5, 3)
        if st.button("Submit Feedback"):
            save_feedback_to_file(user_name, feedback)
            st.success("Thank you for your feedback!")
            st.session_state.feedback_submitted = True