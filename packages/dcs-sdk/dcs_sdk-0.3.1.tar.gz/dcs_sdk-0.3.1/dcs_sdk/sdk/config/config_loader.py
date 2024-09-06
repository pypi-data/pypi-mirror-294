#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import uuid
from typing import List, Optional, Union

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel


class InvalidUUIDError(ValueError):
    pass


class MissingRequiredFieldError(ValueError):
    pass


class InvalidConnectionTypeError(ValueError):
    pass


class SourceTargetConnection(BaseModel):
    id: str
    name: str
    workspace: Optional[str] = "default"
    host: Optional[str] = None
    port: Optional[Union[int, str]] = None
    driver: str
    table: Optional[str] = None
    database: Optional[str] = None
    filepath: Optional[str] = None
    catalog: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse: Optional[str] = None
    role: Optional[str] = None
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    http_path: Optional[str] = None
    access_token: Optional[str] = None


class Comparison(BaseModel):
    comparison_name: str
    source: SourceTargetConnection
    target: SourceTargetConnection
    source_columns: List[str]
    target_columns: List[str]
    primary_keys_source: List[str]
    primary_keys_target: List[str]


class EnvYamlLoader(yaml.SafeLoader):
    """YAML Loader with `!ENV` constructor."""

    def __init__(self, stream):
        super(EnvYamlLoader, self).__init__(stream)
        self.add_constructor("!ENV", self.env_constructor)

    @classmethod
    def env_constructor(cls, loader, node):
        value = loader.construct_scalar(node)
        env_var = value.strip("${} ")
        return os.environ.get(env_var, "")


class DataDiffConfig:
    DRIVER_MAP = {
        "file": "duckdb",
        "duckdb": "duckdb",
        "postgres": "postgres",
        "postgresql": "postgres",
        "snowflake": "snowflake",
        "trino": "trino",
        "databricks": "databricks",
    }

    def __init__(
        self,
        yaml_file_path: Optional[str] = None,
        yaml_string: Optional[str] = None,
        config_json: Optional[dict] = None,
    ):
        load_dotenv()
        if yaml_file_path:
            self.data = self.read_yaml_file(yaml_file_path)
        elif yaml_string:
            self.data = self.read_yaml_string(yaml_string)
        elif config_json:
            self.data = config_json
        else:
            raise ValueError("No configuration provided")

    @staticmethod
    def read_yaml_file(file_path: str) -> dict:
        with open(file_path, "r") as file:
            return yaml.load(file, Loader=EnvYamlLoader)

    @staticmethod
    def read_yaml_string(yaml_string: str) -> dict:
        return yaml.load(yaml_string, Loader=EnvYamlLoader)

    @staticmethod
    def is_valid_uuid(val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def validate_uuid(self, uuid_str: str, field_name: str) -> None:
        if not self.is_valid_uuid(uuid_str):
            raise InvalidUUIDError(f"{field_name} is not a valid UUID")

    @staticmethod
    def validate_required_field(value: Union[str, None], field_name: str, source_name: str) -> None:
        if value is None:
            raise MissingRequiredFieldError(f"{field_name} is required for datasource {source_name}")

    @staticmethod
    def validate_file_connection(connection: dict) -> None:
        if connection.get("type") == "file" and connection.get("filepath") is None:
            raise MissingRequiredFieldError("file path is required for file connection")

    @staticmethod
    def validate_databricks_connection(connection: dict) -> None:
        if connection.get("type") == "databricks":
            if connection.get("connection", {}).get("http_path") is None:
                raise MissingRequiredFieldError("http_path is required for databricks connection")
            if connection.get("connection", {}).get("access_token") is None:
                raise MissingRequiredFieldError("access_token is required for databricks connection")

    def get_driver(self, connection: dict) -> str:
        connection_type = connection.get("type")
        if connection_type not in self.DRIVER_MAP:
            raise InvalidConnectionTypeError(f"Invalid connection type: {connection_type}")
        return self.DRIVER_MAP[connection_type]

    def create_connection_config(self, connection: dict, comparison_data: dict, is_source: bool) -> dict:
        self.validate_uuid(connection.get("id"), "Datasource id")
        self.validate_required_field(connection.get("name"), "connection name", source_name=connection.get("name"))
        self.validate_required_field(connection.get("type"), "connection type", source_name=connection.get("name"))
        self.validate_file_connection(connection)
        self.validate_databricks_connection(connection)

        driver = self.get_driver(connection)

        return {
            "id": connection.get("id"),
            "name": connection.get("name"),
            "workspace": connection.get("workspace", "default"),
            "host": connection.get("connection", {}).get("host"),
            "port": connection.get("connection", {}).get("port", None),
            "account": connection.get("connection", {}).get("account"),
            "warehouse": connection.get("connection", {}).get("warehouse"),
            "role": connection.get("connection", {}).get("role"),
            "driver": driver,
            "table": comparison_data.get("source" if is_source else "target", {}).get("table"),
            "database": connection.get("connection", {}).get("database"),
            "catalog": connection.get("connection", {}).get("catalog"),
            "schema_name": connection.get("connection", {}).get("schema"),
            "username": connection.get("connection", {}).get("username"),
            "password": connection.get("connection", {}).get("password"),
            "http_path": connection.get("connection", {}).get("http_path"),
            "access_token": connection.get("connection", {}).get("access_token"),
            "filepath": connection.get("filepath"),
        }

    def get_data_diff_configs(self) -> List[Comparison]:
        data_sources = {
            ds["name"]: {
                "name": ds.get("name"),
                "id": ds.get("id"),
                "type": ds.get("type"),
                "workspace": ds.get("workspace", "default"),
                "connection": ds.get("connection", {}),
                "filepath": ds.get("file_path"),
            }
            for ds in self.data["data_sources"]
        }
        new_structure = []

        for comparison_name, comparison_data in self.data["comparisons"].items():
            source_connection = data_sources[comparison_data["source"]["data_source"]]
            target_connection = data_sources[comparison_data["target"]["data_source"]]

            source_to_target = {
                item["source_column"]: item["target_column"] for item in comparison_data.get("columns_mappings", {})
            }

            source_columns = comparison_data.get("columns", [])
            target_columns = [source_to_target.get(col, col) for col in source_columns]

            assert len(source_columns) == len(
                target_columns
            ), "source_columns and target_columns must have the same length"

            primary_keys_source = comparison_data.get("key_columns", [])
            if not primary_keys_source:
                raise MissingRequiredFieldError("key_columns are required for comparison")
            primary_keys_target = [source_to_target.get(pk, pk) for pk in primary_keys_source]

            new_comparison = {
                "comparison_name": comparison_name,
                "source": self.create_connection_config(source_connection, comparison_data, True),
                "target": self.create_connection_config(target_connection, comparison_data, False),
                "source_columns": source_columns,
                "target_columns": target_columns,
                "primary_keys_source": primary_keys_source,
                "primary_keys_target": primary_keys_target,
            }
            new_structure.append(Comparison(**new_comparison))

        return new_structure


def data_diff_config_loader(
    config_path: Optional[str] = None,
    config_yaml: Optional[str] = None,
    config_json: Optional[dict] = None,
) -> List[Comparison]:
    config = DataDiffConfig(yaml_file_path=config_path, yaml_string=config_yaml, config_json=config_json)
    return config.get_data_diff_configs()
