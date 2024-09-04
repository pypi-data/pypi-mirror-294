"""Test for bulk.py"""
import copy
import itertools
import json
import random
from unittest import mock

import pytest
from pytest_httpx import HTTPXMock

from simple_salesforce.exceptions import SalesforceGeneralError
from simple_salesforce.aio.bulk import AsyncSFBulkType


def test_bulk_handler(sf_client, constants):
    """Test that BulkHandler Loads Properly"""
    bulk_handler = sf_client.bulk
    assert bulk_handler.session_id == sf_client.session_id
    assert bulk_handler.bulk_url == sf_client.bulk_url
    assert constants["BULK_HEADERS"] == bulk_handler.headers


def test_bulk_type(sf_client, constants):
    """Test bulk type creation"""
    contact = sf_client.bulk.Contact
    assert contact.bulk_url == sf_client.bulk_url
    assert constants["BULK_HEADERS"] == contact.headers
    assert "Contact" == contact.object_name


EXPECTED_RESULT = [
    {"success": True, "created": True, "id": "001xx000003DHP0AAO", "errors": []},
    {"success": True, "created": True, "id": "001xx000003DHP1AAO", "errors": []},
]
EXPECTED_QUERY = [
    {
        "Id": "001xx000003DHP0AAO",
        "AccountId": "ID-13",
        "Email": "contact1@example.com",
        "FirstName": "Bob",
        "LastName": "x",
    },
    {
        "Id": "001xx000003DHP1AAO",
        "AccountId": "ID-24",
        "Email": "contact2@example.com",
        "FirstName": "Alice",
        "LastName": "y",
    },
    {
        "Id": "001xx000003DHP0AAO",
        "AccountId": "ID-13",
        "Email": "contact1@example.com",
        "FirstName": "Bob",
        "LastName": "x",
    },
    {
        "Id": "001xx000003DHP1AAO",
        "AccountId": "ID-24",
        "Email": "contact2@example.com",
        "FirstName": "Alice",
        "LastName": "y",
    },
]



