import streamlit as st
import predictions
import utils
import fitz
from docx import Document
from wordcloud import WordCloud
import pandas as pd

# Function to toggle dark/light mode
def set_background_color(mode="light"):
    if mode == "dark":
        st.markdown(
            """
            <style>
                /* General body styles */
                body {
                    background-color: #121212;
                    color: #ffffff;
                    font-family: 'Roboto', sans-serif;
                    font-size: 18px;
                    line-height: 1.6;
                }

                /* Header and subheader styles */
                .header {
                    font-size: 36px;
                    color: #ffffff;
                    font-weight: 600;
                    padding-bottom: 20px;
                    text-align: center;
                }
                .subheader {
                    font-size: 24px;
                    color: #cccccc;
                    font-weight: 500;
                    text-align: center;
                }

                /* Sidebar styles */
                .sidebar .sidebar-content {
                    background-color: #1f1f1f;
                    color: #ffffff;
                    font-size: 18px;
                }
                .sidebar .sidebar-header {
                    color: #ffffff;
                    font-weight: 700;
                    font-size: 20px;
                    padding-bottom: 10px;
                }

                /* Button styles */
                .stButton button {
                    background-color: #00695C;
                    color: white;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 16px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                    transition: background-color 0.3s ease-in-out;
                }
                .stButton button:hover {
                    background-color: #004d40;
                    cursor: pointer;
                }

                /* Input field styles */
                .stTextInput input {
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                    background-color: #2c2c2c;
                    color: white;
                    border: none;
                    width: 100%;
                    box-sizing: border-box;
                }
                .stTextInput input:focus {
                    outline: none;
                    border: 2px solid #00bfae;
                }

                /* Word cloud container */
                .wordcloud-container {
                    text-align: center;
                    padding-top: 40px;
                }

                /* Footer styles */
                .footer {
                    font-size: 14px;
                    text-align: center;
                    color: #aaaaaa;
                    margin-top: 50px;
                }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <style>
                /* General body styles */
                body {
                    background-color: #f7f8fa;
                    color: #333333;
                    font-family: 'Roboto', sans-serif;
                    font-size: 18px;
                    line-height: 1.6;
                }

                /* Header and subheader styles */
                .header {
                    font-size: 36px;
                    color: #333333;
                    font-weight: 600;
                    padding-bottom: 20px;
                    text-align: center;
                }
                .subheader {
                    font-size: 24px;
                    color: #555555;
                    font-weight: 500;
                    text-align: center;
                }

                /* Sidebar styles */
                .sidebar .sidebar-content {
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 18px;
                }
                .sidebar .sidebar-header {
                    color: #333333;
                    font-weight: 700;
                    font-size: 20px;
                    padding-bottom: 10px;
                }

                /* Button styles */
                .stButton button {
                    background-color: #00bfae;
                    color: white;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 16px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: background-color 0.3s ease-in-out;
                }
                .stButton button:hover {
                    background-color: #008C7D;
                    cursor: pointer;
                }

                /* Input field styles */
                .stTextInput input {
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 16px;
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #dddddd;
                    width: 100%;
                    box-sizing: border-box;
                }
                .stTextInput input:focus {
                    outline: none;
                    border: 2px solid #00bfae;
                }

                /* Word cloud container */
                .wordcloud-container {
                    text-align: center;
                    padding-top: 40px;
                }

                /* Footer styles */
                .footer {
                    font-size: 14px;
                    text-align: center;
                    color: #888888;
                    margin-top: 50px;
                }
            </style>
            """, unsafe_allow_html=True)

# Title of the Streamlit app with custom styling
st.markdown("<h1 style='color: #1e90ff; font-size: 48px; text-align: center; font-weight: bold;'>SkillScape Resume Analyzer</h1>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Choose an option", ("Home", "About"))

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox('Dark Mode', value=False)
set_background_color("dark" if dark_mode else "light")

