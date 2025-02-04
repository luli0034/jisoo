from __future__ import absolute_import


class MissingRequiredParameter(Exception):
    pass


class DuplicateStateError(Exception):
    pass


class StateUndefinedError(Exception):
    pass


class EmptyStateInGraph(Exception):
    pass


class EmptyStateInChain(Exception):
    pass


class DuplicateStatesInChain(Exception):
    pass


class InvalidGraph(Exception):
    pass


class InvalidRule(Exception):
    pass


class InvalidInputScheam(Exception):
    pass
