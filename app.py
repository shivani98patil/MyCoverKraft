import streamlit as st
import openai as ai
from docx import Document
from fpdf import FPDF
from PyPDF2 import PdfReader
from io import BytesIO
import logging
import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import date

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

tab1, tab2, tab3 = st.tabs(["Resume Parser and Editor", "Cover Letter Generator", "Resume and Job Description Keyword Matcher"])

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


    def get_state():
        if 'state' not in st.session_state:
            st.session_state['state'] = AppState()
        return st.session_state['state']


    def create_text_file(cover_letter):
        return cover_letter.encode('utf-8')


    def create_docx(response_out):
        doc = Document()
        doc.add_paragraph(response_out)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer


    def create_pdf(response_out):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, response_out)
        buffer = BytesIO()
        pdf.output(dest='S').encode('latin1')  # 'S' returns the PDF as a string
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)
        return buffer.getvalue()


    class AppState:
        def __init__(self):
            self.file_data1 = None
            self.file_data2 = None
            self.file_data3 = None

        def generate_files(self, data):
            self.file_data1 = create_text_file(data)
            self.file_data2 = create_docx(data)
            self.file_data3 = create_pdf(data)


    state = get_state()


    if submitted :
        if res_text and job_desc and user_name and company and role:
            try:

                customization_prompt = f"""
                Tone: {tone.lower()}
                Achievements/Skills: {achievements}
                Structure: {letter_structure.lower()}
                """
                completion = ai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature=0.99,
                    messages=[
                        {"role": "user",
                         "content": f"You will need to generate a cover letter based on specific resume and a job description"},
                        {"role": "user", "content": f"My resume text: {res_text}"},
                        {"role": "user", "content": f"The job description is: {job_desc}"},
                        {"role": "user",
                         "content": f"The candidate's name to include on the cover letter: {user_name}"},
                        {"role": "user", "content": f"The job title/role : {role}"},
                        {"role": "user", "content": f"The hiring manager is: {manager}"},
                        {"role": "user", "content": f"How you heard about the opportunity: {referral}"},
                        {"role": "user",
                         "content": f"The company to which you are generating the cover letter for: {company}"},
                        {"role": "user", "content": customization_prompt},
                        {"role": "user", "content": f"The cover letter should have three content paragraphs"},
                        {"role": "user",
                         "content": "Please replace all placeholders with the specific details provided. For example, replace '[Your Name]' with the user's actual name."},
                        {"role": "user", "content": f"Do not include {user_name} in the starting"},
                        {"role": "user", "content": f""" 
                    In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
                    about it, and summarize what you have to offer based on the above resume
                    """},
                        {"role": "user", "content": f""" 
                    In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
                    and the qualifications on the job description.
                    """},
                        {"role": "user", "content": f""" 
                    In the 3RD PARAGRAPH: Conclusion
                  Restate your interest in the organization and/or job and summarize what you have to offer and thank the reader for their time and consideration.
                    """},
                        {"role": "user", "content": f""" 
                    note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
                        """},
                        {"role": "user", "content": "Use" + user_name + "as the candidate"},
                        {"role": "user",
                         "content": "Only put Date before Dear Hiring Manager. Do not include your name and and Company name or any additional information."},

                        {"role": "user",
                         "content": f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
                    ]
                )

                response_out = completion['choices'][0]['message']['content']
                if manager:
                    response_out = response_out.replace('[Hiring Manager]', manager)
                else:
                    response_out = response_out.replace('[Hiring Manager]', 'Hiring Manager')

                response_out = response_out.replace('[Recipient\'s Name]', manager if manager else 'Hiring Manager')
                response_out = response_out.replace('[Your Name]', user_name if user_name else 'Your Name')
                response_out = response_out.replace('[Job description*]', job_desc)
                response_out = response_out.replace('[Company Name]', company)
                response_out = response_out.replace('[Job Role*]', role)
                today_date = date.today()
                today_date_str = today_date.strftime("%B %d, %Y")
                response_out = response_out.replace('[Today\'s Date]', today_date_str)
                response_out = response_out.replace('[Today’s Date]', today_date_str)
                response_out = response_out.replace('[Date]', today_date_str)
                response_out = response_out.replace('[Company Address]', '')
                response_out = response_out.replace('[Your Address]', '')
                response_out = response_out.replace('[City, State, ZIP Code]', '')
                response_out = response_out.replace('[City, State, ZIP]', '')
                response_out = response_out.replace('[Email Address]', '')
                response_out = response_out.replace('[Phone Number]', '')
                response_out = response_out.replace('[Your Contact Information]', '')
                response_out = response_out.replace('[How did you find out about this opportunity?]', referral)

                st.write(response_out)
                state.generate_files(response_out)
                st.session_state.cover_letter_generated = True

            except Exception as e:
                logging.error("Error in cover letter generation: " + str(e))
                st.error("An error occurred while generating the cover letter.")
        else:
            st.error("Please fill in all the required fields.")


    col1, col2, col3 = st.columns(3)

    if state.file_data1:
        with col1:
            st.download_button('Download TXT', state.file_data1, user_name+'_cover_letter.txt', 'text/plain')

    if state.file_data2:
        with col2:
            st.download_button('Download DOCX', state.file_data2, user_name+'_cover_letter.docx',
                               'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    if state.file_data3:
        with col3:
            st.download_button('Download PDF', state.file_data3, user_name+'_cover_letter.pdf', 'application/pdf')


    if st.session_state.cover_letter_generated and not st.session_state.feedback_submitted:
        feedback = st.slider("Rate the quality of the generated cover letter (1-5)", 1, 5, 3)
        if st.button("Submit Feedback"):
            save_feedback_to_file(user_name, feedback)
            st.success("Thank you for your feedback!")
            st.session_state.feedback_submitted = True

with tab3:
    st.title("Resume and Job Description Keyword Matcher")
    with st.expander("Instructions"):
        st.write("""
                    - Fields marked with an asterisk (*) are mandatory.
                    - Upload your resume or copy your resume/experiences.
                    - Paste a relevant job description.
                    - Input other relevant data.
                    - Choose a cover letter style.
                """)
    # radio for upload or copy paste option
    resume_input_method = st.radio(
        "Choose how to input your resume:",
        ('Upload PDF', 'Paste Text'),
        key='resume_input_method'
    )

    resume_text = ""
    if resume_input_method == 'Upload PDF':
        uploaded_file = st.file_uploader("Upload your resume* ", type="pdf", key='resume_uploader')
        if uploaded_file:  # Check if the file is uploaded
            resume_text = extract_text_from_pdf(uploaded_file)
    elif resume_input_method == 'Paste Text':
        resume_text = st.text_area("Paste Your Resume Here", height=200, key='resume_textarea')

    job_desc_text = st.text_area("Paste the Job Description", height=200)

    if st.button('Match Keywords'):
        if resume_text and job_desc_text:
            # Extract keywords
            resume_keywords = extract_keywords(resume_text.lower())
            job_desc_keywords = extract_keywords(job_desc_text.lower())

            # Calculate match
            match_percentage, matched_keywords = calculate_match(resume_keywords, job_desc_keywords)

            st.write(f"Match Percentage: {match_percentage:.2f}%")
            st.write("Matched Keywords:", matched_keywords)
        else:
            st.error("Please input both the resume and the job description.")