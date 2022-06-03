import numpy as np
import pandas as pd
import re
import nltk
import sklearn
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

from docx import Document
from PyPDF2 import PdfFileReader, PdfFileWriter
import docx2txt
import pickle
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
dep = {"Data science": 6,"HR": 12,"Advocate": 0,"Arts": 1,"Web designing": 24,"Mechanical Engineer": 16,"Sales": 22,"Health and fitness": 14,"Civil Engineer": 5,"Java Developer": 15,"Business Analyst": 4,"SAP Developer": 21,"Automation Testing": 2,"Electrical Engineering": 11,"Operations Manager": 18,"Python Developer": 20,
       "DevOps Engineer": 8,"Network Security Engineer": 17,"PMO": 19,"Database": 7,"Hadoop": 13,"ETL Developer": 10,"DotNet Developer": 9,"Blockchain": 3,"Testing": 23}
SKILLS_DB = []
ch = ['c', 'c++', 'java', '.NET c#', 'python', 'ruby', 'php', 'html', 'css', 'javascript', 'node js', 'react js','django', 'flask', 'apache','hadoop', 'big data', 'data science', 'numpy', 'pandas', 'machine learning', 'deep learning', 'statistics', 'nlp',
      'natural language processing''open cv', 'compter vision', 'devops', 'aws', 'azure', 'microsoft azure', 'google cloud', 'rest api', 'graphql','react', 'react native','sql', 'postgresql', 'git', 'redis', 'jira', 'selenium', 'jquery', 'bootstrap', 'mongodb']
for i in ch:
    SKILLS_DB.append(i.lower())


def get_predictions(complete_text):
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer()
    model = pickle.load(open('model.pkl', 'rb'))
    tf = pickle.load(open('count.pkl', 'rb'))
    lemma = WordNetLemmatizer()
    p = []
    review = re.sub('http\S+\s*', ' ', complete_text)  # remove URLs
    review = re.sub('RT|cc', ' ', review)  # remove RT and cc
    review = re.sub('#\S+', '', review)  # remove hashtags
    review = re.sub('@\S+', '  ', review)  # remove mentions
    review = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', review)  # remove punctuations
    review = re.sub(r'[^\x00-\x7f]', r' ', review)
    review = re.sub('\s+', ' ', review)  # remove extra whitespace
    review = review.lower()
    review = review.split()
    review = [lemma.lemmatize(word) for word in review if not word in stopwords.words("english")]
    review = ' '.join(review)
    p.append(review)
    l = tf.transform(p).toarray()
    sol = model.predict(l)
    for i, j in dep.items():
        if j == sol:
            l = i
    number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', complete_text)
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", complete_text)
    years = re.findall(r"(\d+(?:\.\d+)?).?\s?year.?", complete_text)

    ## Extract name
    nlp = spacy.load('en_core_web_sm')

    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)
    nlp_text = nlp(complete_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        name = span.text

    input_text = complete_text.lower()
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)

    return l , number , emails , years , name , found_skills


