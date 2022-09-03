import os
import glob
import pdfplumber
import pandas as pd

from utils.utils import label_s2t

def pdf2txt(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        title = pdf_path.split('/')[-1].replace('.pdf', '') + '\n'
        contents = f'Title: {title}'
        for i in range(1, len(pdf.pages)):
            page = pdf.pages[i]
            page_content = ''

            if '目錄\n' in page.extract_text():
                continue
            for line in page.extract_text().split('\n')[:-1]:
                line = line.replace(' ', '')
                if line == '':
                    continue
                page_content += line
            contents += page_content
    txt = open(pdf_path.replace('.pdf', '.txt'), 'w', encoding='utf-8')
    txt.write(contents)
    txt.close()
    return

def read_stopwords():
    stopwordss = []
    for stop_path in glob.glob(r'./stop_word/*.txt'):
        with open(stop_path, 'r', encoding='utf-8') as f:
            stopwords = f.readlines()
        for i in range(len(stopwords)): 
            stopwords[i] = stopwords[i].replace('\n', '')
        stopwordss += stopwords
    stopwordss = set(stopwordss + ['Fig', 'fig', 'Fig.', '图', '气候变迁', '中', '会'])
    return stopwordss

def read_paper(file_path):
    file_name = file_path.split('\\')[-1].replace('.txt', '')
    err = False
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
        if len(sentences) > 1:
            sentence = sentences[1]
        else:
            sentence = []
            err = True
        f.close()

    return sentence, err

def save_csv(hyp, keywords, scoress, file_path):
    file_name = file_path.split('\\')[-1].replace('.txt', '')
    save_dir = file_path.replace('data', 'output\\csv').replace(file_path.split('\\')[-1], '')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    
    areas = hyp['areas']
    keywords, areas = label_s2t(keywords, areas)
    df = pd.DataFrame(scoress)
    df.columns = keywords[:, 0]
    df.insert(0, 'AREA', areas)
    df.to_csv(f'{save_dir}/{file_name}.csv', index=False, encoding='utf-8-sig')
    