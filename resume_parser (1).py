# -*- coding: utf-8 -*-
"""Resume Parser.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vnX4JYMyQ3aLzQtyXYdPzcFkqGp0C02w
"""

!pip install pymupdf
import fitz
import nltk
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
nltk.download('stopwords')

# getting a file and reading the contents of the file or the resume we want
#pdf_path = "Graduate Admission Centre Form (only for Bachelor's Degree) (1).docx"
pdf_path = "Swanand_Wagh_Resume (1).docx"
document = fitz.open(pdf_path)

text = ""
for page_num in range(document.page_count):
  pages = document[page_num]
  text+=pages.get_text()

document.close()
print(text)

"""Since we now have the entire text with us, we now extract the main keywords from the given text"""

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
tokens = word_tokenize(text)
sentences = sent_tokenize(text)
print(tokens)
print()

for sentence in sentences:
  print(sentence)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
wc = WordCloud().generate(text)
plt.figure(figsize=(15,15))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(sentences)
feature_names = vectorizer.get_feature_names_out()
tfidf_vector = tfidf_matrix[0]

tfidf_dict = dict(zip(feature_names, tfidf_vector.toarray().flatten()))
most_frequent_words = {k: v for k, v in sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)}
print(most_frequent_words)

# Using Bag of Words
vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform([text])
print("Feature names:", vectorizer.get_feature_names_out())
print("Bag of Words matrix:\n", bow_matrix.toarray())
features = vectorizer.get_feature_names_out()
print(features)

#Getting the number of times a particular keyword is appearing in the resume
def getKeyWords(inputWords, features):
  wordCount = 0
  for element in features:
    if element == inputWords:
      wordCount+=1
  print(wordCount)

getKeyWords('engineering', features)

import re

date_pattern = r'\b(?:\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b[- ]?\d{2,4})\b'
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
phone_pattern = r'(\+\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'

job_titles = ["Software Engineer", "Data Scientist", "Project Manager", "Machine Learning Engineer", "SDE"]
skills_list = ["Python", "Java", "Machine Learning", "NLP", "Data Analysis", "React JS"]

all_emails = []
all_phone_numbers = []
all_dates = []

def extract_dates(sentence):
    return re.findall(date_pattern, sentence)

def extract_emails(sentence):
    return re.findall(email_pattern, sentence)

def extract_phone_numbers(sentence):
    return re.findall(phone_pattern, sentence)

for sentence in sentences:
  emails = extract_emails(sentence)
  phone_numbers = extract_phone_numbers(sentence)
  dates = extract_dates(sentence)

  all_emails.extend(emails)
  all_phone_numbers.extend(phone_numbers)
  all_dates.extend(dates)

print(all_emails)
print(all_dates)

import spacy

# Load pretrained spaCy model
nlp = spacy.load("en_core_web_sm")

job_titles = ["Software Engineer", "Data Scientist", "Project Manager", "Machine Learning Engineer", "SDE", "Technology Analyst", "Software Development Engineer Intern"]
skills_list = ["Python", "Java", "Machine Learning", "NLP", "Data Analysis", "React JS"]

doc = nlp(text)

# Initialize lists to hold detected skills and job titles
extracted_skills = []
extracted_job_titles = []

for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# Check for job titles and skills in the text
for token in doc:
    if token.text in skills_list:
        extracted_skills.append(token.text)
    if token.text in job_titles:
        extracted_job_titles.append(token.text)

# Print extracted skills and job titles
print("\nExtracted Skills:", extracted_skills)
print("Extracted Job Titles:", extracted_job_titles)

import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker_tab')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Function to extract email using regex
def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    emails = re.findall(email_pattern, text)
    return emails

# Function to extract phone number using regex
def extract_phone(text):
    phone_pattern = r'\+?\(?\d{1,4}?\)?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}'
    phone_numbers = re.findall(phone_pattern, text)
    return phone_numbers

