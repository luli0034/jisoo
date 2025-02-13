from jisoo.models.state import State
from typing import Optional, List
from jisoo.models.state.base import Block


class Retry(Block):
    """
    Represents a retry policy for error handling in state executions.

    A Retry block defines how a state should retry its execution when specific errors occur.
    It specifies which errors to catch, how many retry attempts to make, and the timing
    between retries with optional exponential backoff.

    Attributes:
        error_equals (List[ErrorEqualsEnum]): List of error types that trigger retries.
            Can include specific error names or predefined error types like
            "States.ALL", "States.Timeout", etc.
        interval_seconds (Optional[int]): Number of seconds to wait between retry attempts.
            Defaults to None
        max_attempts (Optional[int]): Maximum number of retry attempts before giving up.
            Defaults to None
        backoff_rate (Optional[float]): Multiplier for interval_seconds between retries.
            Each subsequent retry will wait backoff_rate times longer.
            Defaults to None

    Example:
        >>> from jisoo.models.common import ErrorEqualsEnum
        >>> retry = Retry(
        ...     error_equals=[ErrorEqualsEnum.Events.STATES_TIMEOUT],
        ...     interval_seconds=2,
        ...     max_attempts=3,
        ...     backoff_rate=2.0
        ... )

    Note:
        - If max_attempts is reached without success, the state will fail
        - With backoff_rate=2.0 and interval_seconds=2, retries would wait:
          2 seconds, then 4 seconds, then 8 seconds
        - The error_equals list is processed in order when matching errors
    """

    error_equals: List[str]
    interval_seconds: Optional[int] = None
    max_attempts: Optional[int] = None
    backoff_rate: Optional[float] = None
