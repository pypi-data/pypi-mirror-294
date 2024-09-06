from lyrasense import Lyrasense

# Initialize Lyrasense with your API base URL and key
Lyrasense.init(
    "http://35.214.166.85",
    "w9eFPBG9D0K6mFLel_CgSTeYGDr8cyoSDwPhnJeblckb__jy1dD7LbHZCWnR",
    debug=True,
)

# Use the environment configuration if needed
Lyrasense.env(
    base_image="python:3.11-slim-bookworm",
    python_packages=[
        'xarray',
        'pandas'
    ]
)
