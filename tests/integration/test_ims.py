import os

import requests_mock

import zeep


def read_file(file_name, folder='wsdl_ims'):
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder, file_name)
    with open(file, encoding='UTF-8') as f:
        return f.read()


def test_find_product(ims_login_token):
    with requests_mock.mock() as m:
        m.get("http://example.com/inventory?wsdl", text=read_file("inventory.wsdl"))
        for i in range(33):
            m.get(f"http://example.com/Inventory?xsd=xsd{i}",
                  text=read_file(f"Inventory?xsd=xsd{i}"))
        m.post("http://example.com/Inventory/iInventoryHttp",
               text=read_file("find_product_by_name_response.xml", 'mock_ims'))
        # set strict to True -> then data will be available in _raw_elements
        client = zeep.Client('http://example.com/inventory?wsdl', strict=True)
        filter_fields = [{"FilterField": {"Name": "Name", "SelectedOperator": "OperationEquals", "Value": "LP"}}]
        filter = {"Filters": filter_fields}
        pager = {"StartElement": 0, "Descending": False, "NumberOfElements": 10,
                 "OrderByProperty": None}
        assert client.service.GetAllProductsFiltered(pager=pager, filter=filter, sessionToken=ims_login_token)


def test_find_customer(ims_login_token):
    with requests_mock.mock() as m:
        m.get("http://example.com/inventory?wsdl", text=read_file("inventory.wsdl"))
        for i in range(33):
            m.get(f"http://example.com/Inventory?xsd=xsd{i}",
                  text=read_file(f"Inventory?xsd=xsd{i}"))
        m.post("http://example.com/Inventory/iInventoryHttp",
               text=read_file("find_customer_by_name_response.xml", 'mock_ims'))
        # set strict to True -> then data will be available in _raw_elements
        client = zeep.Client('http://example.com/inventory?wsdl', strict=True)
        filter_fields = [{"FilterField": {"Name": "Name", "SelectedOperator": "OperationEquals", "Value": "SURFNET"}}]
        filter = {"Filters": filter_fields}
        pager = {"StartElement": 0, "Descending": False, "NumberOfElements": 10,
                 "OrderByProperty": None}
        assert client.service.GetAllCustomersFiltered(pager=pager, filter=filter, sessionToken=ims_login_token)
