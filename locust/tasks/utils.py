import json


def log_failure(action: str, response, extra_info=None):
	print(f'[{action}] - Status: {response.status_code}')
	print(f'Response: {response.text}')
	if extra_info:
		print(f'Info: {json.dumps(extra_info, indent=2, default=str)}')
