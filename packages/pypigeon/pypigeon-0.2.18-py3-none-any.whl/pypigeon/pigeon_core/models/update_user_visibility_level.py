from enum import Enum


class UpdateUserVisibilityLevel(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"

    def __str__(self) -> str:
        return str(self.value)
