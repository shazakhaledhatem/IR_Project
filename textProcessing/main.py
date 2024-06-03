from flask import Flask, request, render_template, jsonify
import pandas as pd
from queryTextProcessing import Process

app = Flask(__name__)  

dataset1 = pd.read_csv('C:/Users/DELL/Desktop/ir_progect_new/merged_ranked_results.csv')
dataset2 = pd.read_csv('C:/Users/DELL/Desktop/ir_progect_new/merged_ranked_results_1.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    print("Request received:", request)
    if request.method == 'POST':
        query = request.form.get('query')
        dataset_choice = request.form.get('dataset')
        if query and dataset_choice:
            query_new = Process.process_query(query)
            print("Processed Query:", query_new)
            results = search_csv(dataset1 if dataset_choice == 'First Data Set(antique/train)' else dataset2, query_new)
            print("Results to return:", {'query': query_new, 'results': results})
            return jsonify({'query': query_new, 'results': results})
        else:
            return jsonify({'message': 'Missing query or dataset choice.'}), 400
    
    query = request.args.get('query')
    dataset_choice = request.args.get('dataset')
    if query and dataset_choice:
        query_new = Process.process_query(query)
        results = search_csv(dataset1 if dataset_choice == 'First Data Set(antique/train)' else dataset2, query_new)
        print("Results to return:", {'query': query_new, 'results': results})
        return jsonify({'query': query_new, 'results': results})
    else:
        return jsonify({'message': 'Please provide query and dataset parameters.'}), 400

def search_csv(dataset, query):
    try:
        if 'query' in dataset.columns:
            filtered_dataset = dataset[dataset['query'].str.contains(query, case=False, regex=False)]
            results_list = filtered_dataset.to_dict(orient='records')
            return results_list
        else:
            print("Query column not found in dataset.")
            return []
    except Exception as e:
        print("Error processing dataset:", str(e))
        return []

if __name__ == '__main__':
    app.run(host='192.168.14.9', port=5000, debug=True)