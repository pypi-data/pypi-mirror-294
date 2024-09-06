# Lyrasense Platform - Python SDK

This library is a Python SDK that can be used to interface with the Lyrasense Earth Observation(EO) platform.

## Example Usage

First install the library in your environment:

```bash
pip install lyrasense
```

Then you need to login on the Lyrasense platform and create an API key.
To get access to the platform contact us at: <info@lyrasense.com>

<image>

Then you can the lyrasense decorators to wrap functions that you want to be deployed in the Lyrasense platform and execute them on demand.

```python
from lyrasense import Lyrasense

# Initialize Lyrasense with your API base URL and key
Lyrasense.init(
    "http://<base url>",
    "<your api key>>",
)

# Use the environment configuration if needed
Lyrasense.env(
    baseImage="python:3.9"
)

@Lyrasense.function
def addition(a, b):
    return a + b


if __name__ == "__main__":
    # If you call the wrapped function normally, it will be executed locally
    result_local_def = addition(5, 3)
    print(f"Local result: {result_local_def}")

    # You can also explicitly call the wrapped function locally by using .local()
    result_local = addition.local(5, 3)
    print(f"Local result: {result_local}")

    # You can execute the wrapped function remotely by using .remote()
    # This will first deploy the function and then call it
    result_remote = additionlowercase.remote(5, 3)
    print(f"Remote result: {result_remote}")

```

**Notes:**
- The initial function deployment needs some time to create the function, any further function calls should be fast.
- If the function code changes the updated function with the new code will be re-deployed.
