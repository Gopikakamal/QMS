from dal.mongo_data_adapter.mongo_dal import DBAdapter


class FiaStatusModel:

    def insert_fia_status(self, data):
        return DBAdapter("QMS").insert("fia", data)

    def get_one_fia_status(self, query):
        return DBAdapter("QMS").get_one("fia", query_param=query)

    def get_all_fia_status(self, query, projection):
        return DBAdapter("QMS").get_all_doc(
            collection_name="fia",
            query=query,
            projection=projection,
            page=1,
            limit=10
        )
        # print("Response from DAL:", response)
        # return response

    def update_fia_status(self, query, update_data):
        return DBAdapter("QMS").update("fia", update_data, query)
