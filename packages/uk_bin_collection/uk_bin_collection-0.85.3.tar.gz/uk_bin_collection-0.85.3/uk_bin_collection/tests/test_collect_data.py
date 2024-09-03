import json
from unittest import mock

import pytest
from requests import exceptions as req_exp
from requests.models import Response
from uk_bin_collection.get_bin_data import AbstractGetBinDataClass as agbdc
from uk_bin_collection.get_bin_data import setup_logging
import logging


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, raise_error_type):
            self.text = json_data
            self.status_code = status_code
            if raise_error_type is not None:
                self.raise_for_status = self.raise_error(raise_error_type)
            else:
                self.raise_for_status = lambda: None

        def raise_error(self, errorType):
            if errorType == "HTTPError":
                raise req_exp.HTTPError()
            elif errorType == "ConnectionError":
                raise req_exp.ConnectionError()
            elif errorType == "Timeout":
                raise req_exp.Timeout()
            elif errorType == "RequestException":
                raise req_exp.RequestException()
            return errorType

    if args[0] == "aurl":
        return MockResponse({"test_data": "test"}, 200, None)
    elif args[0] == "HTTPError":
        return MockResponse({}, 999, "HTTPError")
    elif args[0] == "ConnectionError":
        return MockResponse({}, 999, "ConnectionError")
    elif args[0] == "Timeout":
        return MockResponse({}, 999, "Timeout")
    elif args[0] == "RequestException":
        return MockResponse({}, 999, "RequestException")
    elif args[0] == "notPage":
        return MockResponse("not json", 200, None)
    return MockResponse(None, 404, "HTTPError")


# Unit tests


def test_logging_exception():
    logging_dict = "SW1A 1AA"
    with pytest.raises(ValueError) as exc_info:
        result = setup_logging(logging_dict, "ROOT")
    assert exc_info.typename == "ValueError"


def test_setup_logging_valid_config():
    # Example of a minimal valid logging configuration dictionary
    logging_config = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "ROOT": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }
    logger_name = "ROOT"
    # Run the function with valid logging configuration
    logger = setup_logging(logging_config, logger_name)

    # Assert that logger is correctly configured
    assert logger.name == logger_name
    assert logger.level == logging.DEBUG


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_data(mock_get):
    page_data = agbdc.get_data("aurl")
    assert page_data.text == {"test_data": "test"}


@pytest.mark.parametrize(
    "url", ["HTTPError", "ConnectionError", "Timeout", "RequestException"]
)
@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_data_error(mock_get, url):
    with pytest.raises(Exception) as exc_info:
        result = agbdc.get_data(url)
    assert exc_info.typename == url


def test_output_json():
    bin_data = {"bin": ""}
    output = agbdc.output_json(bin_data)
    assert type(output) == str
    assert output == '{\n    "bin": ""\n}'

class ConcreteGetBinDataClass(agbdc):
    """Concrete implementation of the abstract class to test abstract methods."""
    def parse_data(self, page: str, **kwargs) -> dict:
        return {"mock_key": "mock_value"}

@pytest.fixture
def concrete_class_instance():
    return ConcreteGetBinDataClass()

def test_get_and_parse_data_no_skip_get_url(concrete_class_instance):
    mock_page = "mocked page content"
    mock_parsed_data = {"mock_key": "mock_value"}

    with mock.patch.object(concrete_class_instance, 'get_data', return_value=mock_page) as mock_get_data, \
         mock.patch.object(concrete_class_instance, 'parse_data', return_value=mock_parsed_data) as mock_parse_data:
        
        result = concrete_class_instance.get_and_parse_data("http://example.com")

        mock_get_data.assert_called_once_with("http://example.com")
        mock_parse_data.assert_called_once_with(mock_page, url="http://example.com")
        assert result == mock_parsed_data

def test_get_and_parse_data_skip_get_url(concrete_class_instance):
    mock_parsed_data = {"mock_key": "mock_value"}

    with mock.patch.object(concrete_class_instance, 'parse_data', return_value=mock_parsed_data) as mock_parse_data:
        
        result = concrete_class_instance.get_and_parse_data("http://example.com", skip_get_url=True)

        mock_parse_data.assert_called_once_with("", url="http://example.com", skip_get_url=True)
        assert result == mock_parsed_data