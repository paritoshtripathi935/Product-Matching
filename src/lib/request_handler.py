import time
import requests
import tls_client
import traceback
import random
import sys
sys.path.append("src")


class RequestHandler:
    """
    A class that handles HTTP requests with proxy rotation and retry mechanism.

    Args:
        max_retries (int)           : The maximum number of retries for a failed request. Default is 3.
        proxies (list, optional)    : A list of proxies. Default is None.
        clients (list, mandatory)   : A list of client identifiers. Default is None.

    Attributes:
        max_retries (int)           : The maximum number of retries for a failed request.
        clients (list)              : A list of client identifiers.
        proxies_list (list)         : A list of proxies.
        status_code_count (dict)    : A dictionary to keep track of the count of different status codes.

    Methods:
        get_random_clients          : Returns a random client identifier from the list.
        get_proxy                   : Returns a list of proxies.
        handle_request              : Handles the HTTP request with proxy rotation and retry mechanism.

    Inherited Classes:
        GeneralUtils                : A class that handles general utilities.
        
    Examples:
    
        >>> from utils.request_handler import RequestHandler
        >>> request_handler = RequestHandler()
        
    """

    def __init__(self, max_retries=5):
        super().__init__()
        self.max_retries = max_retries
        self.tls_client = ['android11','android12','android13','android14','chrome111','chrome112','chrome113','chrome114']
        self.status_code_count = {}
        self.status_code_count["total_number_of_requests"] = 0
        self.status_code_count["total_number_of_success"] = 0
        self.status_code_count["total_number_of_failed"] = 0
        self.status_code_count["total_number_of_exceptions"] = 0
        self.successful_status_codes = [200, 201]
        self.failed_status_codes = [401, 403, 404, 409, 429, 400]
        self.redirect_status_codes = [301, 302, 303, 307, 308]
        self.server_down_status_codes = [500, 502, 503, 504]
        self.session_cookies = None
        
    def get_random_clients(self):
        return random.choice(self.tls_client)

    def handle_request(
        self,
        url,
        method,
        headers=None,
        data=None,
        params=None,
        json=None,
        requestType="tls",
        country_code="sg",
        proxies=None,
    ):
        """
        Handles the HTTP request with proxy rotation and retry mechanism.

        Args:
            url (str)                   : The URL of the request.
            method (str)                : The HTTP method of the request.
            headers (dict, optional)    : The headers of the request. Default is None.
            data (dict, optional)       : The data of the request. Default is None.
            params (dict, optional)     : The query parameters of the request. Default is None.
            json (dict, optional)       : The JSON data of the request. Default is None.
            requestType (str, optional) : The type of request. Default is "tls".
            country_code (str, optional): The country code for proxy selection. Default is "at".

        Returns:
            requests.Response or None   : The response object if the request is successful, None otherwise.

        """
        retries = 0

        while retries < self.max_retries:
            retries += 1
                
            self.status_code_count["total_number_of_requests"] += 1

            session = tls_client.Session(
                client_identifier=self.get_random_clients(),
                random_tls_extension_order=True,
            )
            
            try:
                if requestType == "tls":
                    if params:
                        url += f"&{params}" if "?" in url else f"?{params}" 
                    response = session.execute_request(
                        method=method,
                        url=url,   
                        headers=headers,
                        data=data,
                        json=json,
                        proxy=proxies,
                        cookies=self.session_cookies,
                    )

                else:
                    response = requests.request(
                        method=method,
                        url=url, # type: ignore
                        headers=headers,
                        data=data,
                        json=json,
                        proxies=proxies,
                        params=params,
                        cookies=self.session_cookies,
                    )
                    
                self.session_cookies = response.cookies
                self.handling_logging(f"Request: {url} {response.status_code}")
                self.status_code_count[response.status_code] = (
                    self.status_code_count.get(response.status_code, 0) + 1
                )

                if response.status_code in self.successful_status_codes:
                    self.status_code_count["total_number_of_success"] += 1

                    self.handling_logging(
                        f"""
                        [SUCCESS] [{response.status_code}] 
                        Request successful {url} {response.status_code}
                        Max retries: {self.max_retries} 
                        Retries: {retries}
                        Headers: {headers}
                        Payload: {data}
                        """
                    )

                    return response

                elif response.status_code in self.failed_status_codes:
                    self.handling_logging(
                        f"""
                        [BLOCKED] [{response.status_code}] 
                        Request blocked {url} {response.status_code} {response.text} 
                        Max retries: {self.max_retries} 
                        Retries: {retries}
                        Proxy: {proxies}
                        Headers: {headers}
                        """,
                        "warning",
                    )
                
                elif response.status_code in self.redirect_status_codes:
                    url = response.headers.get("location", None)
                    if url:           
                        self.handling_logging(
                            f"""
                            [REDIRECT] [{response.status_code}]
                            Redirecting to {url}
                            Max retries: {self.max_retries}
                            Retries: {retries}
                            """,
                            "warning",
                        )
                    else:
                        self.handling_logging(
                            f"""
                            [ERROR] [{response.status_code}]
                            No redirect url found
                            Max retries: {self.max_retries}
                            Retries: {retries}
                            """,
                            "error",
                        )
                        return response
                
                elif response.status_code in self.server_down_status_codes:
                    self.handling_logging(
                        f"""
                        [SERVER DOWN] [{response.status_code}] 
                        Server down {url} {response.status_code} {response.text} 
                        Max retries: {self.max_retries} 
                        Retries: {retries}
                        """,
                        "warning",
                    )
                    time.sleep(10)
                    self.max_retries = 10

                else:
                    self.handling_logging(
                        f"""
                        [ERROR] [{response.status_code}] 
                        Request failed {url} {response.status_code} {response.text} 
                        Max retries: {self.max_retries} 
                        Retries: {retries}
                        """,
                        "error",
                    )

            except Exception as e:
                self.handling_logging(
                    f"""
                    [EXCEPTION]
                    {traceback.format_exc()}
                    {e}
                    """,
                    "error",
                )
                self.status_code_count["total_number_of_exceptions"] += 1
            

        self.handling_logging(f"""
            [FAILED]
            url: {url}
            Max retries: {self.max_retries}
            Retries: {retries}
            """, "error")
        
        self.status_code_count["total_number_of_failed"] += 1
        return None


