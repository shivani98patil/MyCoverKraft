# Unit Testing for MyCoverKraft

This Section provides instructions on how to run the unit tests for the MyCoverKraft project.

## Getting Started

Before running the tests, make sure you have the necessary packages installed. You can install them using pip:
bash
pip install -r requirements.txt

## Running the Tests

To run the tests, navigate to the directory containing the test file (`test.py`) in your terminal or command prompt, and run the following command:
bash
python -m unittest test.py

This will run all the test cases defined in `test.py` and print the results to the console. Each test that passes is represented by a dot. If a test fails, it will be represented by an 'F', and an error message will be printed to help you debug the issue.

## Test Cases

The test file includes the following test cases:

1. `test_extract_text_from_pdf`: This test checks if the `extract_text_from_pdf` function correctly extracts text from a PDF file.

2. `test_save_feedback_to_file`: This test checks if the `save_feedback_to_file` function correctly saves feedback to a file.

3. `test_extract_keywords`: This test checks if the `extract_keywords` function correctly extracts keywords from a text.

4. `test_calculate_match`: This test checks if the `calculate_match` function correctly calculates the match percentage between a set of resume keywords and a set of job description keywords.

## Mocking

The tests use mocking to simulate the behavior of external systems like file I/O operations and PDF reading operations. This allows the tests to run quickly and reliably, without depending on the behavior of these external systems.

# Acceptance Testing for MyCoverKraft

Use Case: Generate a Cover Letter

This use case involves generating a cover letter using the MyCoverKraft application.
Execution Steps:

1. Open the MyCoverKraft application.
2. Navigate to the "Resume Parser and Editor" tab.
3. Upload a PDF resume using the "Upload your resume (PDF format)" button.
4. Review and edit the extracted text from your resume in the "Edit the text as needed:" text area.
5. Confirm the edited text by clicking the "Confirm Edited Text" button.
6. Navigate to the "Cover Letter Generator" tab.
7. Choose the "Paste" option for the "Resume Input Method".
8. Paste the confirmed edited text into the "Pasted resume elements" text box.
9. Select a tone for your cover letter from the "Select the Tone of Your Cover Letter" dropdown.
10. Enter any specific achievements, skills, or keywords into the "Include Specific Achievements, Skills or Keywords" text box.
11. Choose a structure for your cover letter from the "Choose Your Cover Letter Structure" radio buttons.
12. Fill in the rest of the form with the appropriate information (job description, name, company name, hiring manager, job role, and how you found out about the opportunity).
13. Click the "Generate Cover Letter" button.

#### Expected Output:

After clicking the "Generate Cover Letter" button, the application should generate a cover letter based on the information you provided. The cover letter should be displayed on the screen, and you should have the option to download it as a TXT, DOCX, or PDF file.

The generated cover letter should match the tone and structure you selected, include the specific achievements, skills, or keywords you entered, and be personalized with the information you provided in the form. The cover letter should not include any placeholders (like '[Your Name]') - all placeholders should be replaced with the appropriate information.

If any required fields are left blank, the application should display an error message prompting you to fill in the missing information.

### Use Case: Resume and Job Description Keyword Matcher

This use case involves matching keywords between a resume and a job description using the MyCoverKraft application.

#### Execution Steps:

1. Open the MyCoverKraft application.
2. Navigate to the "Resume and Job Description Keyword Matcher" tab.
3. Choose how to input your resume: either upload a PDF resume using the "Upload PDF" option, or paste the resume text using the "Paste Text" option.
4. Paste the job description into the "Paste the Job Description" text area.
5. Click the "Match Keywords" button.
Expected Output:

After clicking the "Match Keywords" button, the application should calculate the match percentage between the keywords in the resume and the job description. The application should display the matched keywords.

If either the resume or the job description is not provided, the application should display an error message prompting you to input both the resume and the job description.
