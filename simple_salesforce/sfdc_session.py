import re

from requests import Session
from xml.etree import ElementTree as ET


class SfdcSession(Session):
    _DEFAULT_API_VERSION = "43.0"
    _LOGIN_URL = "https://{instance}.salesforce.com"
    _SOAP_API_BASE_URI = "/services/Soap/c/{version}"
    _XML_NAMESPACES = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'mt': 'http://soap.sforce.com/2006/04/metadata',
        'd': 'urn:enterprise.soap.sforce.com'
    }

    _LOGIN_TMPL = \
        """<env:Envelope xmlns:xsd='http://www.w3.org/2001/XMLSchema'
xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
xmlns:env='http://schemas.xmlsoap.org/soap/envelope/'>
    <env:Body>
        <sf:login xmlns:sf='urn:enterprise.soap.sforce.com'>
            <sf:username>{username}</sf:username>
            <sf:password>{password}</sf:password>
        </sf:login>
    </env:Body>
</env:Envelope>"""

    def __init__(
            self, username=None, password=None, token=None,
            is_sandbox=False, api_version=_DEFAULT_API_VERSION,
            **kwargs):
        print("ℹ️ ss.sfdc_session.INIT ----------------------")
        print(username)
        print(password)
        print(token)
        print(is_sandbox)
        print(api_version)
        print(kwargs.get("session_id", None))
        print(kwargs.get("instance", None))
        super(SfdcSession, self).__init__()
        self._username = username
        self._password = password
        self._token = token
        self._is_sandbox = is_sandbox
        self._api_version = api_version
        self._session_id = kwargs.get("session_id", None)
        self._instance = kwargs.get("instance", None)

    # def login(self):
    #     print("ℹ️ ss.sfdc_session.login")
    #     print("ARE WE HERE")
    #     print(self.get_soap_api_uri())
    #     url = self.construct_url(self.get_soap_api_uri())
    #     headers = {'Content-Type': 'text/xml', 'SOAPAction': 'login'}
    #     password = self._password
    #     if self._token:
    #         password += self._token
    #     print("WHAT ARE WE DOING")
    #     print("ℹ️ url: ", url)
    #     print("ℹ️ headers: ", headers)
    #     print("ℹ️ password: ", password)
    #     data = SfdcSession._LOGIN_TMPL.format(**{'username': self._username, 'password': password})
    #     print("ℹ️ data: ", data)
    #     print("posting")
    #     r = self.post(url, headers=headers, data=data)
    #     print("ℹ️ result: ", r)
    #     root = ET.fromstring(r.text)
    #     if root.find('soapenv:Body/soapenv:Fault', SfdcSession._XML_NAMESPACES):
    #         raise Exception("Could not log in. Code: %s Message: %s" % (
    #             root.find('soapenv:Body/soapenv:Fault/faultcode', SfdcSession._XML_NAMESPACES).text,
    #             root.find('soapenv:Body/soapenv:Fault/faultstring', SfdcSession._XML_NAMESPACES).text))
    #     self._session_id = root.find('soapenv:Body/d:loginResponse/d:result/d:sessionId',
    #                                  SfdcSession._XML_NAMESPACES).text
    #     server_url = root.find('soapenv:Body/d:loginResponse/d:result/d:serverUrl', SfdcSession._XML_NAMESPACES).text
    #     self._instance = re.search("""https://(.*).salesforce.com/.*""", server_url).group(1)

    def get_server_url(self):
        print("ℹ️ ss.sfdc_session.get_server_url")
        if not self._instance:
            url = SfdcSession._LOGIN_URL.format(**{'instance': 'test' if self._is_sandbox else 'login'})
        url = SfdcSession._LOGIN_URL.format(**{'instance': self._instance})
        if re.search(r'cloudforce', url):
            url = re.sub(r'\.salesforce\.com$', '', url)
        print("URL: ", url)
        return url

    def get_soap_api_uri(self):
        print("ℹ️ ss.sfdc_session.get_soap_api_uri")
        return SfdcSession._SOAP_API_BASE_URI.format(**{'version': self._api_version})

    def construct_url(self, uri):
        print("ℹ️ ss.sfdc_session.construct_url")
        print("%s%s" % (self.get_server_url(), uri))
        return "%s%s" % (self.get_server_url(), uri)

    def get_api_version(self):
        print("ℹ️ ss.sfdc_session.get_api_version")
        print(self._api_version)
        return self._api_version

    def get_session_id(self):
        print("ℹ️ ss.sfdc_session.get_session_id")
        print(self._session_id)
        return self._session_id

    def is_connected(self):
        print("ℹ️ ss.sfdc_session.is_connected")
        return True if self._instance else False
