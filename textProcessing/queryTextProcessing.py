from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from num2words import num2words
from nltk.stem import PorterStemmer
import string
import re

class Process:
    
    @staticmethod
    def apply_lowercase(text):
        return text.lower()

    @staticmethod
    def apply_remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def numbers_to_strings(text, max_num=1e18):
        def replace_number(match):
            num = int(match.group())
            if abs(num) >= max_num:
                return match.group()  # Return the original number if it's too large
            try:
                return num2words(num)
            except OverflowError:
                return match.group()  # Return the original number if there's an overflow error

        return re.sub(r'\d+', replace_number, text)

    @staticmethod
    def apply_remove_stop_words(text):
        stop_words = set(stopwords.words('english'))
        return ' '.join([word for word in text.split() if word not in stop_words])

    @staticmethod
    def apply_stemming(text):
        stemmer = PorterStemmer()
        return ' '.join([stemmer.stem(word) for word in text.split()])

    @staticmethod
    def apply_remove_modal_verbs(text):
        modal_verbs = [
            "can", "could", "may", "might", "shall", "should", "will", "would",
            "must", "ought", "dare", "need", "used", "is", "am", "are", "was", "were",
            "be", "being", "been","how", "have", "has", "had", "do", "does", "did",
            "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't", 
            "won't", "wouldn't", "don't", "doesn't", "didn't", "can't", "couldn't", 
            "shouldn't", "mightn't", "mustn't", "shan't", "needn't", "oughtn't", 
            "daren't", "isnot", "amnot", "arenot", "wasnot", "werenot", "havenot",
            "hasnot", "hadnot", "cannot", "couldnot", "shouldnot", "mightnot", 
            "mustnot", "shanot", "neednot", "oughtnot", "darenot",
            "isn’t", "aren’t", "wasn’t", "weren’t", "haven’t", "hasn’t", "hadn’t", 
            "won’t", "wouldn’t", "don’t", "doesn’t", "didn’t", "can’t", "couldn’t", 
            "shouldn’t", "mightn’t", "mustn’t", "shan’t", "needn’t", "oughtn’t", 
        ]
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in modal_verbs]
        return ' '.join(filtered_words)

    @staticmethod
    def process_query(text):
        lowercase_text = Process.apply_lowercase(text)
        no_punctuation_text = Process.apply_remove_punctuation(lowercase_text)
        no_stopwords_text = Process.apply_remove_stop_words(no_punctuation_text)
        numbers_to_words_text = Process.numbers_to_strings(no_stopwords_text)
        stemmed_text = Process.apply_stemming(numbers_to_words_text)
        final_text = Process.apply_remove_modal_verbs(stemmed_text) 
        return final_text