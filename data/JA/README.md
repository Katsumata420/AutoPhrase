**stopwords.txt**

The list of stopwords is created from spacy (3.1.2), ginza (5.0.1), and ja-ginza (5.0.0) as follows:

```python
import spacy
nlp = spacy.load("ja_ginza")
stopwords = nlp.Defaults.stop_words # list of stopwords
```

**wiki_quality.txt, wiki_all.txt**

The list of entity names are extracted from titles of Japanese Wikipedia. Quality phrases are defined as those titles with longer text contents (longer than 100 characters) without any stopword or separator.

```
python -m wikiextractor.WikiExtractor jawiki-20210520-pages-articles-multistream.xml.bz2
python extract_phrases.py
```