# app/core/pipeline/command_resolver.py

"""
Command Resolver

Resolves CLI input into pipeline configurations.

Design Principles:
- Profiles are the source of truth
- Resolver does NOT define workflows
- Supports:
    - single profile (commit)
    - multiple commands (commit tag push)
    - composite profiles (dev, release)
"""


class CommandResolver:
    """
    Resolve CLI commands into pipeline step configuration.
    """

    def __init__(self):
        from .profiles import PIPELINE_PROFILES, STEP_ORDER

        self.profiles = PIPELINE_PROFILES
        self.step_order = STEP_ORDER

    def _expand_profile(self, profile_steps: list[dict], visited=None) -> list[dict]:
        if visited is None:
            visited = set()

        expanded = []

        for step in profile_steps:
            name = step["name"]

            # 🚨 Detect circular reference
            if name in visited:
                raise ValueError(
                    f"Circular profile detected: {' -> '.join(visited)} -> {name}"
                )

            # If step is actually a profile → expand it
            if name in self.profiles:
                visited.add(name)
                expanded.extend(self._expand_profile(self.profiles[name], visited))
                visited.remove(name)
            else:
                expanded.append(step)

        return expanded

    def resolve(self, commands: list[str]) -> list[dict]:
        """
        Convert commands into pipeline config.

        Examples:
            ["commit"] → commit profile
            ["commit", "push"] → merged commit + push flow
            ["dev"] → dev profile

        Args:
            commands (List[str])

        Returns:
            List[Dict]
        """

        if not commands:
            raise ValueError("No command provided")

        # =========================
        # Single profile
        # =========================
        if len(commands) == 1 and commands[0] in self.profiles:
            # return self.profiles[commands[0]]

            # This is to handle expanded profiles
            return self._expand_profile(self.profiles[commands[0]])

        # =========================
        # Multiple commands (merge profiles)
        # =========================

        # print("profile_steps",self._merge_profiles(commands))
        return self._merge_profiles(commands)

    def _merge_profiles(self, commands: list[str]) -> list[dict]:
        """
        Merge multiple profiles into one pipeline.

        Example:
            ["commit", "push"]

        Result:
            commit steps + push steps (deduplicated)
        """

        result = []

        for cmd in commands:
            if cmd not in self.profiles:
                raise ValueError(f"Unknown command: {cmd}")

            # result.extend(self.profiles[cmd])

            # This is to handle expanded profiles
            expanded = self._expand_profile(self.profiles[cmd])
            result.extend(expanded)

        # return self._deduplicate(result)
        return self._order_and_deduplicate(result)

    def _deduplicate(self, steps: list[dict]) -> list[dict]:
        """
        Remove duplicate steps while preserving order.

        Important:
        Prevents duplicate 'validate', 'workflow_init', etc.
        """

        seen = set()
        result = []

        for step in steps:
            name = step["name"]
            if name not in seen:
                seen.add(name)
                result.append(step)

        return result

    def _order_and_deduplicate(self, steps: list[dict]) -> list[dict]:
        """
        Normalize pipeline steps by removing duplicates and enforcing execution order.

        This method ensures that when multiple workflow profiles are merged
        (e.g. `commit + tag + push`), the resulting pipeline:

        • contains no duplicate steps
        • follows a consistent, logical execution order

        Ordering is determined by a predefined priority mapping (`STEP_ORDER`),
        which represents the global pipeline flow (validation → preparation →
        generation → execution → finalize).

        Args:
            steps (List[Dict]):
                A list of step definitions, where each step is a dictionary
                containing at least a `"name"` key.

        Returns:
            List[Dict]:
                A deduplicated and ordered list of steps ready for execution.

        Notes:
            • First occurrence of a step is preserved (stable deduplication)
            • Unknown steps are placed at the end of the pipeline
            • This method converts multiple profile pipelines into a single,
              coherent execution flow

        Example:
            Input:
                commit + tag + push profiles

            Output:
                [
                    {"name": "ensure_git_repo_step"},
                    {"name": "prepare_version_step"},
                    {"name": "commit_step"},
                    {"name": "tag_step"},
                    {"name": "push_step"},
                ]
        """
        seen = set()
        unique_steps = []

        for step in steps:
            name = step["name"]
            if name not in seen:
                seen.add(name)
                unique_steps.append(step)

        # 🔥 Sort by defined pipeline order
        return sorted(
            unique_steps,
            key=lambda s: self.step_order.get(s["name"], 999),
        )
