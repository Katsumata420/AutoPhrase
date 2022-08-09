from glob import glob
import multiprocessing as mp
import xml.etree.ElementTree as ET

def check_stopwords(title, stopwords):
    for stop in stopwords:
        if stop in title:
            return True
    return False

def check_separator(title):
    for ch in ",;:() ":
        if ch in title:
            return True
    return False

def init_fn():
    global stopwords
    with open("stopwords.txt") as h:
        stopwords = [line for line in h.read().split("\n") if len(line) > 0]

def process_fn(fn):
    global stopwords

    with open(fn) as h:
        text = h.read()
    text = f"<root>{text}</root>"

    root = ET.fromstring(text)
    all_titles = []
    quality_titles = []
    for child in root:
        doc_text = child.text
        title = doc_text.split("\n")[1]
        all_titles.append(title)

        if len(doc_text) < 100:
            continue
        if check_stopwords(title, stopwords):
            continue
        if check_separator(title):
            continue

        quality_titles.append(title)

    return all_titles, quality_titles    

if __name__=="__main__":
    TARGET_DIRECTORY = "text"

    # Extract all titles.
    fns = glob(f"{TARGET_DIRECTORY}/*/wiki_*")

    titles = []
    quality_titles = []
    with mp.Pool(mp.cpu_count(), initializer=init_fn) as pool:
        for _titles, _quality_titles in pool.imap_unordered(process_fn, fns, chunksize=5):
            titles += _titles
            quality_titles += _quality_titles

    with open("wiki_all.txt", "w") as h:
        for title in titles:
            h.write(f"{title}\n")
    
    with open("wiki_quality.txt", "w") as h:
        for title in quality_titles:
            h.write(f"{title}\n")