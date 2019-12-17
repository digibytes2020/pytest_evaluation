import pytest
import requests
from requests import Session, Response


# Check server reset url
# def test_server_test(server_reset):
#	assert server_reset.status_code == 200


# Check if you are able to post '''
from API.conftest import post_quote


def test_server_stat(server_quotes):
	assert server_quotes == 200


# check if get quotes test case is ok
def test_get_quotes(get_quotes_validation):
	assert get_quotes_validation == True


# Test case to get data for a given quote id and check not None
testdata = [1,2,3,4,6,7,8]
@pytest.mark.parametrize("quote_id", testdata)
def test_get_quote_status(get_quote_by_id):
	assert get_quote_by_id is not None


# test case to get Quote id and compare the response
def test_compare_quotes_by_id(compare_quote_data):
	assert compare_quote_data == True




# delete quote by id and status check
testdata1 = [9]
@pytest.mark.parametrize("q_id", testdata1)
def test_del_quote_by_id(del_quote_by_id):
	assert del_quote_by_id == True

def test_post_quote():
	assert post_quote() == True