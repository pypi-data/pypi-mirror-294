import xarray as xr
import numpy as np
from lyrasense import Lyrasense

@Lyrasense.function(imports=[
    'import xarray as xr',
    'import numpy as np'
])
def function_with_derps():
    data = xr.DataArray(np.random.randn(2, 3), dims=("x", "y"), coords={"x": [10, 20]})
    return f'Result is {data}'


@Lyrasense.function
def addition_lowercase(a, b):
    return a + b
