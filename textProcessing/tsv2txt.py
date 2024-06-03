import logging
import os
import re


class tsv2txt :
 def separate_combined_text_file(input_file, output_dir, log_file='processing.log'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up logging to file
    logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s: %(message)s')
    
    logging.info(f"Starting to process the file: {input_file}")
    
    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            content = infile.read()
        
        # Split the content into individual documents using the separator
        documents = re.split(r'\n-{50}\n', content)
        
        for document in documents:
            lines = document.strip().split('\n')
            if len(lines) < 2:
                logging.warning(f"Skipping incomplete document: {document[:50]}...")
                continue
            
            doc_id_line = lines[0]
            title_line = lines[1]
            
            # Extract the document ID and title
            doc_id_match = re.match(r'Document ID: (.+)', doc_id_line)
            title_match = re.match(r'Title: (.+)', title_line)
            
            if not doc_id_match or not title_match:
                logging.warning(f"Skipping malformed document: {document[:50]}...")
                continue
            
            doc_id = doc_id_match.group(1)
            title = title_match.group(1)
            
            # Create the file name and path
            file_name = f"{doc_id}.txt"
            file_path = os.path.join(output_dir, file_name)
            
            # Write the title to the individual text file
            try:
                with open(file_path, mode='w', encoding='utf-8') as outfile:
                    outfile.write(title)
                logging.info(f"Written document {doc_id} to {file_path}")
            except Exception as e:
                logging.error(f"Failed to write document {doc_id} to {file_path}: {e}")
                
        logging.info(f"Documents separated and saved to directory: {output_dir}")
    
    except Exception as e:
        logging.error(f"Failed to process the file: {e}")

# Example usage
 input_file = 'combined_documents.txt'
 output_dir = 'separated_documents'
 separate_combined_text_file(input_file, output_dir)