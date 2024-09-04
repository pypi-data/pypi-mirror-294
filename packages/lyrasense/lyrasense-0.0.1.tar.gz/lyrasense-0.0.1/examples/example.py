from lyrasense import Lyrasense

# Initialize Lyrasense with your API base URL and key
Lyrasense.init(
    "http://35.214.166.85",
    "w9eFPBG9D0K6mFLel_CgSTeYGDr8cyoSDwPhnJeblckb__jy1dD7LbHZCWnR",
    debug=True,
)

# Use the environment configuration if needed
Lyrasense.env(baseImage="python:3.9")


@Lyrasense.function
def additionlowercase(a, b):
    return a + b


if __name__ == "__main__":
    # Use the function locally
    result_local = additionlowercase.local(5, 3)
    print(f"Local result: {result_local}")

    # Use the function remotely
    result_remote = additionlowercase.remote(5, 3)
    print(f"Remote result: {result_remote}")
