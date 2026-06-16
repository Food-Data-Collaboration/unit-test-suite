"""Test adapter interface.

Each platform must implement this adapter to run the interop tests.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class TestAdapter(ABC):
    """Base class for platform-specific test adapters."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name (e.g., 'python-rdflib')."""

    @abstractmethod
    def parse_jsonld(self, data: dict[str, Any]) -> Any:
        """Parse a JSON-LD document into the platform's native structure.

        Args:
            data: Parsed JSON-LD dictionary

        Returns:
            Platform-specific parsed representation
        """

    @abstractmethod
    def serialize_jsonld(self, data: Any) -> dict[str, Any]:
        """Serialize a platform's native structure back to JSON-LD.

        Args:
            data: Platform-specific parsed representation

        Returns:
            JSON-LD dictionary
        """

    @abstractmethod
    def validate(self, data: dict[str, Any]) -> list[str]:
        """Validate a JSON-LD document against its context.

        Args:
            data: Parsed JSON-LD dictionary

        Returns:
            List of validation error messages (empty if valid)
        """

    @abstractmethod
    def expand(self, data: dict[str, Any]) -> Any:
        """Expand a JSON-LD document.

        Args:
            data: Parsed JSON-LD dictionary

        Returns:
            Expanded JSON-LD
        """

    @abstractmethod
    def compact(self, data: Any, context: dict[str, Any]) -> dict[str, Any]:
        """Compact a JSON-LD document.

        Args:
            data: Expanded JSON-LD
            context: Context to compact with

        Returns:
            Compacted JSON-LD dictionary
        """

    @abstractmethod
    def flatten(self, data: dict[str, Any]) -> dict[str, Any]:
        """Flatten a JSON-LD document.

        Args:
            data: Parsed JSON-LD dictionary

        Returns:
            Flattened JSON-LD dictionary
        """
