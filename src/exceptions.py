class ContractViolationError(TypeError):
    """Source doesn't match for contract (Protocol)"""

class InvalidTaskError(ValueError):
    """Too bad task (doesn't match to model)"""

class TaskValidationError(ValueError):
    """Base error for task model validation."""


class EmptyTaskIdError(TaskValidationError):
    """Task id is empty or invalid."""


class InvalidDescriptionError(TaskValidationError):
    """Task description is invalid."""


class InvalidPriorityError(TaskValidationError):
    """Task priority is invalid."""


class InvalidStatusError(TaskValidationError):
    """Task status is invalid."""


class InvalidCreatedAtError(TaskValidationError):
    """Task created_at is invalid."""