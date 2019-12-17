from typing import Dict, Any
import json
import re
import pytest
import requests
from requests import Session, Response


# get reset url response before every test
# @pytest.fixture()
def server_reset():
	s = requests.Session()
	in_url = 'http://127.0.0.1:6543/reset'
	out = s.post(url=in_url, data={}, json=[])
	return out


# check if quotes endpoint is ok
@pytest.fixture()
def server_quotes():
	# data = {}
	in_url = 'http://127.0.0.1:6543/quotes'
	response = requests.get(in_url)  # , params=data)
	print(response)
	return response.status_code


# funtion to return ids of quotes
def get_quotes():
	index = 0
	new_lst = []
	in_url = 'http://127.0.0.1:6543/quotes'
	get_quotes_req = requests.get(in_url)
	quote = get_quotes_req.json()
	lst_data = quote['data']
	print(lst_data)
	id_lst = ([d['id'] for d in lst_data])
	print(id_lst)
	return id_lst


@pytest.fixture()
@pytest.mark.dependency(depends=["server_quotes"])
def get_quotes_validation():
	result1 = check_if_duplicates_Ids(get_quotes())
	result2 = check_if_sorted_id(get_quotes())
	print(result1)
	print(result2)
	if result1:
		if result2:
			return True
		else:
			return False
	else:
		return False


def check_if_duplicates_Ids(id_lst):
	for elem in id_lst:
		if id_lst.count(elem) > 1:
			return False
	print('No Duplicate ids found.Test passed')
	return True


def check_if_sorted_id(id_lst):
	expect_list1 = [1, 2, 3, 4, 5, 6, 7]
	print(id_lst)
	if id_lst == expect_list1:
		return True
	else:
		return False


@pytest.mark.dependency(depends=["server_quotes"])
@pytest.fixture()
# get quote by id
def get_quote_by_id(quote_id):
	in_url = 'http://127.0.0.1:6543/quotes'
	params = {'id': quote_id}
	new_url = "{}/{}".format(in_url, quote_id)
	get_quote_details = requests.get(new_url, params=params)
	if get_quote_details.status_code == 404:
		print("Quote id does not exists")
	else:
		quote_data = get_quote_details.json()
		data = quote_data['data']
		print(data)
	return data


@pytest.fixture()
# compare quote id details with actual response
def compare_quote_data():
	data = get_quote_by_id(4)

	expected_quote = [{
		"id": 1,
		"text": "We have nothing to fear but fear itself!"
	}, {
		"id": 2,
		"text": "All work and no play makes Jack a dull boy."
	}, {
		"id": 3,
		"text": "Travel is fatal to prejudice, bigotry, and narrow-mindedness."
	}, {
		"id": 4,
		"text": "What a day"
	}]

	if re.search(json.dumps(data), json.dumps(expected_quote)):
		print("valid quote id and text")
		flag = True
	else:
		flag = False
	return flag

@pytest.fixture()
def del_quote_by_id(q_id):
	in_url = 'http://127.0.0.1:6543/quotes'
	params = {'id': q_id}
	new_url = "{}/{}".format(in_url, q_id)
	print("new_url {0}   id {1}".format(new_url,q_id))
	del_response = requests.delete(new_url, params=params)
	if del_response.status_code == 200:
		get_resp = requests.get(new_url, params=params)
		if get_resp.status_code == 404:
			print('quote id {0} deleted sucessfully'.format(q_id))
			flag = True
	else:
		print('Unable to delete quote')
		flag = False
	return flag

def get_last_quote_id():
	new_lst = get_quotes()
	max_id = max(new_lst)
	print(max_id)
	return max_id


@pytest.fixture()
def post_quote():
	url = 'http://127.0.0.1:6543/quotes'
#out = server_reset()
	last_quote_id = get_last_quote_id()
	payload = {'text': 'writing the history today'}
	if type(payload['text']) == str:
		print('payload is string')
		for value in payload:
			print (value)
			response = requests.post(url,data=json.dumps(payload))
			print(response.json())
			if response.status_code == 200:
				new_quote_id = get_last_quote_id()
				if new_quote_id == last_quote_id+1:
					print("New quote id  last quote id+1")
					flag = True
				else:
					print("new quote id is not last id +1. Something went wrong.Your test migth failed")
					flag = False
			else:
				flag = False
	else:
		response = None
		print("Payload is not string,post unsucessful")
		flag = False
	return flag



