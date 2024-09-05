import json


class RequestsManager:
    def __init__(self):
        self.driver = None

    def capture_request(self):
        all_logs = self.driver.get_log('performance')
        requests = {}
        logs = [json.loads(entry["message"]) for entry in all_logs]
        network_logs = list(filter(lambda log: "Network." in log["message"]["method"], logs))
        for log_json in network_logs:
            message = log_json["message"]
            request_id = message["params"].get("requestId")

            if not request_id:
                continue

            if not requests.get(request_id):
                requests[request_id] = {"url": None,
                                        "status_code": None,
                                        "status_text": None,
                                        "type": None,
                                        "log_data": [], }

            requests[request_id]["log_data"].append(message)
            if message["method"] == "Network.requestWillBeSent":
                requests[request_id]["url"] = message["params"]["request"]["url"]
                requests[request_id]["method"] = message["params"]["request"]["method"]
            elif message["method"] == "Network.responseReceived":
                requests[request_id]["status_code"] = message["params"]["response"]["status"]
                requests[request_id]["status_text"] = message["params"]["response"]["statusText"]
                requests[request_id]["type"] = message["params"]["type"]

        return requests
