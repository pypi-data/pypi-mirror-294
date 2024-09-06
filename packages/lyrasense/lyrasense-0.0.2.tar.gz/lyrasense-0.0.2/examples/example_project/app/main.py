import lyrasense_config
from calculations.example import addition_lowercase, function_with_derps

if __name__ == "__main__":
    # Use the function locally
    result_local = addition_lowercase.local(5, 3)
    print(f"Local result: {result_local}")

    result_local_2 = addition_lowercase(5, 3)
    print(f"Local result: {result_local_2}")

    # Use the function remotely
    result_remote = addition_lowercase.remote(5, 3)
    print(f"Remote result: {result_remote}")

    result_local_2 = function_with_derps()
    print(f"Local result: {result_local_2}")

    result_local_3 = function_with_derps.local()
    print(f"Local result: {result_local_3}")

    result_remote_2 = function_with_derps.remote()
    print(f"Remote result: {result_remote_2}")
