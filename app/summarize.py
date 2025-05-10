
import nltk
import os

# Ensure punkt tokenizer is downloaded properly
NLTK_DATA_DIR = "/tmp/nltk_data"
nltk.data.path.append(NLTK_DATA_DIR)

def ensure_punkt():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", download_dir=NLTK_DATA_DIR)

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def generate_exec_summary(text, sentence_count=3):
    ensure_punkt()

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return "\n".join(str(sentence) for sentence in summary)
