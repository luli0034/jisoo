from __future__ import annotations
import json
from typing import Optional, List, Dict, Union, Any
from enum import Enum
from pydantic import field_validator, BaseModel, PrivateAttr, computed_field
from jisoo.models.state.retry import Retry
from jisoo.models.state.catch import Catch


class ErrorHandler(BaseModel):
    """Handles error management through retry and catch mechanisms.

    This class manages error handling configurations for state machines,
    supporting both single and multiple retry/catch configurations.

    Attributes:
        retry (Optional[Union[Retry, List[Retry], List[Dict]]]): Retry configuration(s)
        catch (Optional[Union[Catch, List[Catch], List[Dict]]]): Catch configuration(s)
    """

    retry: Optional[Union[Retry, List[Retry], List[Dict]]] = None
    catch: Optional[Union[Catch, List[Catch], List[Dict]]] = None

    @field_validator("retry", mode="after")
    @classmethod
    def set_retries(
        cls, value: Optional[Union[Retry, List[Retry]]]
    ) -> List[Dict[str, Any]]:
        """Validates and transforms retry configurations into a list of dictionaries.

        Args:
            value: Single Retry instance or list of Retry instances

        Returns:
            List[Dict[str, Any]]: List of retry configurations as dictionaries
        """
        if value is None:
            return []

        retries: List[Dict[str, Any]] = []

        if isinstance(value, Retry):
            retries.append(value.to_dict())
        elif isinstance(value, list):
            retries.extend(retry.to_dict() for retry in value)

        return retries

    @field_validator("catch", mode="after")
    @classmethod
    def set_catches(
        cls, value: Optional[Union[Catch, List[Catch]]]
    ) -> List[Dict[str, Any]]:
        """Validates and transforms catch configurations into a list of dictionaries.

        Args:
            value: Single Catch instance or list of Catch instances

        Returns:
            List[Dict[str, Any]]: List of catch configurations as dictionaries

        Note:
            The current implementation checks for Retry instead of Catch in the first
            isinstance check, which might be a bug in the original code.
        """
        if value is None:
            return []

        catches: List[Dict[str, Any]] = []

        if isinstance(value, Catch):
            catches.append(value.to_dict())
        elif isinstance(value, list):
            catches.extend(catch.to_dict() for catch in value)

        return catches


class NextHandler(BaseModel):
    """Handles state transitions in a state machine.

    This class manages the next state information and end state flags
    for state machine transitions.

    Attributes:
        _next (Optional[str]): Private attribute storing the next state identifier
        end (Optional[bool]): Flag indicating if this is an end state
    """

    _next: Optional[str] = PrivateAttr(None)
    _end: Optional[bool] = PrivateAttr(None)

    @computed_field
    def next(self) -> Optional[str]:
        """Get the identifier of the next state.

        Returns:
            Optional[str]: The identifier of the next state, if any
        """
        return self._next

    @computed_field
    def end(self) -> Optional[bool]:
        """Check if the current state is an end state."""
        return self._end
