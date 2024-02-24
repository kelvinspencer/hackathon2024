import csv, os
from app.models.object_helper import ItemModel

class DBQuery():
    def __init__(self, db_type):
        self.db_type = db_type
        self.db_location = None
        self.initalize()

    def initalize(self):
        if self.db_type == "csv":
            self.db_location = "./app/data_base.csv"

    def search_for_string(self, search_string):
        entries = []
        with open(self.db_location, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if 'Macbook' is in any column of the row
                # if search_string in row:
                if any(search_string in element for element in row):
                    entries.append(row)
        return entries

    def find_by_id(self, search_id):
        with open(self.db_location, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming the id is in the first column
                if row[0] == str(search_id):
                    return row
        return None

    def create_doc(self, item):

        if os.path.exists(self.db_location):
            base_data = ItemModel.load_csv(self.db_location)
        else:
            base_data = ItemModel.initalize()
        
        base_data = base_data._append(item.__dict__, ignore_index=True)
        base_data.to_csv(self.db_location, index_label="id")
        return item