@pytest.mark.parametrize(
    "operation,method_name",
    (
        ("delete", "delete"),
        ("insert", "insert"),
        ("update", "update"),
        ("hardDelete", "hard_delete"),
    ),
)
async def test_insert(operation, method_name, sf_client, httpx_mock: HTTPXMock):
    """Test bulk insert records"""
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = copy.deepcopy(body1)
    body3["state"] = "Closed"
    body4 = copy.deepcopy(body2)
    body4["state"] = "InProgress"
    body5 = copy.deepcopy(body2)
    body5["state"] = "Completed"
    body6 = [
        {"success": True, "created": True, "id": "001xx000003DHP0AAO", "errors": []},
        {"success": True, "created": True, "id": "001xx000003DHP1AAO", "errors": []},
    ]
    body7 = {}
    all_bodies = [body1, body2, body3, body4, body5, body6, body7]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)
    data = [
        {
            "AccountId": "ID-1",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "AccountId": "ID-2",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    function = getattr(sf_client.bulk.Contact, method_name)
    coro = await function(data, wait=0.1)
    results = []
    async for result in coro:
        results.append(result)
    assert EXPECTED_RESULT == results


async def test_upsert(sf_client, httpx_mock: HTTPXMock):
    """Test bulk upsert records"""
    operation = "delete"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = copy.deepcopy(body1)
    body3["state"] = "Closed"
    body4 = copy.deepcopy(body2)
    body4["state"] = "InProgress"
    body5 = copy.deepcopy(body2)
    body5["state"] = "Completed"
    body6 = [
        {"success": True, "created": True, "id": "001xx000003DHP0AAO", "errors": []},
        {"success": True, "created": True, "id": "001xx000003DHP1AAO", "errors": []},
    ]
    body7 = {}
    all_bodies = [body1, body2, body3, body4, body5, body6, body7]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = [{"id": "ID-1"}, {"id": "ID-2"}]
    results = []
    coro = await sf_client.bulk.Contact.upsert(data, "some-field", wait=0.1)
    async for result in coro:
        results.append(result)

    assert EXPECTED_RESULT == results



async def test_query(httpx_mock: HTTPXMock, sf_client):
    """Test bulk query"""
    operation = "query"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = copy.deepcopy(body1)
    body3["state"] = "Closed"
    body4 = copy.deepcopy(body2)
    body4["state"] = "InProgress"
    body5 = copy.deepcopy(body2)
    body5["state"] = "Completed"
    body6 = ["752x000000000F1", "752x000000000F2"]
    body7 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-13",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-24",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    body8 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-13",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-24",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    all_bodies = [body1, body2, body3, body4, body5, body6, body7, body8]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = "SELECT Id,AccountId,Email,FirstName,LastName FROM Contact"
    result = await sf_client.bulk.Contact.query(data, wait=0.1, lazy_operation=False)
    assert body7[0] in result
    assert body7[1] in result
    assert body8[0] in result
    assert body8[1] in result



async def test_query_all(httpx_mock: HTTPXMock, sf_client):
    """Test bulk query all"""
    operation = "queryAll"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = copy.deepcopy(body1)
    body3["state"] = "Closed"
    body4 = copy.deepcopy(body2)
    body4["state"] = "InProgress"
    body5 = copy.deepcopy(body2)
    body5["state"] = "Completed"
    body6 = ["752x000000000F1", "752x000000000F2"]
    body7 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-13",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-24",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    body8 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-13",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-24",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    all_bodies = [body1, body2, body3, body4, body5, body6, body7, body8]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = "SELECT Id,AccountId,Email,FirstName,LastName FROM Contact"
    result = await sf_client.bulk.Contact.query_all(
        data, wait=0.1, lazy_operation=False
    )
    assert body7[0] in result
    assert body7[1] in result
    assert body8[0] in result
    assert body8[1] in result



async def test_query_lazy(httpx_mock: HTTPXMock, sf_client):
    """Test lazy bulk query"""
    operation = "queryAll"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = copy.deepcopy(body1)
    body3["state"] = "Closed"
    body4 = copy.deepcopy(body2)
    body4["state"] = "InProgress"
    body5 = copy.deepcopy(body2)
    body5["state"] = "Completed"
    body6 = ["752x000000000F1", "752x000000000F2"]
    body7 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-13",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-24",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    body8 = [
        {
            "Id": "001xx000003DHP0AAO",
            "AccountId": "ID-15",
            "Email": "contact1@example.com",
            "FirstName": "Bob",
            "LastName": "x",
        },
        {
            "Id": "001xx000003DHP1AAO",
            "AccountId": "ID-26",
            "Email": "contact2@example.com",
            "FirstName": "Alice",
            "LastName": "y",
        },
    ]
    all_bodies = [body1, body2, body3, body4, body5, body6, body7, body8]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = "SELECT Id,AccountId,Email,FirstName,LastName FROM Contact"
    results = []
    coro = await sf_client.bulk.Contact.query_all(data, wait=0.1, lazy_operation=True)
    async for result in coro:
        results.append(result)
    assert body7[0] in results[0]
    assert body7[1] in results[0]
    assert body8[0] in results[1]
    assert body8[1] in results[1]
    # [[{'Id': '001xx000003DHP0AAO', 'AccountId': 'ID-13',
    # 'Email': 'contact1@example.com', 'FirstName': 'Bob',
    # 'LastName': 'x'}, {'Id': '001xx000003DHP1AAO',
    # 'AccountId': 'ID-24', 'Email': 'contact2@example.com',
    # 'FirstName': 'Alice', 'LastName': 'y'}],
    # [{'Id': '001xx000003DHP0AAO', 'AccountId': 'ID-13',
    # 'Email': 'contact1@example.com', 'FirstName': 'Bob',
    # 'LastName': 'x'}, {'Id': '001xx000003DHP1AAO',
    # 'AccountId': 'ID-24', 'Email': 'contact2@example.com',
    # 'FirstName': 'Alice', 'LastName': 'y'}]]



async def test_query_fail(httpx_mock: HTTPXMock, sf_client):
    """Test bulk query records failure"""
    operation = "query"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open",
    }
    body2 = {"id": "Batch-1", "jobId": "Job-1", "state": "Queued"}
    body3 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON",
        "id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Closed",
    }
    body4 = {"id": "Batch-1", "jobId": "Job-1", "state": "InProgress"}
    body5 = {
        "id": "Batch-1",
        "jobId": "Job-1",
        "state": "Failed",
        "stateMessage": "InvalidBatch : Failed to process query",
    }
    all_bodies = [body1, body2, body3, body4, body5]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = "SELECT ASDFASfgsds FROM Contact"
    with pytest.raises(SalesforceGeneralError) as exc:
        await sf_client.bulk.Contact.query(data, wait=0.1)
        assert exc.status == body5["state"]
        assert exc.resource_name == body5["jobId"]
        assert exc.content == body5["stateMessage"]


