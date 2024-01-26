import boto3
import os
import dotenv
dotenv.load_dotenv()

class Kendra:
    client = boto3.client('kendra')
    index_id = os.getenv("KENDRA_INDEX_ID")
    
    def __init__(self):
        pass
    
    def retrieve(self, question):
        response = self.client.retrieve(
            IndexId=self.index_id,
            QueryText=question,
            PageSize=10
        )
        return response
    
    def describe(self):
        return self.client.describe_index(Id=self.index_id)