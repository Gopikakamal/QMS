from proto.test_pb2 import FIAResponse
from proto.test_pb2_grpc import FiaStatusServiceServicer
import json
from app.models.fia_status_model import FiaStatusModel


class FiaStatus(FiaStatusServiceServicer):
    def __init__(self):
        self.model = FiaStatusModel()

    def GetFiaStatus(self, request, context):
        try:
            query = json.loads(request.json)
            print(query)
            required_params = ["is_fpi"]
            missing_params = [param for param in required_params
                              if param not in query]
            if missing_params:
                missing_params_str = ", ".join(missing_params)
                return FIAResponse(json=json.dumps({"status": False,
                                                    "message": f"Missing \
                                required parameters: {missing_params_str}"}))

            query_params = {"qa_status": {"$exists": False}}
            if query.get("is_fpi"):
                query_params["is_fpi"] = True

            projection_fields = {
                "_id": 0, "tenant_id": 1, "sub_tenant_id": 1, "unit_id": 1,
                "dept_id": 1, "machine_num": 1, "MTS_num": 1,
                "workorder_id": 1, "opn_num": 1, "part_num": 1,
                "part_serial_num": 1, "instage_inspection_status": 1,
                "is_fpi": 1
            }
            response = self.model.get_all_fia_status(query_params,
                                                     projection_fields)
            # print(">>>>>>>>>>>:", response)
            if not response["status"]:
                return FIAResponse(json=json.dumps({"status": False, "message\
                    ": "Failed to get FIA status"}))
            records = response["data"]["records"]
            if not records:
                return FIAResponse(json=json.dumps({"status": True,
                                                    "message": "No FIA status \
                                                    records found"}))
            # print(response, ">>>>>>>>>>>>>>>>.")
            return FIAResponse(json=json.dumps(response))
            # return FIAResponse("response")
        except Exception as e:
            return FIAResponse(json=json.dumps({"status": False,
                                                "message": str(e)}))

    def PostFiaStatus(self, request, context):
        try:
            data = json.loads(request.json)
            print("Data Received for Posting:", data)
            required_params = ["tenant_id", "sub_tenant_id", "workorder_id",
                               "opn_num", "part_num"]
            missing_params = [param for param in required_params if not
                              data.get(param)]
            if missing_params:
                return FIAResponse(json=json.dumps({"status": False, "message \
                    ": f"Missing required parameters:\
                        {', '.join(missing_params)}"}))

            response_details = []
            if 'part_serial_num_list' in data:
                for part in data['part_serial_num_list']:
                    part_data = data.copy()
                    part_data.update(part)
                    del part_data['part_serial_num_list']

                    if part_data.get("is_fpi"):
                        check_param = {
                            "tenant_id": part_data["tenant_id"],
                            "sub_tenant_id": part_data["sub_tenant_id"],
                            "opn_num": part_data["opn_num"],
                            "part_num": part_data["part_num"],
                            "workorder_id": {"$ne": part_data["workorder_id"]}
                        }
                        existing_entry = self.model.get_one_fia_status(
                            check_param)
                        if (existing_entry.get("status")
                                and existing_entry.get("data")):
                            response_details.append({"part_serial_num": part['\
                                part_serial_num'], "status": False, "message\
                                    ": "Duplicate entry exists with a \
                                        different work order ID."})
                            continue

                    insert_result = self.model.insert_fia_status(part_data)
                    if insert_result.get("status"):
                        response_details.append(
                            {"part_serial_num": part['part_serial_num'], "\
                                status": True, "message": "Inserted \
                                    successfully"})
                    else:
                        response_details.append(
                            {"part_serial_num": part['part_serial_num'], "\
                                status": False, "message": "Insert failed"})

                return FIAResponse(json=json.dumps({"status": True, "message\
                    ": "Processed", "details": response_details}))
            else:
                insert_result = self.model.insert_fia_status(data)
                if insert_result.get("status"):
                    return FIAResponse(json=json.dumps({"status": True,
                                                        "message": "FIA status\
                                                        posted successfully"}))
                else:
                    return FIAResponse(json=json.dumps(insert_result))

        except Exception as e:
            return FIAResponse(json=json.dumps({"status": False,
                                                "message": str(e)}))

    def UpdateFiaStatus(self, request, context):
        try:
            data = json.loads(request.json)
            print("Data recieved:", data)
            for entry in data:
                mandatory_fields = ["machine_num", "workorder_id", "part_num",
                                    "opn_num", "part_serial_num"]
                if not all(field in entry for field in mandatory_fields):
                    return FIAResponse(json=json.dumps({"status": False,
                                                        "message": "Missing \
                                    mandatory field in one or more entries."}))

                query_param = {field: entry[field] for field in
                               mandatory_fields}
                existing_entry = self.model.get_one_fia_status(query_param)
                if (not existing_entry.get("status") or
                        not existing_entry.get("data")):
                    return FIAResponse(json=json.dumps({"status": False,
                                                        "message": "No \
                                            existing entry found for update"}))
                qa_status = (
                    "Accepted" if entry.get("is_qms", False) else "Rejected"
                )
                update_data = {
                    "qa_status": qa_status,
                    "inspected_by": entry.get("inspected_by", "")
                }
                update_result = self.model.update_fia_status(
                    query_param, update_data)
                if not update_result.get("status"):
                    return FIAResponse(json=json.dumps({"status": False,
                                                        "message": "Update\
                                                    failed for this entry"}))

            return FIAResponse(json=json.dumps({"status": True,
                                                "message": "All entries\
                                                    updated successfully"}))
        except Exception as e:
            return FIAResponse(json=json.dumps({"status": False,
                                                "message": str(e)}))

    def GetDataQaStatus(self, request, context):
        try:
            query = json.loads(request.json)
            print(query)
            required_params = [
                "machine_num", "MTS_num", "workorder_id", "opn_num", "part_num"
            ]
            missing_params = [
                param for param in required_params
                if param not in query or not query.get(param)
            ]
            if missing_params:
                missing_msg = f"Missing required \
                    parameters: {', '.join(missing_params)}"
                return FIAResponse(json=json.dumps({"status": False,
                                                    "message": missing_msg}))

            query_params = {
                "tenant_id": query.get("tenant_id"),
                "sub_tenant_id": query.get("sub_tenant_id"),
                "machine_num": query.get("machine_num"),
                "MTS_num": query.get("MTS_num"),
                "unit_id": query.get("unit_id"),
                "dept_id": query.get("dept_id"),
                "workorder_id": query.get("workorder_id"),
                "opn_num": query.get("opn_num"),
                "part_num": query.get("part_num")
            }
            projection = {"_id": 0, "qa_status": 1, "is_fpi": 1,
                          "inspected_by": 1, "part_serial_num": 1}

            response = self.model.get_all_fia_status(query_params, projection,
                                                     page=1, limit=10)
            records = response.get("data", {}).get("records", [])
            if not records:
                return FIAResponse(json=json.dumps({"status": False,
                                                    "message": "FIA status \
                                                        not found"}))

            formatted_response = {
                "part_serial_num_list": [
                    {
                        "machine_num": record.get("machine_num", ""),
                        "MTS_num": record.get("MTS_num", ""),
                        "tenant_id": record.get("tenant_id", ""),
                        "sub_tenant_id": record.get("sub_tenant_id", ""),
                        "workorder_id": record.get("workorder_id"),
                        "opn_num": record.get("opn_num"),
                        "part_num": record.get("part_num"),
                        "part_serial_num": record.get("part_serial_num", ""),
                        "qa_status": record.get("qa_status", ""),
                        "is_fpi": record.get("is_fpi", ""),
                        "inspected_by": record.get("inspected_by", "")
                    } for record in records
                ]
            }

            return FIAResponse(json=json.dumps({"status": True,
                                                "data": formatted_response}))
        except Exception as e:
            return FIAResponse(json=json.dumps({"status": False,
                                                "message": str(e)}))