async def test_bulk_operation_auto_batch_size(httpx_mock: HTTPXMock, sf_client):
    """Test that batch_size="auto" leads to using _add_autosized_batches"""
    operation = "update"
    body1 = {
        "apiVersion": 42.0,
        "concurrencyMode": "Parallel",
        "contentType": "JSON","id": "Job-1",
        "object": "Contact",
        "operation": operation,
        "state": "Open"
    }
    body2 = {
        "apiVersion" : 42.0,
        "concurrencyMode" : "Parallel",
        "contentType" : "JSON",
        "id" : "Job-1",
        "object" : "Contact",
        "operation" : operation,
        "state" : "Closed"
    }

    all_bodies = [body1, body2]
    for body in all_bodies:
        httpx_mock.add_response(200, json=body)

    data = [{
        'AccountId': 'ID-1',
        'Email': 'contact1@example.com',
        'FirstName': 'Bob',
        'LastName': 'x'
    }]
    results = []
    async for result in sf_client.bulk.Contact._bulk_operation(
        operation, data, batch_size="auto"
    ):
        results.append(result)
    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    req1, req2 = requests

    http_methods = set((req1.method, req2.method))
    http_urls = (req1.url.path, req2.url.path)
    assert http_methods == {"POST"}
    assert http_urls[0].endswith("/async/job")
    assert http_urls[1].endswith("/async/job/Job-1")


@mock.patch('simple_salesforce.aio.bulk.AsyncSFBulkType._add_batch')
async def test_add_autosized_batches(add_batch, httpx_mock: HTTPXMock, sf_client):
    """Test that _add_autosized_batches batches all records correctly"""
    # _add_autosized_batches passes the return values from add_batch, so we
    # can pass the data it was given back so that we can test it

    data = [
        # Expected serialized record size of 13 to 1513. Idea is that
        # earlier record batches are split on record count, whereas later
        # batches are split for hitting the byte limit.
        {'key': 'value' * random.randint(0, i // 50)}
        for i in range(30000)
    ]

    add_batch.side_effect = lambda job_id, data, operation: data
    sf_bulk_type = AsyncSFBulkType(None, None, None, None)
    result = await sf_bulk_type._add_autosized_batches(  # pylint: disable=protected-access
        data=data, operation="update", job="Job-1"
    )
    reconstructed_data = list(itertools.chain(*result))
    # all data was put in a batch
    assert len(data) == len(reconstructed_data)
    assert data == list(itertools.chain(*result))

    for i, batch in enumerate(result):
        record_count = len(batch)
        size_in_bytes = len(json.dumps(batch))
        is_last_batch = i == len(result) - 1
        # Check that all batches are within limits
        assert record_count <= 10_000
        assert size_in_bytes <= 10_000_000
        # ... and that - except for the last batch - all batches have maxed
        # out one of the two limits
        assert (
            is_last_batch or
            record_count == 10_000 or
            (size_in_bytes + len(json.dumps(result[i + 1][0])) + 2
                > 10_000_000)
        )