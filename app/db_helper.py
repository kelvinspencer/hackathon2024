import csv, os, json
import re
import chromadb
from app.models.object_helper import ItemModel
import vertexai
import os
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

def get_unique_hashes(dict_list):
    unique_hashes = set()
    for item in dict_list:
        unique_hashes.add(item['hash'])
    
    unique_dicts = []
    for hash in unique_hashes:
        for item in dict_list:
            if item['hash'] == hash:
                unique_dicts.append(item)
                break
    return unique_dicts

class DBQuery():
    def __init__(self, db_type):
        self.db_type = db_type
        self.db_location = None
        self.initalize()

    def initalize(self):
        if self.db_type == "csv":
            self.db_location = "./app/data_base.csv"
        elif self.db_type == "chromadb":
            self.client = chromadb.PersistentClient(path='./chromadb')


    def search_for_string(self, search_string):
        entries = []
        if self.db_type == "csv":
            with open(self.db_location, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if any(search_string in element for element in row):
                        entries.append(row)
        elif self.db_type == "chromadb":
            entries = self.collection.query(
                query_texts=[search_string],
                n_results=10,
                # where={"metadata_field": "is_equal_to_this"}, # optional filter
                where_document={"$contains":search_string}  # optional filter
            )

        return entries

    def find_by_id(self, search_id):
        with open(self.db_location, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(search_id):
                    return row
        return None

    def create_doc(self, item):
        if self.db_type == "csv":
            if os.path.exists(self.db_location):
                base_data = ItemModel.load_csv(self.db_location)
            else:
                base_data = ItemModel.initalize()
            
            base_data = base_data._append(item.__dict__, ignore_index=True)
            base_data.to_csv(self.db_location, index_label="id")

        elif self.db_type == "chromadb":
            metadatas=[]
            for x in item.metadatas:
                metatag = json.loads(x)
                metadatas.append(metatag)
    
            self.collection.add(
                documents=item.documents, 
                metadatas=metadatas,
                ids=item.ids, 
            )
        
        return item
    
    def delete_all_docs(self):
        self.client.delete_collection(name="all-documents")
        self.initalize()
    
    def get_tags(self):
        collection = self.client.get_collection("all-documents")
        tag_strings = [item.get('tags') for item in collection.get().get("metadatas") if item]
        tags_full= []
        for tag_string in tag_strings:
            if tag_string:
                tags_full.extend(tag_string.lower().split('|'))
        return list(set(tags_full))
    
    def get_docs_by_tags(self, tags):
        tag_compare = '|'.join(tags)
        collection = self.client.get_collection("all-documents")
        documents = collection.get().get("documents")
        metadatas = collection.get().get("metadatas")
        tag_strings = [(i, item.get('tags')) for i, item in enumerate(metadatas) if item]
        docs = []
        for idx,tag_string in tag_strings:
            if tag_string:
                match = re.search(tag_compare, tag_string.lower())
                if match:
                    metadata = metadatas[idx]
                    header = metadata.pop('header')
                    hash = metadata.pop('hash')
                    source_url = metadata.pop('source_url')
                    original_content = metadata.pop('original_content')
                    docs.append({"document":documents[idx],
                                 "original_content": original_content,
                                 "metadata": metadata,
                                 "header": header,
                                 "source_url": source_url,
                                 "hash": hash})
        return get_unique_hashes(docs)

