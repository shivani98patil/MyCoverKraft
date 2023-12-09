# MyCoverKraft

## Introduction

**MyCoverKraft** redefines the process of crafting personalized cover letters for job applications. In today's competitive job market, a compelling cover letter plays a pivotal role in distinguishing candidates. Our application aims to bridge the gap between generic cover letters and context-rich representations of an individual's skills, experiences, and career aspirations.

By harnessing advanced language processing and tailored prompts, **MyCoverKraft** empowers users to generate cover letters that surpass traditional templates. The focus is on understanding the intricate nuances of diverse professions, enabling job seekers to create compelling, personalized cover letters that resonate deeply with potential employers.

From parsing resumes to synthesizing job descriptions, **MyCoverKraft** intelligently amalgamates this information to craft bespoke cover letters, significantly enhancing a candidate's prospects of securing interviews and landing coveted positions. Our tool is poised to streamline the application process, ensuring candidates stand out in a competitive landscape.

## Deployment

The MyCoverKraft application has been deployed and is accessible at [MyCoverKraft](https://mycoverkraft.streamlit.app/).


## Getting Started

Before running the tests, make sure you have the necessary packages installed. You can install them using pip:

1. **Ensure Python is installed on your system.**

2. **Create a virtual environment:**

    ```
    python -m venv venv
    ```

3. **Activate the virtual environment and install the dependencies:**

    ```
    venv\Scripts\activate  # For Windows
    source venv/bin/activate  # For macOS/Linux
    pip install -r requirements.txt
    ```

4. **Run the project:**

    ```
    streamlit run app.py
    ```

5. **Handling the API Key:**

   To use the project functionalities that require an API key, you'll need to acquire an API key and place it in a `secrets.toml` file. Here's how you can set it up:

   - Obtain your API key from [API Provider].
   - Create a `secrets.toml` file in the root directory of your project.
   - Add your API key to `secrets.toml` in the following format:

     ```toml
     [api]
     key = "YOUR_API_KEY_HERE"
     ```

   Make sure to replace `"YOUR_API_KEY_HERE"` with your actual API key.


# Project Structure

- `app.py`: The main Streamlit application.
- `feedback_data.csv`: Contains all the feedback provided by the user.
- `requirements.txt`: Contains all the required libraries needed to run this project.
- `README.md`: This file.

# Unit Testing for MyCoverKraft

This section provides instructions on how to run the unit tests for the MyCoverKraft project.

## Why Unit Test?

Testing isn't just a suggestion; it's a crucial skill for any developer. It helps you:

- Catch bugs early: Identify and fix problems before they reach users.
- Prevent regressions: Ensure changes don't break existing functionality.
- Build confidence: Gain trust in your code's quality and stability.

It ensures you are building the thing, right.

## Running the Tests

To run the tests, navigate to the directory containing the test file `test.py` in your terminal or command prompt, and run the following command:

     python -m unittest test.py



This command will execute all the test cases defined in `test.py` and display the results in the console. Each passing test will be represented by a dot, while any failed test will be indicated by an 'F', accompanied by an error message for debugging purposes.


## Test Cases

The test file includes the following test cases:

1. `test_extract_text_from_pdf`: This test checks if the `extract_text_from_pdf` function correctly extracts text from a PDF file.
   
2. `test_save_feedback_to_file`: This test checks if the `save_feedback_to_file` function correctly saves feedback to a file.
   
3. `test_extract_keywords`: This test checks if the `extract_keywords` function correctly extracts keywords from a text.
   
4. `test_calculate_match`: This test checks if the `calculate_match` function correctly calculates the match percentage between a set of resume keywords and a set of job description keywords.

## Mocking

The tests use mocking to simulate the behavior of external systems like file I/O operations and PDF reading operations. This allows the tests to run quickly and reliably, without depending on the behavior of these external systems.


# Acceptance Testing: Generating Cover Letter using MyCoverKraft

## Why Acceptance Testing?

Acceptance testing is a critical phase that validates whether the application meets the specified business requirements and functions as expected in a real-world scenario. It ensures that the generated cover letter aligns with the user's input, job description, and resume details. By performing acceptance testing, potential issues or discrepancies in the cover letter generation process can be identified early, leading to improved application reliability and user satisfaction.

## Use Case Description

This use case involves generating a cover letter using the MyCoverKraft application.

### Execution Steps

1. Open the MyCoverKraft application.
2. Navigate to the "Cover Letter Generator" tab.
3. Upload a PDF resume using the "Upload" button.
4. Choose the "Paste" option for the "Resume Input Method".
5. Enter any specific achievements, skills, or keywords into the "Include Specific Achievements, Skills or Keywords" text box.
6. Select a tone for your cover letter from the "Choose Your Cover Letter Structure" radio buttons.
7. Fill in the rest of the form with the appropriate information (job description, name, company name, hiring manager, job role, and how you found out about the opportunity).
8. Click the "Generate Cover Letter" button.

### Expected Output or Behavior

- The MyCoverKraft application should generate a cover letter based on the provided resume details, additional input (achievements, skills, keywords), and form information.
- The generated cover letter should display the selected tone and include relevant details as per the form entries.
- The system should allow users to review the generated cover letter.

### Example or Screenshot 

- <img width="800" alt="Screenshot 2023-12-08 at 10 38 30 PM" src="https://github.com/shivani98patil/MyCoverKraft/assets/142866037/7489a48c-42a9-4aa8-a171-21fd6bef6ca6">
- <img width="800" alt="Screenshot 2023-12-08 at 10 38 49 PM" src="https://github.com/shivani98patil/MyCoverKraft/assets/142866037/6be2f8e9-0233-4c31-91bb-e01bc1f60ca1">
- <img width="800" alt="Screenshot 2023-12-08 at 10 37 30 PM" src="https://github.com/shivani98patil/MyCoverKraft/assets/142866037/fd561056-b96f-4c9a-ac81-a327538ede42">
- <img width="800" alt="Screenshot 2023-12-08 at 10 37 41 PM" src="https://github.com/shivani98patil/MyCoverKraft/assets/142866037/4792c2c7-767d-47fa-af2d-0a675b5e7f83">

## Execution Verification

Follow these steps to:
- Generate a cover letter using the MyCoverKraft application.
- Review the generated cover letter to ensure it aligns with the provided resume details and form information.

## Postconditions

- Users should have access to a generated cover letter tailored based on the provided resume details and additional input.
- The system should provide an intuitive and accurate cover letter generation process within the MyCoverKraft application.
