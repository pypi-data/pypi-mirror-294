# Bladed Results API 2.0 (Beta)

The Bladed Results API is an easy, fast, and robust way to access Bladed results using Python.

It provides features for:

- Discovering Bladed runs
- Finding variables in a set of runs
- Getting data from variables
- Reporting run and variable metadata
- Exploring and writing output groups.

The API depends on the [`numpy`](https://numpy.org) package.

> Currently only Windows is supported.

> Bladed Results API 2.0 replaces Results API 1.x which is being discontinued.

## Pre-requisites

- Requires a _32- or 64-bit Windows_ installation of:
  - Python 3.9
  - or Python 3.10
  - or Python 3.11
  - or Python 3.12

> 64-bit Python is recommended.

- The Results API has been tested on Windows 10.

### Quick Start

```shell
pip install dnv-bladed-results
```

```python
from dnv_bladed_results import *

run = ResultsApi.get_run(run_dir, run_name)
var_1d = run.get_variable_1d(variable_name)
print(var_1d.get_data())
```

## Usage Examples

Usage examples demonstrating core functionality are distributed with the package in the `UsageExamples` folder.  A brief description of each example follows.

The `UsageExamples` installation folder and list of available examples may be enquired as follows:
```python
import os
from dnv_bladed_results import UsageExamples
print(UsageExamples.__path__[0])
os.listdir(UsageExamples.__path__[0])
```

### Basic Operations

Load a Bladed run, request groups and variables, and get data for tower members and blade stations:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_BasicOperations
```

### Variable Data

Load a Bladed run, request 1D and 2D variables* from both the run and from a specific output group, and obtain data from the returned variables:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ReadBasic
```

Obtain data from a 2D variable* for specific independent variable values, and specify the precision of the data to read:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ReadExtended
```

  > *1D and 2D variables are dependent variables with one and two independent variables respectively.

### Runs

Use filters and regular expressions to find a subset of runs in a directory tree:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_FindRuns
```

Find and process runs asynchronously using a Python generator:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_FindRunsUsingGenerator
```

### Metadata

Get metadata for runs, groups, and variables:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_RunMetadata
```
```python
from dnv_bladed_results.UsageExamples import ResultsApi_GroupMetadata
```
```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableMetadata
```
```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableStats
```

### Output

Export 1D and 2D Bladed output groups, as well as an entire run, using the HDF5 file format:

  > Requires the `h5py` library, which is installed with the Results API.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ExportHDF5
```

Export Bladed output groups using the Matlab file format:

  > Requires the `scipy` library, which is installed with the Results API.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ExportMatlab
```

Write 1D and 2D output groups using the Bladed file format:
```python
from dnv_bladed_results.UsageExamples import ResultsApi_WriteGroup
```

### Charting

Create 2D and 3D plots of blade loads:

  > Requires the `matplotlib` library, which is installed with the Results API.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_Charting2D
```
```python
from dnv_bladed_results.UsageExamples import ResultsApi_Charting3D
```

## Data types

The API comprises a generated Python wrapper dispatching to a C++ DLL.  The DLL performs the work of fetching and storing data, validation, and memory management.

### One- and two-dimensional variable return types

The API has separate functions for getting 1D and 2D variables* primarily due to differences in the shape of the data and hence differences in the functions required to operate on the data.

  > *1D and 2D variables are dependent variables with one and two independent variables respectively. 

### Implicit typing of variable data

It is not necessary for the user to specify (or even know) the underlying type of the data (float or double) in the request, despite the C++ layer being statically typed.  By default, the return type always reflects the actual (serialised) type of the data:
```python
# Type of data reflects the serialised data (usually single-precision float)
data = run.get_variable_1d("Name").get_data()
```

The return type may be overridden globally as follows:
```python
ResultsApi_CacheSettings.set_data_type_for_reading(DATA_TYPE_SPECIFIER_READ_AS_FLOAT64)

# Type of data is double-precision float
data = run.get_variable_1d("Name").get_data()
```

### NumPy support

All arrays returned or accepted by API functions are of type NumPy `ndarray`. These functions wrap the underlying data without copying*.

The API provides counterpart functions returning C-style native array denoted with the suffix `_native_array`. These functions slightly improve performance by avoiding the (generally small) cost of wrapping a native array as NumPy.

> For most purposes, the functions returning NumPy array should be preferred as they offer several useful functions and improved memory safety.

  *Functions returning a two-dimensional NumPy array, for example the 2D variable function `get_data_for_all_independent_variable_values`, perform a deep copy of the underlying data. In performance-sensitive code, the counterpart function returning native array should be preferred.

## Known limitations

### Type hints in Visual Studio Code

It is necessary to use a type hint for VS Code Intellisense (also known as autocomplete) to work with wrapped class types inside a loop.  This issue does not affect PyCharm.

In the example below, in order for the member list of the run loop variable to display correctly, a type hint is required:
```python
# Get some Bladed runs
runs = ResultsApi.get_runs(r".\RunsFolder", SEARCH_SCOPE_RECURSIVE_SEARCH)

# Note the following type hint declared on the run loop variable
run: Run
for run in runs:
    # Do something with run - easy now Intellisense works!
```

### Variable-length argument lists

Functions with variable-length argument lists take a single `*args` parameter:
```python
def get_variable_1d(self, *args) -> Variable1D_Float32 | Variable1D_Float64 | Variable1D_Int32:
```

All valid argument permutations are described in the docstring.

In a future release `*args` will be replaced with explicit argument lists that include type hints, to improve readability.

## Glossary

#### Run

The output from running a Bladed calculation. Typically, this comprises several output _groups_, with each group containing variables that relate to a specific part of the model.

#### Variable

In the context of the Results API, the term _variable_ is synonymous with _dependent variable_.

#### Dependent variable

A variable calculated as the result of changing one or more independent variables. Dependent variables are listed next to the `VARIAB` key of an output group header file.

 Dependent variables may be one-dimensional (1D) or two-dimensional (2D).

- The value of a one-dimensional variable is determined by one independent variable, known as the _primary_ independent variable.

  Example: in a time series turbine simulation, 1D variable `Rotor speed` depends on primary independent variable `Time`. The data for `Rotor speed` is a one-dimensional array indexed on time.

- The value of a two-dimensional variable is determined by two independent variables, known as _primary_ and _secondary_ independent variables.

  Example: In a time series turbine simulation with a multi-member tower, 2D variable `Tower Mx` depends on primary independent variable `Time`, and secondary independent variable `Location`. The data for `Tower Mx` is a two-dimensional array indexed on member location and time.

#### Independent variable

A variable whose value does not depend on other variables in the calculation. Independent variables are denoted by the `AXISLAB` key of an output group header file.

In a time series calculation, a _primary_ independent variable typically represents time. A _secondary_ independent variable typically represents an measurement point, such as a blade station.

#### Header file

A file containing metadata describing an output group. A header files extension takes the form `.%n`, where `n` is a number uniquely identifying the group within the run.

#### Data file

A file containing an output group’s data (binary or ASCII). A data file extension takes the form `.$n`, where `n` matches the corresponding header file number.

#### (Output) group

A collection of variables that relate to a specific part of the model. For example, the variables `Rotor speed` and `Generator speed` belong to the `Drive train variables` group.

A Bladed group is represented by two files: a header file containing metadata, and a data file containing data for all dependent variables in the group.