# Job recommendations based on skills
job_recommendations = {
    "Data Scientist": {
        "Description": "A Data Scientist uses machine learning and statistical techniques to analyze and interpret complex data to inform business decisions.",
        "Required Skills": ["Python", "SQL", "Machine Learning", "Data Analysis", "Statistics"]
    },
    "Full Stack Developer": {
        "Description": "A Full Stack Developer is responsible for both front-end and back-end development of web applications.",
        "Required Skills": ["HTML", "CSS", "Basics JavaScript", "React", "Node.js"]
    },
    "Software Engineer": {
        "Description": "A Software Engineer designs and develops software applications using programming languages and frameworks.",
        "Required Skills": ["Java", "Python", "C++", "Algorithms", "Problem Solving"]
    },
    "Machine Learning Engineer": {
        "Description": "A Machine Learning Engineer focuses on developing algorithms that allow computers to learn from data and make predictions.",
        "Required Skills": ["Python", "TensorFlow", "Machine Learning", "Deep Learning"]
    }
}

# Home Page
if option == "Home":
    st.sidebar.write("Upload a resume (PDF or DOCX) to extract key information.")

    # File uploader for PDFs and DOCX files with file size limit
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"], accept_multiple_files=False)
    
    if uploaded_file:
        if uploaded_file.size > 50 * 1024 * 1024:  # Limit: 50MB
            st.error("File size exceeds the 50MB limit. Please upload a smaller file.")
        else:
            # Placeholder for displaying results
            result_placeholder = st.empty()
            with st.spinner("Processing..."):
                filename = uploaded_file.name
                upload_image_path = utils.save_upload_image(uploaded_file)

                complete_text = ""
                if filename.endswith(".pdf"):
                    with fitz.open(upload_image_path) as doc:
                        for page in doc:
                            complete_text += page.get_text()

                elif filename.endswith(".docx"):
                    resume_text = Document(upload_image_path)
                    for p in resume_text.paragraphs:
                        complete_text += p.text

                # Predictions
                l, number, emails, years, name, found_skills = predictions.get_predictions(complete_text)

                # Displaying extracted information
                st.markdown(f"### **Name**: {name}")
                st.markdown(f"### **Email**: {emails}")
                st.markdown(f"### **Mobile Number**: {number}")
                if years:
                    st.markdown(f"### **Years of Experience**: {years}")
                else:
                    st.markdown(f"### **Years of Experience**: No experience")
                st.markdown(f"### **Skills**: {', '.join(found_skills)}")

                # Job recommendation based on skills
                st.markdown("### **Recommended Jobs**:")
                recommendations_displayed = False

                # Lowercase the skills for case-insensitive comparison
                found_skills_lower = [skill.lower() for skill in found_skills]

                for job, details in job_recommendations.items():
                    # Convert job's required skills to lowercase for comparison
                    matched_skills = set([skill.lower() for skill in details["Required Skills"]]).intersection(found_skills_lower)
                    
                    # Check if at least 3 skills match
                    if len(matched_skills) >= 3:
                        st.markdown(f"#### **{job}**")
                        st.markdown(f"**Description**: {details['Description']}")
                        st.markdown(f"**Matched Skills**: {', '.join(matched_skills)}")
                        st.markdown("---")
                        recommendations_displayed = True

                if not recommendations_displayed:
                    st.markdown("No job recommendations based on your skills.")

                # Display a word cloud for skills
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(found_skills))
                st.image(wordcloud.to_array(), caption="Skills Word Cloud", use_container_width=True)

                # Project name styling (increase font size, color)
                st.markdown(f"<h3 style='color: #1e90ff; font-size: 28px;'>**Project: Resume Parsing**</h3>", unsafe_allow_html=True)

                # Download as CSV
                csv = pd.DataFrame([{
                    "Name": name,
                    "Email": emails,
                    "Mobile": number,
                    "Experience": years if years else "No experience",
                    "Skills": ', '.join(found_skills)
                }])
                st.download_button("Download as CSV", csv.to_csv(index=False), "parsed_resume.csv", "text/csv")
