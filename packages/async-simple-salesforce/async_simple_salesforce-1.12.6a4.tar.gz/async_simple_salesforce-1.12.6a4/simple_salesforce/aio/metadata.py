"""Async Class to work with Salesforce Metadata API """

from base64 import b64encode, b64decode
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

import aiofiles
import httpx
from zeep import AsyncClient, Settings
from zeep.proxy import AsyncServiceProxy
from zeep.xsd import AnySimpleType, ComplexType, CompoundValue


from simple_salesforce.messages import (
    DEPLOY_MSG,
    CHECK_DEPLOY_STATUS_MSG,
    CHECK_RETRIEVE_STATUS_MSG,
    RETRIEVE_MSG,
)
from simple_salesforce.util import Headers
from .aio_util import call_salesforce


class AsyncMetadataType:
    """
    Salesforce Metadata Type (using Async Zeep client)
    """

    def __init__(
        self,
        name: str,
        service: AsyncServiceProxy,
        zeep_type: ComplexType | AnySimpleType,
        session_header: CompoundValue,
    ):
        """
        Initialize metadata type

        :param name: Name of metadata type
        :type name: str
        :param service: Zeep service
        :type service: zeep.proxy.AsyncServiceProxy
        :param zeep_type: Zeep type object
        :type zeep_type: zeep.xsd.ComplexType or zeep.xsd.AnySimpleType
        :param session_header: Session Id header for Metadata API calls
        """
        self._name = name
        self._service = service
        self._zeep_type = zeep_type
        self._session_header = session_header

    @staticmethod
    def _handle_api_response(response: List[Any]) -> None:
        """
        Parses SaveResult and DeleteResult objects to identify if there was
        an error, and raises exception accordingly

        :param response: List of zeep.objects.SaveResult or
        zeep.objects.DeleteResult objects
        :type response: list
        :raises Exception: If any Result object contains one or more error
        messages
        """
        err_string = ""
        for result in response:
            if not result.success:
                err_string += f"\n{result.fullName}: "
                for error in result.errors:
                    err_string += f"({error.statusCode}, {error.message}), "
        if err_string:
            raise Exception(err_string)

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Creates a new object of this metadata type

        :param args: Parameters to pass to zeep.xsd.AnySimpleType
        :param kwargs: Parameters to pass to zeep.xsd.ComplexType
        :returns: An object of type self._name
        """
        return await self._zeep_type(*args, **kwargs)

    async def create(self, metadata: List[Any]) -> None:
        """
        Performs a createMetadata call

        :param metadata: Array of one or more metadata components.
                         Limit: 10. (For CustomMetadata and CustomApplication
                         only, the limit is 200.)
                         You must submit arrays of only one type of
                         component. For example, you can submit an
                         array of 10 custom objects or 10 profiles, but not a
                         mix of both types.
        :type metadata: list
        """
        response = await self._service.createMetadata(
            metadata, _soapheaders=[self._session_header]
        )
        self._handle_api_response(response)

    async def read(self, full_names: List[str]) -> List[Any] | Any:
        """
        Performs a readMetadata call

        :param full_names: Array of full names of the components to read.
                           Limit: 10. (For CustomMetadata and
                           CustomApplication only, the limit is 200.)
                           You must submit arrays of only one type of
                           component. For example, you can submit an array
                           of 10 custom objects or 10 profiles, but not a mix
                           of both types.
        :type full_names: list
        :returns: A list of metadata components
        :rtype: list
        """
        response = await self._service.readMetadata(
            self._name, full_names, _soapheaders=[self._session_header]
        )
        if len(response) == 1:
            return response[0]
        return response

    async def update(self, metadata: List[Any]) -> None:
        """
        Performs an updateMetadata call. All required fields must be passed
        for each component

        :param metadata: Array of one or more metadata components.
                         Limit: 10. (For CustomMetadata and CustomApplication
                         only, the limit is 200.)
                         You must submit arrays of only one type of
                         component. For example, you can submit an
                         array of 10 custom objects or 10 profiles, but not a
                         mix of both types.
        :type metadata: list
        """
        response = await self._service.updateMetadata(
            metadata, _soapheaders=[self._session_header]
        )
        self._handle_api_response(response)

    async def upsert(self, metadata: List[Any]) -> None:
        """
        Performs an upsertMetadata call. All required fields must be passed
        for each component

        :param metadata: Array of one or more metadata components.
                         Limit: 10. (For CustomMetadata and CustomApplication
                         only, the limit is 200.)
                         You must submit arrays of only one type of
                         component. For example, you can submit an
                         array of 10 custom objects or 10 profiles, but not a
                         mix of both types.
        :type metadata: list
        """
        response = await self._service.upsertMetadata(
            metadata, _soapheaders=[self._session_header]
        )
        self._handle_api_response(response)

    async def delete(self, full_names: List[Dict[str, Any]]) -> None:
        """
        Performs a deleteMetadata call

        :param full_names: Array of full names of the components to delete.
                           Limit: 10. (For CustomMetadata and
                           CustomApplication only, the limit is 200.)
                           You must submit arrays of only one type of
                           component. For example, you can submit an array
                           of 10 custom objects or 10 profiles, but not a mix
                           of both types.
        :type full_names: list
        """
        response = await self._service.deleteMetadata(
            self._name, full_names, _soapheaders=[self._session_header]
        )
        self._handle_api_response(response)

    async def rename(self, old_full_name: str, new_full_name: str) -> None:
        """
        Performs a renameMetadata call

        :param old_full_name: The current component full name.
        :type old_full_name: str
        :param new_full_name: The new component full name.
        :type new_full_name: str
        """
        result = await self._service.renameMetadata(
            self._name,
            old_full_name,
            new_full_name,
            _soapheaders=[self._session_header],
        )
        self._handle_api_response([result])

    async def describe(self) -> Any:
        """
        Performs a describeValueType call

        :returns: DescribeValueTypeResult
        """
        return await self._service.describeValueType(
            f"{{http://soap.sforce.com/2006/04/metadata}}{self._name}",
            _soapheaders=[self._session_header],
        )


class AsyncSfdcMetadataApi:
    # pylint: disable=too-many-instance-attributes
    """Class to work with Salesforce Metadata API"""
    _METADATA_API_BASE_URI = "/services/Soap/m/{version}"
    _XML_NAMESPACES = {
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "mt": "http://soap.sforce.com/2006/04/metadata",
    }

    # pylint: disable=R0913
    def __init__(
        self,
        session_id: str,
        instance: str,
        metadata_url: str,
        headers: Headers,
        api_version: str | None,
        session_factory: Optional[Callable[[], httpx.AsyncClient]] = None,
    ):
        """Initialize and check session"""
        self._session_id = session_id
        self._instance = instance
        self.metadata_url = metadata_url
        self.headers = headers
        self._api_version = api_version
        self._deploy_zip = None
        self.session_factory = session_factory

        wsdl_path = Path(__file__).parent.parent / "metadata.wsdl"

        # The zeep client synchronously loads the wsdl file
        self._client = AsyncClient(
            str(wsdl_path.absolute()),
            settings=Settings(strict=False, xsd_ignore_sequence_order=True),
        )  # type: ignore[no-untyped-call]
        # Odd that we can't create this easily from zeep itself
        self._service: AsyncServiceProxy = AsyncServiceProxy(
            self._client,
            self._client.service._binding,
            address=self.metadata_url,
        )  # type: ignore[no-untyped-call]
        self._session_header: Element = self._client.get_element(
            "ns0:SessionHeader"  # type: ignore[no-untyped-call]
        )(sessionId=self._session_id)

    def __getattr__(self, item: str) -> "AsyncMetadataType":
        return AsyncMetadataType(
            item,
            self._service,
            self._client.get_type("ns0:" + item),  # type: ignore[no-untyped-call]
            self._session_header,
        )

    async def describe_metadata(self) -> Any:
        """
        Performs a describeMetadata call

        :returns: An object of zeep.objects.DescribeMetadataResult
        """
        return await self._service.describeMetadata(
            self._api_version, _soapheaders=[self._session_header]
        )

    async def list_metadata(self, queries: List[Any]) -> List[Any]:
        """
        Performs a listMetadata call

        :param queries: A list of zeep.objects.ListMetadataQuery that specify
        which components you are interested in.
                        Limit: 3
        :type queries: list
        :returns: List of zeep.objects.FileProperties objects
        :rtype: list
        """
        return await self._service.listMetadata(  # type: ignore[no-any-return]
            queries, self._api_version, _soapheaders=[self._session_header]
        )

    # pylint: disable=R0914
    # pylint: disable-msg=C0103
    async def deploy(
        self, zipfile: str | Path, sandbox: bool, **kwargs: Any
    ) -> Tuple[str | None, str | None]:
        """Kicks off async deployment, returns deployment id
        :param zipfile:
        :type zipfile:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        client = kwargs.get("client", "simple_salesforce_metahelper")
        checkOnly = kwargs.get("checkOnly", False)
        testLevel = kwargs.get("testLevel")
        tests = kwargs.get("tests")
        ignoreWarnings = kwargs.get("ignoreWarnings", False)
        allowMissingFiles = kwargs.get("allowMissingFiles", False)
        autoUpdatePackage = kwargs.get("autoUpdatePackage", False)
        performRetrieve = kwargs.get("performRetrieve", False)
        purgeOnDelete = kwargs.get("purgeOnDelete", False)
        rollbackOnError = kwargs.get("rollbackOnError", False)
        singlePackage = True

        attributes = {
            "client": client,
            "checkOnly": checkOnly,
            "sessionId": self._session_id,
            "ZipFile": await self._read_deploy_zip(zipfile),
            "testLevel": testLevel,
            "tests": tests,
            "ignoreWarnings": ignoreWarnings,
            "allowMissingFiles": allowMissingFiles,
            "autoUpdatePackage": autoUpdatePackage,
            "performRetrieve": performRetrieve,
            "purgeOnDelete": purgeOnDelete,
            "rollbackOnError": rollbackOnError,
            "singlePackage": singlePackage,
        }

        if not sandbox:
            attributes["allowMissingFiles"] = False
            attributes["rollbackOnError"] = True

        if testLevel:
            test_level = f"<met:testLevel>{testLevel}</met:testLevel>"
            attributes["testLevel"] = test_level

        tests_tag = ""
        if tests and str(testLevel).lower() == "runspecifiedtests":
            for test in tests:
                tests_tag += f"<met:runTests>{test}</met:runTests>\n"
            attributes["tests"] = tests_tag

        request = DEPLOY_MSG.format(**attributes)

        headers = {"Content-Type": "text/xml", "SOAPAction": "deploy"}
        result = await call_salesforce(
            url=self.metadata_url + "deployRequest",
            method="POST",
            session_factory=self.session_factory,
            headers=self.headers,
            additional_headers=headers,
            data=request,
        )

        root = ET.fromstring(result.text)

        async_process_id = find_element_text(
            root,
            "soapenv:Body/mt:deployResponse/mt:result/mt:id",
            self._XML_NAMESPACES,
        )

        state = find_element_text(
            root,
            "soapenv:Body/mt:deployResponse/mt:result/mt:state",
            self._XML_NAMESPACES,
        )

        return async_process_id, state

    @staticmethod
    # pylint: disable=R1732
    async def _read_deploy_zip(zipfile: str | Path) -> str:
        """
        :param zipfile:
        :type zipfile:
        :return:
        :rtype:
        """
        # Synchronous file-handle: WILL BLOCK
        async with aiofiles.open(zipfile, "rb") as fl:
            raw = await fl.read()

        return b64encode(raw).decode("utf-8")

    async def _retrieve_deploy_result(
        self, async_process_id: str, **kwargs: Any
    ) -> Element:
        """Retrieves status for specified deployment id
        :param async_process_id:
        :type async_process_id:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        client = kwargs.get("client", "simple_salesforce_metahelper")

        attributes = {
            "client": client,
            "sessionId": self._session_id,
            "asyncProcessId": async_process_id,
            "includeDetails": "true",
        }
        mt_request = CHECK_DEPLOY_STATUS_MSG.format(**attributes)
        headers = {"Content-type": "text/xml", "SOAPAction": "checkDeployStatus"}

        res = await call_salesforce(
            url=self.metadata_url + "deployRequest/" + async_process_id,
            method="POST",
            session_factory=self.session_factory,
            headers=self.headers,
            additional_headers=headers,
            data=mt_request,
        )

        root = ET.fromstring(res.text)
        result = root.find(
            "soapenv:Body/mt:checkDeployStatusResponse/mt:result", self._XML_NAMESPACES
        )
        if result is None:
            raise Exception(f"Result node could not be found: {res.text}")

        return result

    @staticmethod
    def get_component_error_count(value: str) -> int:
        """Get component error counts"""
        try:
            return int(value)
        except ValueError:
            return 0

    async def check_deploy_status(self, async_process_id: str, **kwargs: Any) -> Tuple[
        Optional[str],
        Optional[str],
        Optional[Mapping[str, Any]],
        Optional[Mapping[str, Any]],
    ]:
        """
        Checks whether deployment succeeded
        :param async_process_id:
        :type async_process_id:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        result = await self._retrieve_deploy_result(async_process_id, **kwargs)

        state = find_element_text(result, "mt:status", self._XML_NAMESPACES)
        state_detail = find_element_text(result, "mt:stateDetail", self._XML_NAMESPACES)

        component_errors = find_element_text(
            result, "mt:numberComponentErrors", self._XML_NAMESPACES, default="0"
        )
        failed_count = self.get_component_error_count(component_errors)

        # Remap keys to our friendly names
        deploy_fail_node_mapper = {
            "type": "mt:componentType",
            "file": "mt:fileName",
            "status": "mt:problemType",
            "message": "mt:problem",
        }
        unittest_fail_node_mapper = {
            "class": "mt:name",
            "method": "mt:methodName",
            "message": "mt:message",
            "stack_trace": "mt:stackTrace",
        }

        # Pull out errors
        unit_test_errors = []
        deployment_errors = []
        if state == "Failed" or failed_count > 0:
            # Deployment failures
            failures = result.findall(
                "mt:details/mt:componentFailures", self._XML_NAMESPACES
            )
            for failure in failures:
                deploy_error = {}
                for key, nodename in deploy_fail_node_mapper.items():
                    deploy_error[key] = find_element_text(
                        failure, nodename, self._XML_NAMESPACES
                    )
                deployment_errors.append(deploy_error)

            # Unit test failures
            failures = result.findall(
                "mt:details/mt:runTestResult/mt:failures", self._XML_NAMESPACES
            )
            for failure in failures:
                unit_test_error = {}
                for key, nodename in unittest_fail_node_mapper.items():
                    unit_test_error[key] = find_element_text(
                        failure, nodename, self._XML_NAMESPACES
                    )
                unit_test_errors.append(unit_test_error)

        # Pull out deployment info
        deploy_detail_mapper = {
            "total_count": "mt:numberComponentsTotal",
            "failed_count": "mt:numberComponentErrors",
            "deployed_count": "mt:numberComponentsDeployed",
        }
        deployment_detail = {
            key: find_element_text(result, nodename, self._XML_NAMESPACES)
            for key, nodename in deploy_detail_mapper.items()
        }
        deployment_detail["errors"] = deployment_errors

        unit_test_mapper = {
            "total_count": "mt:numberTestsTotal",
            "failed_count": "mt:numberTestErrors",
            "completed_count": "mt:numberTestsCompleted",
        }
        unit_test_detail = {
            key: find_element_text(result, nodename, self._XML_NAMESPACES)
            for key, nodename in unit_test_mapper.items()
        }
        unit_test_detail["errors"] = unit_test_errors

        return state, state_detail, deployment_detail, unit_test_detail

    async def download_unit_test_logs(self, async_process_id: str) -> None:
        """Downloads Apex logs for unit tests executed during specified
        deployment"""
        result = await self._retrieve_deploy_result(async_process_id)
        print("response: %s" % ET.tostring(result, encoding="us-ascii", method="xml"))

    async def retrieve(
        self, async_process_id: str, single_package: bool = True, **kwargs: Any
    ) -> Tuple[Optional[str], Optional[str]]:
        """Submits retrieve request"""
        # Compose unpackaged XML
        client = kwargs.get("client", "simple_salesforce_metahelper")

        unpackaged = ""
        if unpackaged_param := kwargs.get("unpackaged", {}):
            if isinstance(unpackaged_param, dict):
                for metadata_type in unpackaged_param:
                    unpackaged += "<types>"
                    members = unpackaged_param[metadata_type]
                    for member in members:
                        unpackaged += f"<members>{member}</members>"
                    unpackaged += f"<name>{metadata_type}</name></types>"
            else:
                raise TypeError("unpackaged metadata types must be a dict")

        # Compose retrieve request XML
        attributes = {
            "client": client,
            "sessionId": self._session_id,
            "apiVersion": self._api_version,
            "singlePackage": single_package,
            "unpackaged": unpackaged,
        }
        request = RETRIEVE_MSG.format(**attributes)
        # Submit request
        headers = {"Content-type": "text/xml", "SOAPAction": "retrieve"}

        res = await call_salesforce(
            url=self.metadata_url + "deployRequest/" + async_process_id,
            method="POST",
            session_factory=self.session_factory,
            headers=self.headers,
            additional_headers=headers,
            data=request,
        )
        root = ET.fromstring(res.text)
        # Parse response to get async Id and status
        async_process_id = find_element_text(
            root,
            "soapenv:Body/mt:retrieveResponse/mt:result/mt:id",
            self._XML_NAMESPACES,
        )
        state = find_element_text(
            root,
            "soapenv:Body/mt:retrieveResponse/mt:result/mt:state",
            self._XML_NAMESPACES,
        )

        return async_process_id, state

    async def retrieve_retrieve_result(
        self, async_process_id: str, include_zip: str, **kwargs: Any
    ) -> Element:
        """Retrieves status for specified retrieval id"""
        client = kwargs.get("client", "simple_salesforce_metahelper")
        attributes = {
            "client": client,
            "sessionId": self._session_id,
            "asyncProcessId": async_process_id,
            "includeZip": include_zip,
        }
        mt_request = CHECK_RETRIEVE_STATUS_MSG.format(**attributes)
        headers = {"Content-type": "text/xml", "SOAPAction": "checkRetrieveStatus"}
        res = await call_salesforce(
            url=self.metadata_url + "deployRequest/" + async_process_id,
            method="POST",
            session_factory=self.session_factory,
            headers=self.headers,
            additional_headers=headers,
            data=mt_request,
        )

        root = ET.fromstring(res.text)
        result = root.find(
            "soapenv:Body/mt:checkRetrieveStatusResponse/mt:result",
            self._XML_NAMESPACES,
        )
        if result is None:
            raise Exception("Result node could not be found: %s" % res.text)

        return result

    async def retrieve_zip(
        self, async_process_id: str, **kwargs: Any
    ) -> Tuple[Optional[str], Optional[str], List[Dict[str, Any]], bytes]:
        """Retrieves ZIP file"""
        result = await self.retrieve_retrieve_result(async_process_id, "true", **kwargs)
        state = find_element_text(result, "mt:status", self._XML_NAMESPACES)
        error_message = find_element_text(result, "mt:errorMessage", self._XML_NAMESPACES)

        # Check if there are any messages
        messages = []
        message_list = result.findall("mt:details/mt:messages", self._XML_NAMESPACES)
        for message in message_list:
            messages.append(
                {
                    "file": find_element_text(message, "mt:fileName", self._XML_NAMESPACES),
                    "message": find_element_text(message, "mt:problem", self._XML_NAMESPACES),
                }
            )

        # Retrieve base64 encoded ZIP file
        zipfile_base64 = find_element_text(result, "mt:zipFile", self._XML_NAMESPACES, default="")
        zipfile = b64decode(zipfile_base64)

        return state, error_message, messages, zipfile

    async def check_retrieve_status(
        self, async_process_id: str, **kwargs: Any
    ) -> Tuple[Optional[str], Optional[str], List[Dict[str, Optional[str]]]]:
        """Checks whether retrieval succeeded"""
        result = await self.retrieve_retrieve_result(
            async_process_id, "false", **kwargs
        )
        state = find_element_text(result, "mt:status", self._XML_NAMESPACES)
        error_message = find_element_text(result, "mt:errorMessage", self._XML_NAMESPACES)

        # Check if there are any messages
        messages = []
        message_list = result.findall("mt:details/mt:messages", self._XML_NAMESPACES)
        for message in message_list:
            messages.append(
                {
                    "file": find_element_text(message, "mt:fileName", self._XML_NAMESPACES),
                    "message": find_element_text(message, "mt:problem", self._XML_NAMESPACES),
                }
            )

        return state, error_message, messages


# # # # # Helpers # # # # #
# # # # # # # # # # # # # #
def find_element_text(
    element: Element | None, path: str, *args: Any, default: Any = None
) -> str | Any:
    """Returns the text of an element or `default`"""
    if element is None:
        return default

    node = element.find(path, *args)
    return node.text if node is not None else default
