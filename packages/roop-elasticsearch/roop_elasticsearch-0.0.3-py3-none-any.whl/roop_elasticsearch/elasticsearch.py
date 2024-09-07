import json
import os

from elasticsearch import Elasticsearch

resultCache = None

class OpenSearch:
    def __init__(self):
        self.user, self.pwd = os.environ['ES_USER'], os.environ['ES_PWD']
        self.es_connection = None

    def __enter__(self):
        print("Creating Opensearch connection via user %s" %self.user)
        self.es_connection = Elasticsearch(
            host=os.environ['ES_HOST'],
            http_auth=(
                self.user,
                self.pwd
            ),
            port=int(os.environ['ES_PORT']),
            use_ssl=True,
            verify_certs=False
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.es_connection.transport.close()

    def get_doc(self, index_name, document_id):
        try:
            response = self.es_connection.get(index=index_name, id=document_id)
            if not response:
                return None
            return response['_source']
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")

    def add_doc(self, index_name, document_id, document_data):
        try:
            self.es_connection.index(
                index=index_name, 
                id=document_id, 
                body=json.dumps(document_data, default=str),
                refresh=True
                )
        except Exception as e:
            print(f"Error indexing document: {str(e)}")

    def update_doc(self, index_name, document_id, document_data):
        try:
            _body = {
                'doc': document_data
            }
            self.es_connection.update(
                index=index_name, 
                id=document_id, 
                body=_body,
                refresh=True
                )
        except Exception as e:
            print(f"Error updating document: {str(e)}")

    def delete_doc(self, index_name, document_id):
        try:
            self.es_connection.delete(index=index_name, id=document_id)
        except Exception as e:
            print(f"Error deleting document: {str(e)}")

    def get_doc_by_query(self, index_name, query):
        try:
            response = self.es_connection.search(body=query, index=index_name)
            if len(response["hits"]["hits"]) == 0:
                return None, None
            return response["hits"]["hits"][0]['_source'], response["hits"]["hits"][0]['_id']
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")
            raise e
        
    def get_docs_by_query(self, index_name, query):
        try:
            response = self.es_connection.search(body=query, index=index_name)
            return response["hits"]["hits"]
        except Exception as e:
            print(f"Error retrieving document: {str(e)}")
        
    def update_docs_by_query(self, index_name, query):
        try:
            self.es_connection.update_by_query(index=index_name, body=query, refresh=True)
        except Exception as e:
            print(f"Error indexing document: {str(e)}")


