# third party
import re
from datetime import datetime, timezone

# project package
import util.common_library as common_lib
from app import db_connection


class DBAdapter:

    def __init__(self, db_name='hmi'):
        self.db_name = db_connection.get_database(db_name)

    def insert(self, collection_name, payload):
        """
        MongoDB insert method
        call method ex: obj.insert(collection_name, payload)
        Args:
            payload (dict): {"order_id": "", "order_name": ""}

        Returns:
            dict: {"status": True/False, "data": {}}
        """
        try:
            current_datetime = datetime.now(timezone.utc)
            payload['created_by'] = ''
            payload['created_at'] = int(current_datetime.timestamp())
            payload['updated_by'] = ''
            payload['updated_at'] = int(current_datetime.timestamp())
            payload['is_active'] = False

            result = self.db_name[collection_name].insert_one(payload)
            if result.acknowledged:
                return common_lib.response_json(True)
            else:
                return common_lib.response_json(False)
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def search(
        self,
        collection_name,
        page,
        limit,
        query_param,
        projection={"_id": 0},
        sort_by=[("created_at", -1)]
    ):
        """
        MongoDB get_all method to get based on Pagination
        call method ex: obj.get_one(table_name, page, limit, query)
        Args:
            page : 1
            limit : 10
            query (dict): {"column_name": "", "search_term": ""} ->
                Need to pass column name If search term is there
        Returns:
            dict: {"status": True/False, "data": {}}
        """
        try:
            documents_to_skip = (page-1) * limit
            query_param["is_active"] = False

            if 'search_term' in query_param and query_param['search_term']:
                pipeline = self.create_pipeline_for_search(
                    query_param, documents_to_skip, projection, sort_by)
                documents = self.db_name[collection_name].aggregate(pipeline)
            else:
                documents = self.db_name[collection_name].find(
                    query_param, projection).sort(sort_by).skip(
                        documents_to_skip).limit(limit)

            return self.extract_result(list(documents))
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def create_pipeline_for_search(
        self,
        query_param,
        documents_to_skip,
        projection,
        sort_criteria=[("created_at", -1)]
    ):
        search_term = query_param['search_term']
        column_name = query_param['column_name']
        search_pattern = re.compile(search_term, re.IGNORECASE)

        return [
            {
                '$match': {
                    'is_active': False,
                    column_name: {'$regex': search_pattern},
                }
            },
            {
                '$sort': {
                    sort_criteria[0][0]: sort_criteria[0][1]
                    # 1 for asc and -1 for desc
                }
            },
            {
                '$skip': documents_to_skip  # Number of documents to skip
            },
            {
                '$project': projection
            }
            # Add more conditions if needed
        ]

    def get_one(
        self,
        collection_name,
        projection=None,
        query_param=None,
        sort_by=[("created_at", -1)]
    ):
        """
        MongoDB get_one method to get Single record based on given condition
        call method ex: obj.get_one(table_name, query)
        Args:
            query (dict): {"column_name": "", "search_term": ""} ->
            Need to pass column name If search term is there
        Returns:
            dict: {"status": True/False, "data": {}}
        """
        try:
            if not query_param:
                query_param = {}
            if not projection:
                projection = {"_id": 0}
            else:
                default_projection = {"_id": 0}
                projection |= default_projection
            documents = self.db_name[collection_name].find(
                query_param, projection).sort(sort_by)
            return self.extract_result(list(documents))
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def extract_result(self, documents):
        return common_lib.response_json(True, {"records": documents})

    def get_count(self, collection_name, query_param):
        """
        MongoDB get count method
        call method ex: obj.get_count(table_name, query)
        Args:
            query (dict): {"column_name": "", "search_term": ""} ->
            Need to pass column name If search term is there
        Returns:
            dict: {"status": True/False, "data": {"count":{}}}
        """
        try:
            query_param["is_active"] = False

            if 'search_term' in query_param and query_param['search_term']:
                projection = {"_id": 0}
                pipeline = self.create_pipeline_for_search(
                    query_param, 0, projection)
                aggregate_result = self.db_name[collection_name].\
                    aggregate(pipeline)
                documents = len(list(aggregate_result))
            else:
                documents = self.db_name[collection_name].\
                    count_documents(query_param)
            return common_lib.response_json(True, {"count": documents})
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def update(self, collection_name, fields_to_update, query_param=None):
        """
        MongoDB update method
        call method ex: obj.update(table_name, fields_to_update, query)
        Args:
            fields_to_update (dict): {"order_value": ""}
            query (dict): {"order_id": ""}

        Returns:
            dict: {"status": True/False, "data": {}}
        """
        try:
            current_datetime = datetime.now(timezone.utc)
            fields_to_update['updated_at'] = int(current_datetime.timestamp())
            fields_to_update["updated_by"] = ''
            query_param["is_active"] = False

            documents = self.db_name[collection_name].\
                update_one(query_param, {"$set": fields_to_update})
            if documents.acknowledged:
                return common_lib.response_json(True)
            else:
                return common_lib.response_json(False)
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def delete_item(self, collection_name, query_param, soft_delete=True):
        """
        MongoDB delete method
        call method ex: obj.delete_item(table_name, query, soft_delete)
        Args:
            query (dict): {"order_id": ""}

        Returns:
            dict: {"status": True/False, "data": {}}
        """
        try:
            if soft_delete:
                fields_to_update = {
                    "is_active": True,
                    "updated_at": datetime.now(timezone.utc),
                    "updated_by": ""}
                documents = self.db_name[collection_name].\
                    update_one(query_param, {"$set": fields_to_update})
            else:
                documents = self.db_name[collection_name].\
                    delete_one(query_param)

            if documents.acknowledged:
                return common_lib.response_json(True)
            else:
                return common_lib.response_json(False)
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def get_all_doc(
        self,
        collection_name,
        query,
        sort_by=[("created_at", -1)],
        projection={"_id": 0},
        page=1,
        limit=0
    ):
        try:
            query["is_active"] = False
            if not projection:
                projection = {"_id": 0}
            if limit > 0:
                documents_to_skip = (page-1) * limit
                result = self.db_name[collection_name].\
                    find(query, projection).sort(sort_by).skip(
                        documents_to_skip).limit(limit)
            else:
                result = self.db_name[collection_name].\
                    find(query, projection).sort(sort_by)
            return common_lib.response_json(True, {"records": list(result)})
        except Exception as e:
            return common_lib.response_json(False, str(e))

    def aggregate(self, collection_name, pipeline):
        """
        This will handle direct raw aggregate query
        Args:
            collection_name (str): colletion/table name from db
            pipeline (list): aggr query from actual method

        Returns:
            dict: result/error from mongoDB
        """
        try:
            result = self.db_name[collection_name].aggregate(pipeline)
            return common_lib.response_json(True, {"records": list(result)})
        except Exception as e:
            return common_lib.response_json(False, str(e))
