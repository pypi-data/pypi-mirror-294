from .custom_logger import *


def tester():
    return "Testing successful..."


def test_custom_logger():
    x = custom_logger()
    print(x.initialise_database("logging_data","usage_data"))
    print(x.store_log("test,test,test"))