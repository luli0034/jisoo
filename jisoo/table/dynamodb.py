from typing import Dict, Optional, Any, Union
from dataclasses import dataclass
from jisoo.table.base import Table
from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.exceptions import GetError, TableDoesNotExist, PynamoDBConnectionError
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class TableConfig:
    """
    Configuration for DynamoDB table access

    Attributes:
        table_name: Name of the DynamoDB table
        region_name: AWS region where the table is located
        hash_key: Optional partition key name
        attribute_to_get: Optional attribute to retrieve
    """

    table_name: str
    region_name: str
    hash_key: Optional[str] = None
    attribute_to_get: Optional[str] = None


class DynamoDBTable(Table):
    """
    A class to handle DynamoDB table operations with improved error handling
    and configuration management.
    """

    def __init__(
        self,
        table_name: str,
        region_name: str,
        hash_key: Optional[str] = None,
        attribute_to_get: Optional[str] = None,
        host: Optional[str] = None,
    ):
        """
        Initialize DynamoDB table connection and configuration

        Args:
            table_name: Name of the DynamoDB table
            region_name: AWS region name
            hash_key: Optional default hash key
            attribute_to_get: Optional default attribute to retrieve
        """
        self.config = TableConfig(
            table_name=table_name,
            region_name=region_name,
            hash_key=hash_key,
            attribute_to_get=attribute_to_get,
        )
        self.conn: Optional[Connection] = None
        self._initialize_conn(host)
        self._validate_table_exists()

    def _initialize_conn(self, host: Optional[str] = None) -> None:
        """
        Initialize DynamoDB connection

        Args:
            host: Optional host endpoint for DynamoDB

        Raises:
            DynamoDBConnectionError: If connection initialization fails
        """
        try:
            connection_params = {"region": self.config.region_name}
            if host:
                connection_params["host"] = host

            self.conn = Connection(**connection_params)
        except Exception as e:
            raise PynamoDBConnectionError(
                f"Failed to initialize DynamoDB connection: {str(e)}"
            )

    def _validate_table_exists(self) -> None:
        """
        Validate that the specified table exists

        Raises:
            DynamoDBConnectionError: If table doesn't exist or can't be accessed
        """
        try:
            if self.conn:
                self.conn.describe_table(self.config.table_name)
        except Exception as e:
            raise TableDoesNotExist(f"Failed to validate table existence: {str(e)}")

    def _validate_get_parameters(
        self, hash_key: Optional[str], attribute_to_get: Optional[str]
    ) -> tuple[str, str]:
        """
        Validate and resolve get operation parameters

        Args:
            hash_key: Hash key for the item
            attribute_to_get: Attribute to retrieve

        Returns:
            tuple[str, str]: Resolved hash key and attribute to get

        Raises:
            ValueError: If required parameters are missing
        """
        # Resolve hash key
        resolved_hash_key = hash_key or self.config.hash_key
        if not resolved_hash_key:
            raise ValueError(
                "Hash key must be provided either during initialization or method call"
            )

        # Resolve attribute to get
        resolved_attribute = attribute_to_get or self.config.attribute_to_get
        if not resolved_attribute:
            raise ValueError(
                "Attribute to get must be provided either during initialization or method call"
            )

        # Log warnings for duplicate parameters
        if self.config.hash_key and hash_key:
            logger.warning(
                "Hash key provided both during initialization and method call"
            )
        if self.config.attribute_to_get and attribute_to_get:
            logger.warning(
                "Attribute to get provided both during initialization and method call"
            )

        return resolved_hash_key, resolved_attribute

    def get(
        self,
        range_key: Optional[str],
        attribute_to_get: Optional[Any] = None,
        hash_key: Optional[str] = None,
    ) -> Optional[str]:
        """
        Retrieve an item from DynamoDB

        Args:
            range_key: Sort key value
            attribute_to_get: Specific attribute to retrieve
            hash_key: Partition key value

        Returns:
            Optional[str]: Retrieved attribute value

        Raises:
            GetError: If item or attribute not found
            DynamoDBConnectionError: If connection error occurs
            ValueError: If required parameters are missing
        """
        try:
            if not self.conn:
                raise PynamoDBConnectionError("Connection not initialized")

            resolved_hash_key, resolved_attribute = self._validate_get_parameters(
                hash_key, attribute_to_get
            )

            response = self.conn.get_item(
                table_name=self.config.table_name,
                hash_key=resolved_hash_key,
                range_key=range_key,
                attributes_to_get=resolved_attribute,
            )

            if "Item" not in response:
                raise GetError(
                    f"Item not found with hash key '{resolved_hash_key}' and range key '{range_key}'"
                )

            if resolved_attribute not in response["Item"]:
                raise GetError(f"Attribute '{resolved_attribute}' not found in item")

            return list(response["Item"][resolved_attribute].values())[0]

        except (GetError, ValueError) as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Unexpected error during item retrieval: {str(e)}")
            raise
