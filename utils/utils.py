import requests

import numpy as np

from tqdm import tqdm
from opencc import OpenCC
from collections import Counter

def label_s2t(keywords, areas):
    cc = OpenCC('s2t')
    for i in range(len(keywords)):
        keywords[i, 0] = cc.convert(keywords[i, 0])
    for i in range(len(areas)):
        areas[i] = cc.convert(areas[i])
    return keywords, areas

def get_keywords(sentence, stopwords):
    tags = cutword(sentence)
    cc = OpenCC('t2s')
    keywords = []
    cnt = 0
    for word, fre in Counter(tags).most_common(len(Counter(tags))):
        if cnt < 20:
            word = cc.convert(word)
            if word not in stopwords:
                keywords.append([word, fre])
                cnt += 1
            else:
                continue
        else:
            break
    keywords = np.array(keywords)
    return keywords

def cutword(sentence):
    tags = requests.post("https://textseg.sgis.tw/", {"query":sentence, "mode": 2})
    tags = tags.text.replace('\n', '').replace('\t', '').replace('\r', '')
    tags = tags.replace('{', '').replace('}', '').replace('[', '').replace(']', '')
    tags = tags.replace('"', '').replace(' ', '')
    tags = tags.split(',')[1:]
    return tags

def _sim(keywords, sim, area, scoress):
    scores = []
    for keyword in tqdm(keywords[:, 0]):
        scores.append(sim.get_score(area, keyword))
    scoress[area] = scores
    return scoress

def cal_sim(hyp, sim, keywords):
    scoress_dict = {}
    for area in hyp['areas']:
       scoress_dict = _sim(keywords, sim, area, scoress_dict)

    scoress = []
    for area in hyp['areas']:
        scoress.append(scoress_dict[area])
    scoress = np.array(scoress)
    return scoress

# def _sim_dpp(keywords, area, scoress):
#     scores = []
#     for keyword in keywords[:, 0]:
#         sim = text2vec.Similarity()
#         scores.append(sim.get_score(area, keyword))
#     scoress[area] = scores
#     return 

# def cal_sim_dpp(hyp, keywords):
    
#     manager = Manager()
#     scoress_dict = manager.dict()
#     pool = Pool(processes = hyp['num_work'])

#     pbar = tqdm(total=len(hyp['areas']))
#     pbar.set_description('Calculating..')
#     update = lambda *args: pbar.update()
    
#     for area in hyp['areas']:
#          pool.apply_async(_sim_dpp, (keywords, area, scoress_dict), callback=update)
#     pool.close()
#     pool.join()

#     scoress = []
#     for area in hyp['areas']:
#         scoress.append(scoress_dict[area])
#     return scoress