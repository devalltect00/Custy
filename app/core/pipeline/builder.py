# app/core/pipeline/builder.py

"""
Pipeline Builder

Responsible for constructing pipeline dynamically.

Supports:
- predefined flows
- custom flows
- plugin-based step creation
"""

from typing import List, Dict, Any
from .pipeline import Pipeline, SimplePipeline
from .registry import StepRegistry


class PipelineBuilder:
    """
    Builds pipelines from configuration.

    Examples:
        builder = PipelineBuilder()
        pipeline = builder.build([
            {"name": "validate"},
            {"name": "commit"},
        ])
    """
    
    def __init__(self, isVisible: bool = True):
        self.isVisible = isVisible

    def build(self, config: List[Dict[str, Any]]) -> Pipeline:
        """
        Build pipeline from config list.

        Args:
            config (List[Dict]):
                [
                    {"name": "validate"},
                    {"name": "cleanup", "args": {"cleanup_backups": True}}
                ]

        Returns:
            Pipeline
        """
        steps = []

        for step_cfg in config:
            name = step_cfg["name"]
            args = step_cfg.get("args", {})

            step = StepRegistry.create(name, **args)
            steps.append(step)

        return Pipeline(steps, self.isVisible)
    

class SimplePipelineBuilder:
    """
    Builds pipelines from configuration.

    Examples:
        builder = SimplePipelineBuilder()
        pipeline = builder.build([
            {"name": "validate"},
            {"name": "commit"},
        ])
    """
    
    def __init__(self, useCompletedMessage: bool = True):
        self.useCompletedMessage = useCompletedMessage

    def build(self, config: List[Dict[str, Any]]) -> Pipeline:
        """
        Build pipeline from config list.

        Args:
            config (List[Dict]):
                [
                    {"name": "validate"},
                    {"name": "cleanup", "args": {"cleanup_backups": True}}
                ]

        Returns:
            Pipeline
        """
        steps = []

        for step_cfg in config:
            name = step_cfg["name"]
            args = step_cfg.get("args", {})

            step = StepRegistry.create(name, **args)
            steps.append(step)

        return SimplePipeline(steps, self.useCompletedMessage)
