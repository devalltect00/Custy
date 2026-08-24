# app/core/pipeline/registry.py

"""
Step Registry

Allows dynamic registration of pipeline steps.

Supports:
- registering steps by name
- retrieving steps dynamically
- building pipelines from config

This enables plugin-like behavior.
"""

from typing import Dict, Type
from .steps.base_step import BaseStep


class StepRegistry:
    """
    Registry for pipeline steps.

    Examples:
        StepRegistry.register("validate", ValidateStep)
        step_cls = StepRegistry.get("validate")
    """

    _registry: Dict[str, Type[BaseStep]] = {}

    @classmethod
    def register(cls, name: str, step_cls: Type[BaseStep]) -> None:
        """
        Register a step.

        Args:
            name (str): Unique step name
            step_cls (BaseStep): Step class

        Raises:
            ValueError: If step already exists
        """
        if name in cls._registry:
            raise ValueError(f"Step '{name}' already registered")

        cls._registry[name] = step_cls

    @classmethod
    def get(cls, name: str) -> Type[BaseStep]:
        """
        Retrieve step class by name.

        Args:
            name (str)

        Returns:
            BaseStep

        Raises:
            KeyError: If step not found
        """
        if name not in cls._registry:
            raise KeyError(f"Step '{name}' not found")

        return cls._registry[name]

    @classmethod
    def create(cls, name: str, **kwargs) -> BaseStep:
        """
        Instantiate step by name.

        Args:
            name (str)
            kwargs: Step constructor args

        Returns:
            BaseStep instance
        """
        step_cls = cls.get(name)
        return step_cls(**kwargs)
