import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle

class MatchingAndRanking:
    def init(self, document_folder, query_file, output_folder, vectorizer_pkl_path, tfidf_matrix_pkl_path):
        self.document_folder = document_folder
        self.query_file = query_file
        self.output_folder = output_folder
        self.vectorizer_pkl_path = vectorizer_pkl_path
        self.tfidf_matrix_pkl_path = tfidf_matrix_pkl_path
        
        self.documents, self.file_paths, self.document_ids = self.load_documents_from_files()
        self.tfidf_matrix, self.vectorizer = self.load_vectorizer_and_tfidf_matrix()
        
        self.validate_data()
    
    def load_documents_from_files(self):
        documents = []
        file_paths = []
        document_ids = []
        for filename in os.listdir(self.document_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.document_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append(content)
                    file_paths.append(file_path)
                    document_ids.append(filename)  # Use the filename as document ID
        return documents, file_paths, document_ids

    def load_vectorizer_and_tfidf_matrix(self):
        with open(self.vectorizer_pkl_path, 'rb') as file:
            vectorizer = pickle.load(file)
        
        with open(self.tfidf_matrix_pkl_path, 'rb') as file:
            tfidf_matrix = pickle.load(file)
        
        return tfidf_matrix, vectorizer

    def validate_data(self):
        if len(self.documents) != self.tfidf_matrix.shape[0] or len(self.documents) != len(self.file_paths) or len(self.documents) != len(self.document_ids):
            raise ValueError("Mismatch between the number of documents and the TF-IDF matrix, file_paths, or document_ids.")
        print(f"Loaded {len(self.documents)} documents.")
        print("Validation passed. Number of documents matches TF-IDF matrix and file paths.")
    
    def search_documents(self, query):
        query_vector = self.vectorizer.transform([query])
        cosine_scores = cosine_similarity(query_vector, self.tfidf_matrix)

        results = []
        for i, score in enumerate(cosine_scores.flatten()):
            if score > 0:  # Skip results with zero cosine similarity
                results.append({
                    'document_id': self.document_ids[i],
                    'file_path': self.file_paths[i],
                    'cosine_similarity': score,
                    'document': self.documents[i]
                })

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by='cosine_similarity', ascending=False).head(10)  # Get top 10 results
        return results_df

    def process_queries_and_store_results(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        with open(self.query_file, 'r', encoding='utf-8') as file:
            queries = file.readlines()

        all_results = []

        for query_id, query in enumerate(queries):
            query = query.strip()  # Remove leading/trailing whitespace
            results_df = self.search_documents(query)

            results_df['query_id'] = query_id
            results_df['query'] = query
            
            results_df = results_df[['query_id', 'query', 'document_id', 'file_path', 'cosine_similarity', 'document']]
            
            all_results.append(results_df)

        all_results_df = pd.concat(all_results, ignore_index=True)
        output_file_path = os.path.join(self.output_folder, "ranked_results.csv")
        all_results_df.to_csv(output_file_path, index=False)
        print(f"Results for all queries saved to {output_file_path}")


