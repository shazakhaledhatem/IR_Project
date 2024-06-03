
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from num2words import num2words
from nltk.stem import PorterStemmer
import string
import csv
import re



class Process:
#lowerCase
 def apply_lowercase(input_file, output_file):
    def to_lowercase(text):
        return text.lower()

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            doc_id, text = row
            cleaned_text = to_lowercase(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Lowercase conversion completed and saved to {output_file}")

# Example usage``
 apply_lowercase('webis_touche2020_docs.tsv', 'webis_touche2020_docs_lowercase.tsv')


#panctuation
 def apply_remove_punctuation(input_file, output_file):
    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', string.punctuation))

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            doc_id, text = row
            cleaned_text = remove_punctuation(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Punctuation removal completed and saved to {output_file}")

# Example usage
 apply_remove_punctuation('webis_touche2020_docs_lowercase.tsv', 'webis_touche2020_docs_no_punct.tsv')


#convert numbers
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

def apply_numbers_to_strings(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            doc_id, text = row
            cleaned_text = numbers_to_strings(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Number to string conversion completed and saved to {output_file}")

# Example usage
    apply_numbers_to_strings('webis_touche2020_docs_no_punct.tsv', 'webis_touche2020_docs_numbers.tsv')


#stop words
def apply_remove_stop_words(input_file, output_file):
    def remove_stop_words(text):
        stop_words = set(stopwords.words('english'))
        return ' '.join([word for word in text.split() if word not in stop_words])
    
    # Increase the CSV field size limit to a large value
    csv.field_size_limit(10**9)
    
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            doc_id, text = row
            cleaned_text = remove_stop_words(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Stop words removal completed and saved to {output_file}")


# Example usage
    apply_remove_stop_words('webis_touche2020_docs_numbers.tsv', 'webis_touche2020_docs_no_stopwords.tsv')


#stemming
def apply_stemming(input_file, output_file):
    def stemming(text):
        stemmer = PorterStemmer()
        return ' '.join([stemmer.stem(word) for word in text.split()])

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            doc_id, text = row
            cleaned_text = stemming(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Stemming completed and saved to {output_file}")

# Example usage
    apply_stemming('webis_touche2020_docs_no_stopwords.tsv', 'webis_touche2020_docs_stemmed.tsv')

#remove more stop
def apply_remove_modal_verbs(input_file, output_file):
    modal_verbs = [
    "can", "could", "may", "might", "shall", "should", "will", "would",
    "must", "ought", "dare", "need", "used", "is", "am", "are", "was", "were",
    "be", "being", "been", "have", "has", "had", "do", "does", "did",
    "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't", 
    "won't", "wouldn't", "don't", "doesn't", "didn't", "can't", "couldn't", 
    "shouldn't", "mightn't", "mustn't", "shan't", "needn't", "oughtn't", 
    "daren't", "isnot", "amnot", "arenot", "wasnot", "werenot", "havenot",
    "hasnot", "hadnot", "cannot", "couldnot", "shouldnot", "mightnot", 
    "mustnot", "shanot", "neednot", "oughtnot", "darenot"
         "isn’t", "aren’t", "wasn’t", "weren’t", "haven’t", "hasn’t", "hadn’t", 
    "won’t", "wouldn’t", "don’t", "doesn’t", "didn’t", "can’t", "couldn’t", 
    "shouldn’t", "mightn’t", "mustn’t", "shan’t", "needn’t", "oughtn’t", 
        
]
    def remove_modal_verbs(text, modals=modal_verbs):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in modals]
        return ' '.join(filtered_words)
    
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        # Read and write the header
        header = next(reader)
        writer.writerow(header)
        
        # Process each document
        for row in reader:
            doc_id, text = row
            cleaned_text = remove_modal_verbs(text)
            writer.writerow([doc_id, cleaned_text])
            
    print(f"Modal verbs removal completed and saved to {output_file}")

# Example usage
apply_remove_modal_verbs('webis_touche2020_docs_stemmed.tsv', 'webis_touche2020_docs_no_modals.tsv')
