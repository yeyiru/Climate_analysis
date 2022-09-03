import glob
import yaml
import text2vec

from tqdm import tqdm
from utils.utils import cal_sim, get_keywords
from utils.plot import plot_radar
from utils.file_process import pdf2txt, read_paper, \
                                read_stopwords, save_csv

def run(hyp, sim, stopwords, file_path):
    sentence, err = read_paper(file_path)
    if not err:
        keywords = get_keywords(sentence, stopwords)
        scoress = cal_sim(hyp, sim, keywords)
        print('Begin save to IMG & CSV')
        # plot_heatmap(hyp, keywords, scoress, file_path)
        plot_radar(hyp, keywords, scoress, file_path)
        save_csv(hyp, keywords, scoress, file_path)
    return 

if __name__ == '__main__':
    f = open('./hyp/hyp.yaml', 'r', encoding='utf-8').read()
    hyp = yaml.safe_load(f)
    paper_dir = './data'
    stopwords = read_stopwords()
    sim = text2vec.Similarity()
    print('Begin PDF to TXT!')
    for pdf in tqdm(glob.glob(r'./data/*/*.pdf')):
        # pdf_dir = f'./data/1{i}'
        # for pdf in tqdm(os.listdir(pdf_dir)):
        pdf2txt(pdf)
    
    for file_path in glob.glob(rf'./data/*/*.txt'):
        file_name = file_path.split('\\')[-1].replace('.txt', '')
        print('Begin to calculate ' + file_name)
        run(hyp, sim, stopwords, file_path)