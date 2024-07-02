import argparse
import json

class methodResponse:
    def __init__(self, responseType):
        self.responseType = responseType
        self.total_number_of_files = 0
        self.successful_files = []
        self.failed_files = []
    
    def add_successful_file(self, file_name, number_of_records):
        self.successful_files.append({
            "fileName": file_name,
            "numberOfRecords": number_of_records
        })
        self.total_number_of_files += 1
    
    def add_failed_file(self, file_name, error_message):
        self.failed_files.append({
            "fileName": file_name,
            "errorMessage": error_message
        })
        self.total_number_of_files += 1
    
    def generate_json(self):
        result = {
            "status": self.responseType,
            "totalNumberOfFiles": self.total_number_of_files,
            "results": [
                {
                    "succeed": {
                        "numberOfFiles": len(self.successful_files),
                        "files": self.successful_files
                    },
                    "failed": {
                        "numberOfFiles": len(self.failed_files),
                        "files": self.failed_files
                    }
                }
            ]
        }
        return json.dumps(result, indent=4)


class ErrorResponseGenerator:
    def __init__(self, code, origin, message):
        self.status = "fail"
        self.error = {
            "origin": origin,
            "code": code,
            "message": message
        }

    def get_response(self):
        """
        Returns the error response as a dictionary.
        """
        return {
            "status": self.status,
            "error": self.error
        }

    def get_response_json(self):
        """
        Returns the error response as a JSON string.
        """
        return json.dumps(self.get_response(), indent=4)
    
class SuccessResponseGenerator:
    def __init__(self, num_of_records):
        self.status = "success"
        self.code = 200
        self.records_sent = num_of_records

    def get_response(self):
        """
        Returns the error response as a dictionary.
        """
        return {
            "status": self.status,
            "code": self.code,
            "records_sent": self.records_sent
        }

    def get_response_json(self):
        """
        Returns the error response as a JSON string.
        """
        return json.dumps(self.get_response(), indent=4)
    
