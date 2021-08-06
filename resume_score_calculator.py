import pyresparser
from pyresparser import ResumeParser
import nltk
from google_drive_downloader import GoogleDriveDownloader as gdd
nltk.download('stopwords')
import sys
import en_core_web_sm
import spacy
nlp = spacy.load('en_core_web_sm')# Load English tokenizer, tagger, parser, NER and word vectors


def calculate_score(link, user_name, skills, cgpa):
    link  = link[32:]
    link = link.split('/')
    file_loc = 'resume/' + user_name +'.pdf'
    gdd.download_file_from_google_drive(file_id=link[0],dest_path=file_loc)
    data = ResumeParser(file_loc).get_extracted_data()
    score = 0
    match = 0
    for i in skills:
        if i in data['skills']:
            match = match +1
    if match > 4:
        match =4
    score += match
    left = len(data['skills']) - match
    if left > 0:
        if left > 10:
            score +=1
        else:
            score += left*0.1
    if data['experience']:
        if len(data['experience']) > 20:
            score +=2
        else:
            score += len(data['experience'])*0.2
    cgpa_score = score
    score += float(cgpa)*0.3
    ls = []
    ls.append(cgpa_score)
    ls.append(score)
    return ls
