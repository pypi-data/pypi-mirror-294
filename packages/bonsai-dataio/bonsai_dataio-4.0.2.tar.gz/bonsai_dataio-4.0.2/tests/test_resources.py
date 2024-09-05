import os
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import re

import dataio.schemas.bonsai_api as schemas
from dataio.resources import CSVResourceRepository


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["BONSAI_HOME"] = str(Path("tests").absolute())


@pytest.fixture
def setup_empty_csv_repository(tmp_path):
    # Setup a temporary directory with a test CSV file
    test_db_path = tmp_path / "test_resources"
    test_db_path.mkdir()

    assert test_db_path.absolute()

    repo = CSVResourceRepository(db_path=str(test_db_path))
    return repo


@pytest.fixture
def test_resources():
    return CSVResourceRepository(Path("data"))


def test_automatic_location():

    # test with set location
    expected_location = str(
        Path("tests").absolute() / "clean" / "task1" / "1.0" / "data.csv"
    )
    resource1 = schemas.DataResource(
        name="data",
        task_name="task1",
        stage="clean",
        location="{stage}/{task_name}/{version}/{resource_name}.csv",
        schema_name=schemas.Footprint,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )
    assert expected_location == resource1.location

    # test without set location
    resource2 = schemas.DataResource(
        name="data",
        task_name="task1",
        stage="clean",
        schema_name=schemas.Footprint,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
    )
    assert expected_location == resource2.location


