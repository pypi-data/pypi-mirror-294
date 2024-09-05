import ast
import json
import os
import types
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin

import pandas as pd
from pydantic import BaseModel


class BonsaiBaseModel(BaseModel):

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        # Create a new type for names dynamically
        fields = list(cls.model_fields.keys())
        fields = fields + list(cls.model_computed_fields.keys())
        cls.names = type("Names", (), {field: field for field in fields})

    def to_pandas(self) -> pd.DataFrame:
        """
        Converts instances of BaseToolModel within BaseTableClass to a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing data from instances of BaseToolModel.
        """
        return pd.DataFrame.from_dict(self.model_dump(), orient="index").T

    @classmethod
    def to_dataclass(cls: Type["BaseModel"], input_data) -> "BonsaiTableModel":
        if isinstance(input_data, pd.DataFrame):
            data_instances = [cls(**row) for _, row in input_data.iterrows()]
        elif isinstance(input_data, dict):
            data_list = input_data.get("data", [])
            data_instances = [cls(**item) for item in data_list]
        elif isinstance(input_data, pd.MultiIndex):
            data_instances = [
                cls(**dict(zip(input_data.names, idx))) for idx in input_data
            ]
        else:
            raise ValueError(
                "Invalid input. Must be a pandas DataFrame or a JSON object."
            )
        return BonsaiTableModel(data=data_instances)

    @classmethod
    def get_csv_field_dtypes(cls: Type["BaseModel"]) -> Dict[str, Any]:
        """
        Return a dictionary with field names and their corresponding types.
        Since csv files can only contain str, float and int, all types that
        are not int and float will be changed to str
        """

        def convert_dtype(dtype_str):
            if dtype_str in ["str", "float", "int", "bool"]:
                return dtype_str
            else:
                return "str"

        type_dict = {}
        for field_name, field_info in cls.model_fields.items():
            field_type = field_info.annotation
            origin = get_origin(field_type)
            if origin is Union or isinstance(field_type, types.UnionType):
                # Check for Optional types (Union[X, None])
                args = get_args(field_type)
                if len(args) == 2 and type(None) in args:
                    # Get the non-None type
                    primary_type = next(arg for arg in args if arg is not type(None))
                    type_name = convert_dtype(primary_type.__name__)
                else:
                    # Otherwise, list all types
                    type_name = ", ".join(convert_dtype(arg.__name__) for arg in args)
            else:
                type_name = convert_dtype(field_type.__name__)
            type_dict[field_name] = type_name

        for field_name, field_info in cls.model_computed_fields.items():
            field_type = field_info.return_type
            type_dict[field_name] = field_type.__name__

        return type_dict

    @classmethod
    def get_empty_dataframe(cls: Type["BonsaiBaseModel"]):
        """
        Returns an empty pandas DataFrame with columns corresponding to the fields of the data class.

        Returns:
            pandas.DataFrame: An empty DataFrame with columns corresponding to the fields of the data class.
        """
        columns = list(cls.model_fields.keys())
        columns.extend(cls.model_computed_fields.keys())

        return pd.DataFrame(columns=columns)


class BonsaiTableModel(BaseModel):
    data: list[BonsaiBaseModel]
    # schema_name: str

    def to_json(self):
        """
        Convert the object to a JSON string representation.

        Returns:
            str: A JSON string representing the object with data information.
        """
        return json.dumps(
            {
                "data": [item.model_dump() for item in self.data],
            },
            indent=4,
        )

    def to_pandas(self) -> pd.DataFrame:
        """
        Converts instances of BaseToolModel within BaseTableClass to a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing data from instances of BaseToolModel.
        """
        # Ensure consistent order of columns
        data_dict = {key: [] for key in self.data[0].__dict__.keys()}

        for item in self.data:
            for key, value in item.dict().items():
                data_dict[key].append(value)

        return pd.DataFrame(data_dict)


def generate_prefixed_id(prefix, latest_id=None):
    if latest_id:
        counter = int(latest_id.split("_")[-1]) + 1
        generate_prefixed_id.counters[prefix] = counter
    else:
        generate_prefixed_id.counters[prefix] = (
            generate_prefixed_id.counters.get(prefix, 0) + 1
        )
        counter = generate_prefixed_id.counters[prefix]
    return f"{prefix}_{counter:010d}"


generate_prefixed_id.counters = {}  # Dictionary to store counters for each prefix


def get_dataclasses(directory: str = "src/dataio/schemas/bonsai_api") -> List[str]:
    """
    Retrieve a list of Pydantic dataclass names that inherit from BaseToolModel from Python files in the specified directory.

    Args:
        directory (str): The directory path where Python files containing Pydantic dataclasses are located.
            Defaults to "src/dataio/schemas/bonsai_api".

    Returns:
        List[str]: A list of fully qualified names (including module names) of Pydantic dataclasses that inherit from BaseToolModel.
    """
    dataclasses = []
    found_classes = set()

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                try:
                    tree = ast.parse(file.read(), filename=file_path)
                except SyntaxError:
                    print(f"Error parsing file: {file_path}")
                    continue

            # Find class definitions in the abstract syntax tree
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    # qualified_name = f"{filename[:-3]}.{class_name}"
                    qualified_name = f"{class_name}"
                    # Check if it's a Pydantic dataclass and inherits from BaseToolModel
                    if any(
                        isinstance(base, ast.Name)
                        and base.id == "BonsaiBaseModel"
                        or base.id in dataclasses
                        for base in node.bases
                    ):
                        if qualified_name not in dataclasses:
                            dataclasses.append(qualified_name)
                            found_classes.add(qualified_name)

    return dataclasses


def print_data_classes():
    """
    Print out all the available data classes in the directory src/dataio/schemas/bonsai_api
    """
    list_dataclasses = get_dataclasses()
    print(list_dataclasses)
    return
