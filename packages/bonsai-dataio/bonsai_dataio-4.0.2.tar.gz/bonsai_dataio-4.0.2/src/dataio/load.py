"""Datapackage load module of dataio utility."""

import warnings
from logging import getLogger
from pathlib import Path
from typing import Dict

import h5py
import pandas as pd
import yaml
from pandas._libs.parsers import STR_NA_VALUES
from pydantic import BaseModel

import dataio.schemas.bonsai_api as schemas
from dataio.save import (
    SUPPORTED_DICT_FILE_EXTENSIONS,
    SUPPORTED_MATRIX_FILE_EXTENSIONS,
    SUPPORTED_TABLE_FILE_EXTENSIONS,
)
from dataio.schemas.bonsai_api.base_models import MatrixModel
from dataio.tools import BonsaiBaseModel
from dataio.validate import validate_matrix, validate_table

from .set_logger import set_logger

logger = getLogger("root")

accepted_na_values = STR_NA_VALUES - {"NA"}


def load_metadata(path_to_metadata, datapackage_names=None):
    """
    Load metadata from a YAML file and convert it into a dictionary with UUIDs as keys and MetaData objects as values.
    The YAML file is expected to start directly with a list of metadata entries.

    Parameters
    ----------
    file_path : str
        The path to the YAML file that contains metadata entries.

    Returns
    -------
    dict
        A dictionary where each key is a UUID (as a string) of a MetaData object and each value is the corresponding MetaData object.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    yaml.YAMLError
        If there is an error in parsing the YAML file.
    pydantic.ValidationError
        If an item in the YAML file does not conform to the MetaData model.

    Examples
    --------
    Assuming a YAML file located at 'example.yaml':

    >>> metadata_dict = load_metadata_from_yaml('example.yaml')
    >>> print(metadata_dict['123e4567-e89b-12d3-a456-426614174000'])
    MetaData(id=UUID('123e4567-e89b-12d3-a456-426614174000'), created_by=User(...), ...)
    """
    logger.info(f"Started loading metadata from {path_to_metadata}")

    if datapackage_names:
        # TODO load from API
        pass
    else:
        metadata = load_dict_file(path_to_metadata, schemas.MetaData)
        logger.info("Finished loading metadata")
    return metadata


def load_dict_file(path_to_file, schema: BaseModel):
    result_dict = {}
    try:
        with open(path_to_file, "r") as file:
            data = yaml.safe_load(file)

        for item in data:
            result_obj = schema(**item)
            result_dict[str(result_obj.id)] = result_obj

    except FileNotFoundError:
        logger.error(
            "Could not open dataio datapackage metadata file " f"{path_to_file}."
        )
        raise

    return result_dict


def load_table_file(path_to_file: Path, schema: BonsaiBaseModel, **kwargs):
    str_path = str(path_to_file)
    if str_path.endswith(".pkl"):
        df = pd.read_pickle(path_to_file, **kwargs)
    elif str_path.endswith(".csv"):
        df = pd.read_csv(
            path_to_file, dtype=schema.get_csv_field_dtypes(), **kwargs
        )
        for col_name, type in schema.get_csv_field_dtypes().items():
            if col_name in df.columns and type == "str":
                df[col_name] = df[col_name].fillna("")
    elif ".xls" in str_path:
        df = pd.read_excel(path_to_file, **kwargs)
    elif str_path.endswith(".parquet"):
        df = pd.read_parquet(path_to_file, **kwargs)
    else:
        raise ValueError(f"Failed to import {str_path}")

    validate_table(df, schema)

    return df


def load_matrix_file(path_to_file: Path, schema: MatrixModel, **kwargs):
    df = pd.read_hdf(path_to_file, **kwargs)
    validate_matrix(df, schema)

    return df


def load(path: Path, schemas: Dict[str, BaseModel] = None):

    loaded_files = {}

    if not schemas:
        return load_old_datapackage(path)

    if path.name.startswith("http"):
        # if path is a url, connect to the API url and load the package names
        # defined in the keys of the schemas dict
        df = self._read_http(*args, **kwargs)

    elif path.exists():
        if path.is_dir():
            # If path is a directory, read all files in the directory
            for file in path.iterdir():
                # If path is a file, just load the file
                if file.suffix in SUPPORTED_DICT_FILE_EXTENSIONS:
                    loaded_files[file.stem] = load_dict_file(file, schemas[file.stem])
                # If path is a file, just load the file
                elif file.suffix in SUPPORTED_TABLE_FILE_EXTENSIONS:
                    loaded_files[file.stem] = load_table_file(file, schemas[file.stem])
                elif path.suffix in SUPPORTED_MATRIX_FILE_EXTENSIONS:
                    loaded_files[path.stem] = load_matrix_file(path, schemas[path.stem])

        else:
            # If path is a file, just load the file
            if path.suffix in SUPPORTED_DICT_FILE_EXTENSIONS:
                loaded_files[path.stem] = load_dict_file(path, schemas[path.stem])
            # If path is a file, just load the file
            elif path.suffix in SUPPORTED_TABLE_FILE_EXTENSIONS:
                loaded_files[path.stem] = load_table_file(path, schemas[path.stem])
            elif path.suffix in SUPPORTED_MATRIX_FILE_EXTENSIONS:
                loaded_files[path.stem] = load_matrix_file(path, schemas[path.stem])

    if len(loaded_files) == 1:
        return next(iter(loaded_files.values()))
    return loaded_files