def test_get_latest_version_non_semantic(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    old_version = schemas.DataResource(
        name="test_resource",
        schema_name="TestSchema",
        location="path/to/resource_v1",
        task_name="test_task",
        stage="test_stage",
        data_flow_direction="input",
        data_version="2012b1",
        code_version="1.0.0",
        comment="test comment v1",
        last_update=datetime.now(),
        created_by="tester",
        license="MIT",
        license_url="http://example.com/license",
        dag_run_id="test_dag_run_id_v1",
    )
    new_version = schemas.DataResource(
        name="test_resource",
        schema_name="TestSchema",
        location="path/to/resource_v2",
        task_name="test_task",
        stage="test_stage",
        data_flow_direction="input",
        data_version="2014b3",
        code_version="1.0.0",
        comment="test comment v2",
        last_update=datetime.now(),
        created_by="tester",
        license="MIT",
        license_url="http://example.com/license",
        dag_run_id="test_dag_run_id_v2",
    )
    # Add sample resources to the repository
    repo.add_to_resource_list(old_version)
    repo.add_to_resource_list(new_version)

    # Get the latest version of the resource
    latest_resource = repo.get_latest_version(
        name="test_resource", task_name="test_task"
    )

    # Check that the latest version is returned
    assert latest_resource.data_version == "2014b3"


def test_get_latest_version(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    old_version = schemas.DataResource(
        name="test_resource",
        schema_name="TestSchema",
        location="path/to/resource_v1",
        task_name="test_task",
        stage="test_stage",
        data_flow_direction="input",
        data_version="1.0.0",
        code_version="1.0.0",
        comment="test comment v1",
        last_update=datetime.now(),
        created_by="tester",
        license="MIT",
        license_url="http://example.com/license",
        dag_run_id="test_dag_run_id_v1",
    )
    new_version = schemas.DataResource(
        name="test_resource",
        schema_name="TestSchema",
        location="path/to/resource_v2",
        task_name="test_task",
        stage="test_stage",
        data_flow_direction="input",
        data_version="2.0.0",
        code_version="1.0.0",
        comment="test comment v2",
        last_update=datetime.now(),
        created_by="tester",
        license="MIT",
        license_url="http://example.com/license",
        dag_run_id="test_dag_run_id_v2",
    )
    # Add sample resources to the repository
    repo.add_to_resource_list(old_version)
    repo.add_to_resource_list(new_version)

    # Get the latest version of the resource
    latest_resource = repo.get_latest_version(
        name="test_resource", task_name="test_task"
    )

    # Check that the latest version is returned
    assert latest_resource.data_version == "2.0.0"


def test_overwrite_and_update_resource(setup_empty_csv_repository):
    # write data should update a field if overwrite=True
    repo = setup_empty_csv_repository

    df = pd.DataFrame()
    repo.write_dataframe_for_task(
        data=df,
        resource_name="resource_name",
        location="test/file.csv",
        data_version="1.2",
        comment="No comment",
        schema_name="Supply",
    )

    assert repo.get_resource_info(name="resource_name").comment == "No comment"

    with pytest.raises(FileExistsError):
        repo.write_dataframe_for_task(
            data=df,
            resource_name="resource_name",
            data_version="1.2",
            comment="No new comment",
            license="CC BY 4.0",
            overwrite=False,
        )
    assert repo.get_resource_info(name="resource_name").comment == "No comment"

    repo.write_dataframe_for_task(
        data=df,
        resource_name="resource_name",
        data_version="1.2",
        comment="I actually do have a comment",
        license="CC BY 4.0",
        overwrite=True,
    )

    assert len(repo.available_resources) == 1
    assert (
        repo.get_resource_info(name="resource_name").comment
        == "I actually do have a comment"
    )


def test_resource_exists(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    sample_resource = schemas.DataResource(
        name="test_exist",
        schema_name="TestSchema",
        location="path/to/resource",
        task_name="test_task",
        stage="test_stage",
        data_flow_direction="input",
        data_version="1.0.0",
        code_version="1.0.0",
        comment="test comment",
        last_update=date.today(),
        created_by="tester",
        dag_run_id="test_dag_run_id",
    )
    # Initially, the resource should not exist
    assert not repo.resource_exists(sample_resource)

    # Add the resource to the repository
    repo.add_to_resource_list(sample_resource)

    # Now, the resource should exist
    assert repo.resource_exists(sample_resource)


def test_add_to_resource_list(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    resource = schemas.DataResource(
        name="test_resource",
        schema_name="schema1",
        location=str(repo.db_path),
        task_name="task1",
        stage="raw",
        data_flow_direction="input",
        data_version="v1.0",
        code_version="c1.0",
        comment="Initial test comment",
        last_update=date.today(),
        created_by="tester",
        dag_run_id="12345",
    )
    repo.add_to_resource_list(resource)
    assert not repo.available_resources.empty
    assert repo.available_resources.iloc[-1]["name"] == "test_resource"


def test_update_resource_list(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    # Add a resource first
    resource = schemas.DataResource(
        name="test_resource",
        schema_name="schema1",
        location=str(repo.db_path),
        task_name="task1",
        stage="raw",
        data_flow_direction="input",
        data_version="v1.0",
        code_version="c1.0",
        comment="Initial test comment",
        last_update=date.today(),
        created_by="tester",
        dag_run_id="12345",
    )
    repo.add_to_resource_list(resource)
    # Update the same resource
    updated_comment = "Updated comment"
    resource.comment = updated_comment
    repo.update_resource_list(resource)
    assert (
        repo.available_resources.loc[
            repo.available_resources["name"] == "test_resource", "comment"
        ].iloc[0]
        == updated_comment
    )


def test_get_resource_info_with_filters(setup_empty_csv_repository):
    repo = setup_empty_csv_repository
    # Add some resources
    resource1 = schemas.DataResource(
        name="resource1",
        schema_name="schema1",
        location=str(repo.db_path),
        task_name="task1",
        stage="raw",
        data_flow_direction="input",
        data_version="v1.0",
        code_version="c1.0",
        comment="First resource",
        last_update=date.today(),
        created_by="tester",
        dag_run_id="12345",
    )
    resource2 = schemas.DataResource(
        name="resource2",
        schema_name="schema2",
        location=str(repo.db_path),
        task_name="task2",
        stage="processed",
        data_flow_direction="output",
        data_version="v2.0",
        code_version="c2.0",
        comment="Second resource",
        last_update=date.today(),
        created_by="tester",
        dag_run_id="12346",
    )
    repo.add_to_resource_list(resource1)
    repo.add_to_resource_list(resource2)
    # Test get with filters
    result = repo.get_resource_info(name="resource2")
    assert result.name == "resource2"


def test_list_available_resources(test_resources):
    repo = test_resources

    resources = repo.list_available_resources()
    assert isinstance(resources, list)
    assert len(resources) == 10

    # test if specific resource is loaded correctly
    result = repo.get_resource_info(name="SampleRegion", data_version="1.5")

    assert result.name == "SampleRegion"
    assert result.schema_name == "Location"
    assert result.location == str(
        Path("tests").absolute() / "data" / "SampleRegion.csv"
    )
    assert result.task_name == "test"
    assert result.data_version == "1.5"
    assert result.code_version == "1.0.5"
    assert result.comment == "Only essential fields"
    assert result.created_by == "janedoe"
    assert result.last_update == datetime(2024, 1, 1, 0, 1, 30, tzinfo=timezone.utc)


def test_filter_multiple_resources(test_resources):
    repo = test_resources

    # test if specific resource is loaded correctly
    result = repo.get_resource_info(name="SampleRegion")

    assert len(result) == 2
    assert result[0].name == "SampleRegion"


def test_read_data_for_task(test_resources):
    repo = test_resources
    result = repo.get_dataframe_for_task("SampleRegion", data_version="1.5")

    # Sample data conforming to the specified schema
    expected_data = {
        "position": [0, 1, 2, 3],
        "code": ["AT", "DE", "UK", "DK"],
        "prefixed_id": ["ID001", "ID002", "ID003", "ID004"],
        "parent_id": ["PID001", "PID001", "PID002", "PID003"],
        "level": ["0", "1", "1", "2"],
        "name": ["Alpha", "Beta", "Gamma", "Delta"],
        "description": ["First entry", "Second entry", "Last entry", "Fourth entry"],
    }
    expected_result = pd.DataFrame(expected_data)
    expected_result["position"] = expected_result["position"].astype(int)

    pd.testing.assert_frame_equal(result, expected_result)


def test_write_csv_data(setup_empty_csv_repository):
    # this test defines a pandas dataframe that is then stored as csv file
    # using the resources.write_data method
    # This then results in an updated resources table
    repo = setup_empty_csv_repository

    # Define a DataFrame to write, adhering to the Footprint schema
    data_to_add = pd.DataFrame(
        {
            "flow_code": ["FC100"],
            "description": ["Emission from transportation"],
            "unit_reference": ["per vehicle"],
            "region_code": ["US"],
            "value": [123.45],
            "unit_emission": ["tonnes CO2eq"],
        }
    )

    name = "new_resource"
    last_updated = datetime(2024, 1, 1, 0, 5, 30, tzinfo=timezone.utc)

    # Writing the DataFrame to CSV using the repository method
    repo.write_dataframe_for_task(
        resource_name=name,
        data=data_to_add,
        task_name="new_task",
        stage="processed",
        location=f"data/{name}.csv",
        schema_name="Footprint",
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        last_update=last_updated,
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )

    # Verification step to ensure the data has been added
    assert repo.get_resource_info(name=name).name == name
    assert repo.get_resource_info(name=name).last_update == last_updated
    # Read the data back from the resource to verify it matches the original DataFrame
    retrieved_data = repo.get_dataframe_for_task(name=name)

    assert (retrieved_data.columns == data_to_add.columns).all()

    # Compare the original DataFrame with the retrieved one
    pd.testing.assert_frame_equal(
        data_to_add, retrieved_data.reset_index(drop=True), check_dtype=False
    )


def test_write_load_matrix_data(setup_empty_csv_repository):
    repo = setup_empty_csv_repository

    # Define the MultiIndex for columns
    columns_tuples = [
        ("New York", "Sales", "kg", 2023),
        ("New York", "Sales", "kg", 2024),
        ("Los Angeles", "Sales", "kg", 2023),
        ("Los Angeles", "Sales", "kg", 2024),
    ]

    columns = pd.MultiIndex.from_tuples(
        columns_tuples, names=["location", "activity", "unit", "time"]
    )

    # Define the MultiIndex for rows
    index_tuples = [
        ("New York", "Apples", "kg", 2023),
        ("New York", "Oranges", "kg", 2023),
        ("Los Angeles", "Apples", "kg", 2023),
        ("Los Angeles", "Oranges", "kg", 2023),
        ("New York", "Apples", "kg", 2024),
        ("New York", "Oranges", "kg", 2024),
        ("Los Angeles", "Apples", "kg", 2024),
        ("Los Angeles", "Oranges", "kg", 2024),
    ]

    row_index = pd.MultiIndex.from_tuples(
        index_tuples, names=["location", "product", "unit", "time"]
    )

    # Create the DataFrame with random data
    data = np.random.rand(len(index_tuples), len(columns))

    df = pd.DataFrame(data, index=row_index, columns=columns)

    # Save the DataFrame
    name = "new_resource"
    # Writing the DataFrame to CSV using the repository method
    repo.write_dataframe_for_task(
        resource_name=name,
        data=df,
        task_name="new_task",
        stage="processed",
        location=f"data/{name}.h5",
        schema_name=schemas.A_Matrix,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )

    # Verification step to ensure the data has been added
    assert repo.get_resource_info(name=name).name == name
    # Read the data back from the resource to verify it matches the original DataFrame
    retrieved_data = repo.get_dataframe_for_task(name=name)

    assert (retrieved_data.columns == df.columns).all()

    # Compare the original DataFrame with the retrieved one
    pd.testing.assert_frame_equal(df, retrieved_data)


def test_location_written_correctly_to_csv(setup_empty_csv_repository):

    repo = setup_empty_csv_repository

    # test with set location
    expected_location_in_csv = str(
        Path("clean") / "{task_name}" / "{version}" / "{resource_name}.csv"
    )
    expected_last_update = "2024-07-01 17:55:13-07:00"

    resource = schemas.DataResource(
        name="data",
        task_name="task1",
        stage="clean",
        location="clean/{task_name}/{version}/{resource_name}.csv",
        schema_name=schemas.Footprint,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        last_update=datetime.fromisoformat("2024-07-01T17:55:13-07:00"),
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )

    repo.add_or_update_resource_list(resource)

    all_resources = pd.read_csv(repo.resources_list_path)

    location_in_csv = all_resources[schemas.DataResource.names.location]
    last_update_in_csv = all_resources[schemas.DataResource.names.last_update]

    assert location_in_csv[0] == expected_location_in_csv
    assert last_update_in_csv[0] == expected_last_update

def test_last_update_written_correctly_to_csv(setup_empty_csv_repository):

    repo = setup_empty_csv_repository

    resource = schemas.DataResource(
        name="data",
        task_name="task1",
        stage="clean",
        location="clean/{task_name}/{version}/{resource_name}.csv",
        schema_name=schemas.Footprint,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )

    repo.add_or_update_resource_list(resource)

    all_resources = pd.read_csv(repo.resources_list_path)

    last_update_in_csv = all_resources[schemas.DataResource.names.last_update]

    matching = re.compile("\d+-\d+-\d+ \d+:\d+:\d+\.\d+\w?")
    assert matching.match(last_update_in_csv[0]) is not None


def test_version_change_reflected():

    expected_location = str(
        Path("tests").absolute() / "clean" / "task1" / "1.0" / "data.csv"
    )
    resource = schemas.DataResource(
        name="data",
        task_name="task1",
        stage="clean",
        location="{stage}/{task_name}/{version}/{resource_name}.csv",
        schema_name=schemas.Footprint,
        data_flow_direction="output",
        data_version="1.0",
        code_version="1.1",
        comment="Newly added data for emissions",
        created_by="developer",
        dag_run_id="run200",
    )
    assert expected_location == resource.location

    resource.data_version = "1.7"

    new_expected_location = str(
        Path("tests").absolute() / "clean" / "task1" / "1.7" / "data.csv"
    )
    assert new_expected_location == resource.location
