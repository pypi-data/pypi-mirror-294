import requests
import time
import inspect
import re
import logging

logger = logging.getLogger(__name__)


class LyrasenseFunction:
    def __init__(self, func=None, imports=None):
        self.func = func
        self.function_id = None
        self.deployed_url = None
        self.imports = imports or []

    def __call__(self, *args, **kwargs):
        if self.func is None:
            # This is the decorator being called without parentheses
            return lambda f: self.__class__(f, self.imports)
        # This is either the decorator being called with parentheses,
        # or the wrapped function being called
        return self.func(*args, **kwargs)

    def _function_extraction(self, function_code):
        # The updated regex pattern
        pattern = r"(def\s+.*?$)(?:\n(\s+).*?)*$"

        # Find the match
        match = re.search(pattern, function_code, re.MULTILINE | re.DOTALL)

        if match:
            # Extract the function definition
            function_lines = match.group(0).split("\n")

            # Get the indentation of the first line after the function definition
            if len(function_lines) > 1:
                indentation = re.match(r"\s*", function_lines[1]).group(0)
            else:
                indentation = ""

            # Join the lines, preserving indentation
            extracted_function = "\n".join(
                [function_lines[0]]
                + [
                    line if line.startswith(indentation) else indentation + line
                    for line in function_lines[1:]
                ]
            )

            logger.debug("Extracted function:\n%s", extracted_function)
            return extracted_function
        else:
            raise Exception("Something went wrong with the function extraction!")

    def deploy(self):
        func_source = self._function_extraction(inspect.getsource(self.func))

        logger.debug("In deploy, func source:\n%s", func_source)
        data = {
            "name": self.func.__name__,
            "code": func_source,
            "runtime_config": {
                "python_packages": Lyrasense.python_packages,
                "base_image": Lyrasense.base_image
            },
            "imports": self.imports
        }

        logger.debug("In deploy calling PUT /api/v1/functions/")
        response = requests.put(
            f"{Lyrasense.api_base_url}/api/v1/functions/",
            json=data,
            headers={"api-key": Lyrasense.api_key},
        )
        response.raise_for_status()

        function_data = response.json()

        logger.debug("In deploy PUT response: %s", function_data)
        self.function_id = function_data["id"]

        # Poll until the function is deployed or deployment fails
        while True:
            # TODO: FIX: LRS-84
            time.sleep(5)

            logger.debug("In deploy, started polling, calling GET")
            status = self.get_function_status()

            logger.debug("Poll response: %s", status)
            if status == "deployed":
                self.deployed_url = function_data["deployed_url"]
                logger.info("Function %s deployed successfully.", self.func.__name__)
                break
            elif status == "deployment_failed":
                raise DeploymentFailedException(
                    f"Deployment failed for function {self.func.__name__}"
                )

        return self.deployed_url

    def get_function_status(self):
        response = requests.get(
            f"{Lyrasense.api_base_url}/api/v1/functions/{self.function_id}",
            headers={"api-key": Lyrasense.api_key},
        )
        response.raise_for_status()

        return response.json()["status"]

    def local(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def remote(self, *args, **kwargs):
        if not self.function_id:
            logger.debug("In remote method - no function id, calling deploy")
            self.deploy()

        logger.debug("In remote method - function id present, calling execute")
        data = {"args": args or kwargs}

        response = requests.post(
            f"{Lyrasense.api_base_url}/api/v1/functions/{self.function_id}/execute",
            json=data,
            headers={"api-key": Lyrasense.api_key},
        )
        response.raise_for_status()
        return response.json()["result"]


class Lyrasense:
    api_base_url = None
    api_key = None
    base_image = "python:3.11-slim-bookworm"
    python_packages=[]
    debug = False

    @staticmethod
    def init(api_base_url, api_key, debug=False):
        Lyrasense.api_base_url = api_base_url
        Lyrasense.api_key = api_key
        Lyrasense.debug = debug

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

        logger.info("Lyrasense initialized with API base URL: %s", api_base_url)
        if debug:
            logger.debug("Debug mode is ON")

    @staticmethod
    def function(func=None, imports=None):
        if not Lyrasense.api_base_url or not Lyrasense.api_key:
            raise ValueError(
                "Lyrasense has not been initialized. Call Lyrasense.init() first."
            )
        if callable(func):
            # Used as @Lyrasense.function without parentheses
            return LyrasenseFunction(func, imports)
        else:
            # Used as @Lyrasense.function() or @Lyrasense.function(imports=[...])
            return lambda f: LyrasenseFunction(f, imports)


    @staticmethod
    def env(base_image="python:3.11-slim-bookworm", python_packages=[]):
        Lyrasense.base_image = base_image
        Lyrasense.python_packages = python_packages



class DeploymentFailedException(Exception):
    pass