# Function to extract skills based on common keywords (this can be extended)
def extract_skills(text):
    skills_keywords = ['Python', 'Java', 'C++', 'SQL', 'JavaScript', 'HTML', 'CSS', 'Machine Learning', 'Data Analysis', 'Deep Learning', 'TensorFlow', 'Pandas']
    skills = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    return skills

# Function to extract named entities using NLTK's Named Entity Recognition
def extract_entities(text):
    sentences = sent_tokenize(text)
    named_entities = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        named_entities_tree = ne_chunk(pos_tags)

        # Extract named entities (persons, locations, etc.)
        for chunk in named_entities_tree:
            if isinstance(chunk, nltk.Tree):
                entity = " ".join([word for word, tag in chunk])
                named_entities.append(entity)

    return named_entities

# Function to parse the resume and extract details
def parse_resume(resume_text):
    # Extract email and phone number
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    # Extract skills
    skills = extract_skills(resume_text)

    # Extract named entities (name, organizations, etc.)
    entities = extract_entities(resume_text)

    # Display parsed information
    parsed_data = {
        'Email': email,
        'Phone': phone,
        'Skills': skills,
        'Entities': entities
    }

    return parsed_data

# Parse the resume text
parsed_resume = parse_resume(text)

# Output parsed information
print("Parsed Resume Data:")
for key, value in parsed_resume.items():
    print(f"{key}: {value}")

def extract_name_from_resume(s):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern,s)
    if match:
        name = match.group()
    return name


def extract_contact_number_from_resume(s):
    contact_number = None
    pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|\d{5}[-\.\s]??\d{4})"
    match = re.search(pattern, s)
    if match:
        contact_number = match.group()
    return contact_number

def extract_education_from_resume(s):
    education = []
    pattern = r"(?i)(?:Bsc|\bM\.\[A-Za-z]+|\bPh\.D\.\[A-Za-z]+|\bBachelor(?:'s)?|\bBachelors(?:'s)?|\bMaster(?:'s)?|\bMasters(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+|B\.[A-Za-z]+"
    matches = re.findall(pattern, s)
    for match in matches:
        education.append(match.strip())
    return education

def extract_gpa_from_resume(s):
    gpa = None
    pattern = r'[0-9]+\.\d?(\d)'
    match = re.search(pattern,s)
    if match:
        gpa = match.group()
    return gpa

