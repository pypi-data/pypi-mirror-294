# BONSAI dataio

The BONSAI dataio Python package is a part of the [Getting The Data Right](https://bonsamurais.gitlab.io/bonsai/documentation) project.


The `dataio` package is designed to facilitate the management of data resources through easy-to-use APIs for reading, writing, and updating data in various formats, with a focus on maintaining comprehensive metadata about each data resource.

Read the [BONSAI data architecture](https://bonsamurais.gitlab.io/bonsai/documentation/architecture/data) for background information on table types, foreign keys, and related concepts.

## Installation

To install the dataio package as a standalone package type in the command line:

```bash
pip install git+ssh://git@gitlab.com/bonsamurais/bonsai/util/dataio@<version>
```

dataio uses HDF5 stores for storing matrices. You possibly need to install HDF5 systemwide before you can install dataio. On Mac you can do this by using brew `brew install hdf5`.

To install as dependency in a package add to the field `install_requires` in  `setup.cfg`:

```bash
util_dataio @ git+ssh://git@gitlab.com/bonsamurais/bonsai/util/dataio@<version>
```

You can find the list of versions [here](https://bonsamurais.gitlab.io/bonsai/util/dataio/changelog.html).

## Key Features

- Resource Management: Manage your data resources with a structured CSV repository that supports adding, updating, and listing data resources.
- Data Validation: Validate data against predefined schemas before it is saved to ensure integrity.
- Data Retrieval and Storage: Easily retrieve and store dataframes directly from/to specific tasks and data resources.

## Usage
### Setting Up the Environment

Before using the dataio package, set the BONSAI_HOME environment variable to point to your project's home directory where data resources will be managed:

```python
import os
from pathlib import Path

os.environ["BONSAI_HOME"] = str(Path("path/to/your/data").absolute())
```

If you don't want to set this variable, you need to provide an absolut path when setting up your resource file and then make sure that in that resource file all locations are also absolut.

The execption to this is when you interact with the data through the online API, in this case you also don't need to set the env.

NOTE THAT THIS IS NOT SUPPORTED YET.

### Creating a Resource Repository

Instantiate a CSV resource repository to manage your data resources:

```python
from dataio.resources import CSVResourceRepository

repo = CSVResourceRepository(Path("path/to/your/data"))
```

Currently we only support CSVResourceRespository. In the future you will also be able to use the APIResourceRepository class.

### Adding a New Resource

Add new resources to the repository:

```python
from dataio.schemas.bonsai_api import DataResource
from datetime import date

resource = DataResource(
    name="new_resource",
    schema_name="Schema",
    location="relative/or/absolut/path/to/the/resource.csv",
    task_name="task1",
    stage="collect",
    data_flow_direction="input",
    data_version="1.0.1",
    code_version="2.0.3",
    comment="Initial test comment",
    last_update=date.today(),
    created_by="Test Person",
    dag_run_id="12345",
)

repo.add_to_resource_list(resource)
```

Not all fields need to be set. The schema name needs to correspond to one of the schema names defined in dataio.schemas

For the CSVResourceRepository, the relative locations provided via the resources.csv file are relative to that resources.csv file!

### Updating an Existing Resource

Update an existing resource in your repository:

```python
resource.created_by = "New Name"
repo.update_resource_list(resource)
```

### Retrieving Resource Information

Retrieve specific resource information using filters:

```python
result = repo.get_resource_info(name="new_resource")
print(result)
```
### Writing and Reading Data
You can store and read data using different file formats. The way data is stored depends on the file extension used in the `location` field. The `location` field also is always relative to the resources.csv file. Please don't put absolute paths there. 

The `last_update` field is set automatically by dataio. Please don't overwrite this field.

Currently the following data formats are supported:
#### for dictionaries
[".json", ".yaml"]

#### for tabular data
[".parquet", ".xlsx", ".xls", ".csv", ".pkl"]

#### for matrices
[".hdf5", ".h5"]
Note matrices need to use a `MatrixModel` schema.



Write data to a resource and then read it back to verify:

```python
import pandas as pd

data_to_add = pd.DataFrame({
    "flow_code": ["FC100"],
    "description": ["Emission from transportation"],
    "unit_reference": ["unit"],
    "region_code": ["US"],
    "value": [123.45],
    "unit_emission": ["tonnes CO2eq"],
})

repo.write_dataframe_for_task(
    resource_name="new_resource",
    data=data_to_add,
    task_name="footprint_calculation",
    stage="calculation",
    location="calculation/footprints/{version}/footprints.csv",
    schema_name="Footprint",
    data_flow_direction="output",
    data_version="1.0",
    code_version="1.1",
    comment="Newly added data for emissions",
    created_by="Test Person",
    dag_run_id="run200",
)
# Read the data back
retrieved_data = repo.get_dataframe_for_task("new_resource")
print(retrieved_data)

```

## Testing

To ensure everything is working as expected, run the provided test suite:

```bash
pytest tests -vv
```
or 

```bash
tox
```
This will run through a series of automated tests, verifying the functionality of adding, updating, and retrieving data resources, as well as reading and writing data based on resource descriptions.

## Contributions

Contributions to the dataio package are welcome. Please ensure to follow the coding standards and write tests for new features. Submit pull requests to our repository for review.