def load_old_tables(root_path: str, metadata: dict):
    """Load tables given dataio metadata file.

    Tables are expected to be csv tabular files with an id field.

    Metadata is expected to have fields (for 0 <= k < number of tables):
    - ['path']
    - ['tables'][k]['path']
    - ['tables'][k]['name']

    Parameters
    ----------
    path : str
      path to dataio.yaml file
    path : str
      path to dataio.yaml file

    Returns
    -------
    dataio.Datapackage
    """
    logger.info("Started loading tables")

    if not isinstance(metadata, dict):
        logger.error(
            "Argument 'metadata' is of type " f"{type(metadata)} and not 'dict'"
        )
        raise TypeError
    for key in ["path"]:
        if key not in metadata.keys():
            logger.error(f"Key '{key}' missing from 'metadata' keys.")
            raise KeyError

    try:
        base_path = Path(root_path).joinpath(metadata["path"])
    except FileNotFoundError:
        logger.error(
            "Could not combine root path and datapackage path. "
            f"Their types are {type(root_path)} and "
            f"{type(metadata['path'])}"
        )

    tables = {}
    for pos, table in enumerate(metadata["tables"]):
        # delimiter and quotechar options
        delimiter = ","
        quotechar = '"'
        if "dialect" in table.keys():
            if "csv" in table["dialect"].keys():
                if "delimiter" in table["dialect"]["csv"].keys():
                    delimiter = table["dialect"]["csv"]["delimiter"]
                if "quoteChar" in table["dialect"]["csv"].keys():
                    quotechar = table["dialect"]["csv"]["quoteChar"]
                if "skipInitialSpace" in table["dialect"]["csv"].keys():
                    if table["dialect"]["csv"]["skipInitialSpace"]:
                        logger.warning(
                            f"Initial space skip in {pos} table. "
                            "Might not load if there are delimiters "
                            "inside quotation characters"
                        )
        # primary key as index
        index_col = None
        if "schema" in table.keys():
            if "primaryKeys" in table["schema"].keys():
                index_col = table["schema"]["primaryKeys"][0]

        for key in ["name", "path"]:
            if key not in table.keys():
                logger.error(f"Key '{key}' missing from keys of {pos} table.")
                raise KeyError
        logger.info(f"Started loading table {table['name']}")
        tables[table["name"]] = pd.read_csv(
            base_path.joinpath(table["path"]),
            index_col=index_col,
            delimiter=delimiter,
            quotechar=quotechar,
            keep_default_na=False,
            na_values=accepted_na_values,
        )
        logger.info(f"Finished loading table {table['name']}")

    logger.info("Finished loading tables")
    return tables


def load_old_datapackage(
    full_path: str,
    include_tables: bool = True,
    overwrite: bool = False,
    log_name: str = None,
):
    """Load dataio datapackage.

    Parameters
    ----------
    full_path : str
      <full_path> = <root_path>/<path>/<name>.dataio.yaml
    include_tables : bool
      Whether only metadata or full datapackage is loaded
    overwrite : bool
      whether to overwrite log file (if any)
    log_name : str
      name of log file, if None no log is set

    Returns
    -------
    dataio.Datapackage
    """

    warnings.warn(
        "Using old dataio datapackage, this will soon stop working. Please upgrade to the new dataio schemas",
        DeprecationWarning,
    )
    logger.info("Started loading datapackage")

    # open log file
    if log_name is not None:
        set_logger(
            filename=log_name, path=str(Path(full_path).parent), overwrite=overwrite
        )
        logger.info("Started dataio plot log file")
    else:
        logger.info("Not initialized new log file")

    metadata = load_old_metadata(full_path=full_path)

    if "path" not in metadata.keys():
        logger.error("'metadata' field 'path' missing from metadata")
        raise KeyError
    if not isinstance(metadata["path"], str):
        logger.error("'metadata' field 'path' type is not 'str'")
        raise ValueError

    if metadata["path"] == ".":
        root_path = str(Path(full_path).parent)
    else:
        root_path = str(Path(full_path).parent)[: -len(metadata["path"])]
    logger.info(f"root_path is '{root_path}'")

    if include_tables:
        tables = load_old_tables(root_path, metadata)
    else:
        logger.info("Tables not included")
        tables = {}

    dp = create(metadata, tables)

    logger.info("Finished loading datapackage")
    return dp


def load_old_metadata(full_path: str):
    """Load datapackage metadata from dataio config file.

    Parameters
    ----------
    path : str
      path to dataio.yaml file

    Returns
    -------
    dict
    """
    logger.info(f"Started loading metadata from {full_path}")
    try:
        with open(full_path, "r") as f:
            metadata = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("Could not open dataio datapackage metadata file " f"{full_path}.")
        raise
    logger.info("Finished loading metadata")
    return metadata
