import csv, os, json
import chromadb
from app.models.object_helper import ItemModel

class DBQuery():
    def __init__(self, db_type):
        self.db_type = db_type
        self.db_location = None
        self.initalize()

    def initalize(self):
        if self.db_type == "csv":
            self.db_location = "./app/data_base.csv"
        elif self.db_type == "chromadb":
            self.client = chromadb.Client()
            self.collection = self.client.create_collection("all-documents")


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

