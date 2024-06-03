import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class calculate_tfidf :
 def calculate_and_save_tfidf(input_folder, output_vocab_path, output_matrix_path, vectorizer_path):
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The input folder '{input_folder}' does not exist.")

    # Get all file paths in the input folder
    file_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.txt')]

    if not file_paths:
        raise ValueError(f"No text files found in the input folder '{input_folder}'.")

    # Read the content of all files in the folder
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            documents.append(file.read())

    print(f"Read {len(documents)} documents.")

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Generate TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(documents)
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

    # Save the feature names (vocabulary) to a text file
    with open(output_vocab_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(vectorizer.get_feature_names_out()))

    # Save the TF-IDF matrix to a binary file using pickle
    with open(output_matrix_path, 'wb') as file:
        pickle.dump(tfidf_matrix, file)

    # Save the vectorizer to a binary file using pickle
    with open(vectorizer_path, 'wb') as file:
        pickle.dump(vectorizer, file)

# Example usage:
 input_folder = 'C:/Users/bachar hatem/Desktop/5th/IR/webis-touche2020/separated_documents'
 output_vocab_path = 'C:/Users/bachar hatem/Desktop/5th/IR/webis-touche2020/tfidf_vocabulary.txt'
 output_matrix_path = 'C:/Users/bachar hatem/Desktop/5th/IR/webis-touche2020/tfidf_matrix.pkl'
 vectorizer_path = 'C:/Users/bachar hatem/Desktop/5th/IR/webis-touche2020/tfidf_vectorizer.pkl'

# Function execution
 calculate_and_save_tfidf(input_folder, output_vocab_path, output_matrix_path, vectorizer_path)