def extract_skills_from_resume(s, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, s, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

print("Name:", extract_name_from_resume(text))
print("Contact Number:", extract_contact_number_from_resume(text))
print("Education:", extract_education_from_resume(text))
print("CGPA:", extract_gpa_from_resume(text))

skills_list =  ['frontend','HTML', 'HTML5', 'CSS', 'CSS3', 'React','ReactJS','Angular','AngularJS','jQuery','Frameworks','Version Control','Responsive Design','UI','UX','UI/UX','REST','SEO','Communication','Teamwork','Creativity','Problem Solving','Quick Learner','Attention to Detail','Collaboration','Problem Solving','Writing Skills','Prototype','Troubleshoot','Optimization', 'Graphic Design', 'Testing', 'Debugging','Deployment', 'Web Development','Content Management','Fast Paced','Analytical', 'Multitasking','Java','Python']
print("Skills that match specified role:", extract_skills_from_resume(text, skills_list))

jobRoles = {
    'Frontend Engineer' : ['frontend','HTML', 'HTML5', 'CSS', 'CSS3', 'React','ReactJS','Angular','AngularJS','jQuery','Frameworks','Version Control','Responsive Design','UI','UX','UI/UX','REST','SEO','Communication','Teamwork','Creativity','Problem Solving','Quick Learner','Attention to Detail','Collaboration','Problem Solving','Writing Skills','Prototype','Troubleshoot','Optimization', 'Graphic Design', 'Testing', 'Debugging','Deployment', 'Web Development','Content Management','Fast Paced','Analytical', 'Multitasking'],
    'Backend Engineer' : ['backend','Java','Python','Ruby','Javascript','HTML','HTML5','CSS','CSS3','PHP','Database Management','APIs','Data Structures and Algorithms','CMS','Communication','Teamwork','Collaboration','Problem Solving','Time Management','Critical Thinking','Attention to Detail','Management','Troubleshoot','Debugging','Deployment','Web Development','UI','UX','UI/UX','Collboration','Reusable Code','Analytical','Time Management','Teamwork','Problem Solving'],
    'Fullstack Developer' : ['fullstack','HTML','HTML5','CSS','CSS3','JavaScript','XML','jQuery','Java','Python','PHP','C#','React','ReactJS','Angular','AngularJS','Git/Github','APIs','MySQL','MongoDB','Apache','Frameworks','Version Control','Responsive Design','UI/UX','UI','UX','REST','SEO','Communication','Teamwork','Collaboration','Problem Solving','Time Management','Critical Thinking','Attential to Detail','Management','Creativity','Problem Solving','Client Side Architecture','Server Side Architechture','Responsiveness','Responsive Design','Efficiency','Troubleshoot','Debug','Organizational','Analytical'],
    'Software Engineer' : ['software','Java','Ruby on Rails','C++','Python','Database Management','Data Structures and Algorithms','Object Oriented Programming','Operating Systems','Frameworks','ORM','SQL','JavaScript','Communication','Critical Thinking','Adaptability','Problem Solving','Teamwork','Collaboration','Time Management','SDLC','Problem Solving','Testing','Feasibility','Integration','Quality Assurance','Troubleshoot','Debug','Deployment','Documentation'],
    'Cybersecurity Engineer' : ['cybersecurity','Network Security','Software Testing','Operating Systems','Digital Forensics','Security Auditing','Ethical Hacking','Cloud Security','Communication','Collaboration','Critical Thinking','Adaptability','Problem Solving','Attention to Detail','Security Control','Security Requirements','Performance Reports','Network Data Analysis','Vulnerability Scanning Solutions','Antivirus Software','Security Software'],
    'Blockchain Engineer' : ['blockchain','C++', 'Golang', 'Java', 'Cryptography', 'Network Security', 'Data Structures', 'Blockchain Architecture', 'Web Development', 'Communication', 'Collaboration', 'Critical Thinking', 'Adaptability', 'Problem Solving', 'Attention to Detail','Blockchain','Client and Server Side Applications','Software Development','Open Source Projects', 'JavaScript','Data Structures','Cryptography','P2P','Bitcoin','Concurrency','Writing efficient','Safe Multithreaded Code'],
    'DevOps Engineer' : ['devops','Python', 'JavaScript', 'Ruby', 'Automation', 'Security', 'Software Testing', 'Linux', 'Scripting', 'System Integration', 'Cloud Skills', 'Risk Assessment', 'CI/CD','Communication', 'Management', 'Collaboration', 'Decision-Making', 'Problem Solving', 'Adaptability','Integrations','Level 2 Technical Support','Backend','Root Cause Analysis','System Troubleshooting','Maintenance','DevOps Engineer','SQL','Teamwork'],
    'Android Developer' : ['Android Studio', 'Android SDK', 'Android Testing', 'APIs', 'Java', 'Kotlin', 'XML', 'SQL', 'Firebase', 'JSON', 'Design', 'Git/GitHub', 'UI/UX', 'Version Control', 'Communication', 'Problem Solving', 'Collaboration', 'Time Management','Unit-Test code ','Bug Fixing ','Android','Android SDK','REST', 'JSON','Mobile Development'],
    'Database Administrator' : ['dba','SQL', 'LINUX', 'Oracle', 'UNIX', 'Microsoft Access', 'Windows OS', 'HTML','Communication', 'Problem Solving', 'Organization', 'Analytics', 'Business – focus','Design Database ','Implement Database','Data Security', 'Privacy', 'Integrity','Database Administrator','Database Standards ','Data Backup', 'Data Recovery', 'Data Security','Database Design','Documentation','Coding','DBA tools'],
    'Data Analyst' : ['SQL', 'R', 'Python', 'Tableau', 'Microsoft Excel', 'Mathematical Skills', 'Data Cleaning','Presentation', 'Critical Thinking', 'Communication', 'Problem Solving','Statistical Techniques','Data Collection Systems', 'Analytics','Data Analyst','Business Data Analyst','Data Models', 'Database Design Development', 'Data Mining','Segmentation Techniques','XML', 'JavaScript', 'ETL frameworks','Excel', 'SPSS', 'SAS','Analytical skills','Queries','Report Writing','Presenting Skills'],
    'Data Scientist' : ['Python', 'R', 'SQL', 'Mongo DB', 'MySQL', 'Regression', 'Vector Models', 'Tableau', 'Power BI', 'DS.js', 'BeautifulSoup', 'Pandas', 'Spacy', 'Machine Learning', 'Artificial Intelligence', 'NLP', 'Hadoop', 'Spark','Problem solving', 'Effective Communication', 'Intellectual Curiosity', 'Business Sense','Predictive Models ','Machine Learning Algorithms','Data Visualization','Data Scientist', 'Data Analyst','Data Mining','Scala', 'Java', 'C++','Communication','Presentation Skills'],
    'Data Engineer' : ['Python', 'Java', 'Scala', 'PostgreSQL', 'NoSQL', 'Hadoop', 'Spark', 'Apache Kafka', 'Azure', 'Google Cloud', 'Git', 'Amazon Redshift', 'BigQuery','Communication', 'Collaboration', 'Critical Thinking','Prescriptive and Predictive modeling','Algorithms','Prototypes','Data quality and reliability','Data engineer','data models', 'data mining', 'segmentation techniques','Great numerical and analytical skills'],
    'Business Analyst' : ['SQL','R','Python','SPSS','SAS','Sage','Mathematics','Excel','Power BI','Tableau','Communication','Presentations','Problem Solving','Critical Thinking','Negotiation','Adaptability','Business Intellect','Reporting and Alerting','System Analysis','Maintain System','Quality Assurace','Visualization','Key Performance Indicators','Reporting','Writing Skills','Technical Writing'],
    'Machine Learning Engineer' : ['Statistcal Analysis','Probability','Machine Learning','Model Evaluation','DevOps','CI/CD','AWS','Azure','Google Cloud Platform','Python','C++','Java','Communication','Problem Solving','Adaptability','Data Science Prototypes','Data Representation','Train Systems','Scikit Learn','Tensorflow','Keras','PyTorch','Data Structures','Data Modelling','Software Architecture','MathS','Probability','Python','R','Communication','Teamwork','Analytical Skills','Problem Solving'],
    'Artificial Intelligence Engineer' : ['Python', 'Java', 'R', 'C++','JavaScript','SQL','NoSQL','Apache Spark','Hadoop','SparkSQL','Apache Flink', 'Google Cloud Platform','AWS Azure','ML Models','AI Models','Communication','Collboration','Adaptability','Critical Thinking','Problem Solving','Domain Knowledge','Staistical Analysis','Algorithmic Models','Linear Algebra','Probability','Efficient Code','Big Data'],
}

from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# removing the stopwords which are not necessary for us
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def calculate_cosine_similarity(text, keyword_list):

    #convert text and keyword list to strings
    text_str = ' '.join(text)
    keyword_str = ' '.join(keyword_list)

    #create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    #fit and transform the text and keyword list
    tfidf_matrix = vectorizer.fit_transform([text_str, keyword_str])

    #calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix)[0, 1]
    return similarity

def calculate_keyword_match(text, keywords):
    text_tokens = preprocess_text(text)
    keyword_match = {}
    for key, values in keywords.items():
        #calculate cosine similarity for each keyword list
        similarity_scores = [calculate_cosine_similarity(text_tokens, preprocess_text(keyword)) for keyword in values]

        # average similarity score for the keyword list
        avg_similarity = sum(similarity_scores) / len(similarity_scores)
        keyword_match[key] = avg_similarity

    #sort the dictionary based on average similarity score and return top 3 keys
    top_keys = sorted(keyword_match, key=keyword_match.get, reverse=True)[:3]
    return top_keys

print("Top roles that match candidate skills:", calculate_keyword_match(text, jobRoles))