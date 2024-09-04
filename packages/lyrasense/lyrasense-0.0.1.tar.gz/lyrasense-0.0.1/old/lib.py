import sqlite3
import hashlib
import base64
import requests
import time
import random
import inspect
import re
from functools import wraps
## TODO: Figure out if we can simply install the nuclio SDK without the jupyter baggage to avoid unused dependencies
import nuclio

class LyrasenseCache:
    def __init__(self, db_path='lyrasense_cache.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS function_cache (
            function_name TEXT PRIMARY KEY,
            function_hash TEXT,
            deployed_url TEXT
        )
        ''')
        self.conn.commit()

    def get_function_hash(self, func):
        func_code = inspect.getsource(func)
        return base64.b64encode(hashlib.sha256(func_code.encode()).digest()).decode()

    def get_deployed_url(self, func_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT deployed_url FROM function_cache WHERE function_name = ?', (func_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def update_cache(self, func_name, func_hash, deployed_url):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO function_cache (function_name, function_hash, deployed_url)
        VALUES (?, ?, ?)
        ''', (func_name, func_hash, deployed_url))
        self.conn.commit()

    def is_deployment_needed(self, func):
        func_name = func.__name__
        new_hash = self.get_function_hash(func)
        cursor = self.conn.cursor()
        cursor.execute('SELECT function_hash FROM function_cache WHERE function_name = ?', (func_name,))
        result = cursor.fetchone()
        return result is None or result[0] != new_hash

def retry_on_exception(max_retries=10, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise  # Re-raise the last exception if all retries failed
                    print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= backoff
                    # Add some jitter to avoid thundering herd problem
                    retry_delay += random.uniform(0, 1)
        return wrapper
    return decorator

@retry_on_exception(max_retries=3, delay=2, backoff=2, exceptions=(Exception,))
def deploy_function_with_retry(data):
    print('[deploy_function] The config is: {}'.format(Lyrasense.config))
    print('[deploy_function] The data is: {}'.format(data))
    print("[deploy_function] This deploys the function!")

    userfunction_def=Lyrasense.function_extraction(data['func_source'])
    userfunction_name=data['func_name']

    indented_function = '\n'.join('    ' + line for line in userfunction_def.split('\n'))


    function_template = f'''
def handler(context, event):
    body = event.body
    context.logger.info('[lyrasense][{userfunction_name}] Executing function with args: ' + str(body['args']))

    ## USER DEFINED CODE - START ##
{indented_function}

    result = {userfunction_name}(*body['args'])
    ## USER DEFINED CODE - END ##

    return context.Response(body={{ "function": "{userfunction_name}", "result": result }},
                            headers={{}},
                            content_type='application/json',
                            status_code=200)
'''

    print(function_template)
        
    spec = nuclio.ConfigSpec(
        config= {
            'spec.build.baseImage': 'python:3.9',
        },
        cmd=['pip install msgpack']
    )

    addr = nuclio.deploy_code(
        function_template,
        name='projectName-{}'.format(userfunction_name),
        project='lyrasense',
        verbose=True,
        spec=spec
    )

    print(f"Deploying function: {data['func_name']}")
    print(addr)

    if Lyrasense.ENV == 'LOCAL':
        pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)$'

        # Replace IP with localhost, keeping the port
        addr = re.sub(pattern, r'localhost:\2', addr[0])
    return addr


"""
TODO:
a) Security: Serializing and deserializing functions can be a security risk if not handled properly. Ensure that you have proper authentication and authorization mechanisms in place.
b) Error Handling: Add more robust error handling for network issues, API errors, etc.
c) Asynchronous Execution: Consider implementing an asynchronous approach for long-running tasks.
"""
class LyrasenseFunction:
    cache = LyrasenseCache()

    def __init__(self, func):
        self.func = func
        self.deployed_url = None

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def deploy(self):
        if self.cache.is_deployment_needed(self.func):
            print(f"Deploying function: {self.func.__name__}")
            
            func_source = inspect.getsource(self.func)
            data = {
                "func_source": func_source,
                "func_name": self.func.__name__,
            }

            self.deployed_url = 'http://' + str(Lyrasense.deploy_function(data))
            func_hash = self.cache.get_function_hash(self.func)
            self.cache.update_cache(self.func.__name__, func_hash, self.deployed_url)
        else:
            print(f"Function {self.func.__name__} is up to date, no deployment needed")
            self.deployed_url = self.cache.get_deployed_url(self.func.__name__)
        return self.deployed_url

    def local(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def remote(self, *args, **kwargs):
        if not self.deployed_url:
            #raise ValueError("Function hasn't been deployed yet. Call .deploy() first.")
            self.deploy()

        data = {
            "args": args,
            "kwargs": kwargs
        }
        
        response = requests.post(self.deployed_url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Remote execution failed: {response.text}")

class Lyrasense:
    # Config
    ## TODO: Add logic to switch environments
    ENV = 'LOCAL'
    config = { 'env': 'Python', 'baseImage': 'None' }

    def env(baseImage='python'):
        print('[env] Defines an environment, that you can use to attach functions on it')
        print('[env] The config is: {}'.format(Lyrasense.config))
        Lyrasense.config['baseImage'] = baseImage

    @staticmethod
    def function_extraction(function_code):
        # The updated regex pattern
        pattern = r'(def\s+.*?$)(?:\n(\s+).*?)*$'

        # Find the match
        match = re.search(pattern, function_code, re.MULTILINE | re.DOTALL)

        if match:
            # Extract the function definition
            function_lines = match.group(0).split('\n')
            
            # Get the indentation of the first line after the function definition
            if len(function_lines) > 1:
                indentation = re.match(r'\s*', function_lines[1]).group(0)
            else:
                indentation = ''
            
            # Join the lines, preserving indentation
            extracted_function = '\n'.join([function_lines[0]] + [line if line.startswith(indentation) else indentation + line for line in function_lines[1:]])
            
            print("Extracted function:")
            print(extracted_function)
            return extracted_function
        else:
            raise Exception('Something went wrong with the function extraction!')            


    @staticmethod
    def function_code(func):
        return LyrasenseFunction(func)

    @staticmethod
    def deploy_function(data):
        try:
            return deploy_function_with_retry(data)
        except Exception as e:
            print(f"Deployment failed after multiple attempts: {str(e)}")
            # Here you can add any additional error handling or user notification
            raise
