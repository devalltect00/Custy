# app/cli/context/app_context.py

import typer

from typing import Optional
from dataclasses import dataclass, field
from typing import Optional, Any
import logging

##### Avoid import this, because the error appear. Errors might be looks like: 
#####   (ImportError: cannot import name 'DryRunSupport' from partially initialized module 
#####   'app.core.helper.dry_run' (most likely due to a circular import)).
##### or something like that
# from app.core.helper.git_ops.helper.project_detector import detect_project_strategy

from app.cli.constants.enums import (
    StrategyChoices,
    BumpChoices,
    StageModeChoices,
    LogLevelChoices,
    CleanupTypeChoices,
    InitMode,
)

@dataclass
class AppContext:
    # =========================
    # Global flags
    # =========================
    dry_run: bool = False
    debug: bool = False
    log_level: bool = LogLevelChoices.INFO
    logger: Optional[logging.Logger] = None

    # =========================
    # Shared input files
    # =========================
    # # Init Value
    mode: InitMode = InitMode.ALL
    force_init: bool = False
    ask: bool = False
    # # Git-related
    commit_message_file: Optional[str] = None
    tag_message_file: Optional[str] = None
    version_file: Optional[str] = None
    # # Git Staging
    auto_stage: bool = False
    stage_mode: Optional[str] = StageModeChoices.ALL
    check_cz: bool = False
    # # Git Commit
    force_commit: bool = False
    # # Git Tag
    strategy: list[StrategyChoices] = StrategyChoices.SEMVER
    bump: Optional[list[BumpChoices]] = None
    tag: Optional[str] = None
    tag_message: Optional[str] = None
    pre_release: Optional[str] = None
    post_release: bool = False
    dev_release: bool = False
    meta: Optional[str] = None
    epoch: Optional[int] = None
    force_tag: bool = False
    # # Git Push
    all_remote: bool = True
    remote: Optional[str] = "origin"
    skip_tag: bool = False
    # # changelog
    force_changelog: bool = False
    # # workflow
    enforce: bool = False
    check_transition: bool = False
    from_branch: Optional[str] = None
    to_branch: Optional[str] = None
    from_tag: Optional[str] = None
    to_tag: Optional[str] = None
    # # Cleanup
    type: list[CleanupTypeChoices] = CleanupTypeChoices.ALL
    keep: Optional[int] = 10
    # # Run
    steps: list[str] = None
    # # Global
    # ## changelog and workflow
    sync_backup: bool = False

    # =========================
    # Runtime state
    # =========================
    validated: bool = False

    # deprecated
    current_version: Optional[str] = None
    next_version: Optional[str] = None

    # =========================
    # Raw CLI / runtime objects
    # =========================
    typer_ctx: Any = None
    args: Any = None
    
    # =========================
    # Runtime state
    # =========================
    data: dict = field(default_factory=dict)

    # def update_from_args(self, args, debug_flag: bool):
    #     # direct mappings (same name)
    #     field_map = {
    #         "dry_run": "dry_run",
    #         "log_level": "log_level",
    #         "commit_message_file": "commit_message_file",
    #         "tag_message_file": "tag_message_file",
    #         "version_file": "version_file",
    #         "auto_stage": "auto_stage",
    #         "stage_mode": "stage_mode",
    #     }


    #     for ctx_field, arg_field in field_map.items():
    #         if hasattr(args, arg_field):
    #             setattr(self, ctx_field, getattr(args, arg_field))

    #     # special logic (custom mapping)
    #     self.args = args
    #     self.debug = not args.no_debug if debug_flag else args.no_debug

    def update_from_args(self, args, debug_flag: bool):
        # direct mappings (same name)
        field_map = {
            "dry_run": "dry_run",
            "log_level": "log_level",
            "commit_message_file": "commit_message_file",
            "tag_message_file": "tag_message_file",
            "version_file": "version_file",
            
        }


        for ctx_field, arg_field in field_map.items():
            value = getattr(args, arg_field, None)
            # if hasattr(args, arg_field):
            if value is not None:
                setattr(self, ctx_field, getattr(args, arg_field))

        # special logic (custom mapping)

        # always store args
        self.args = args

        # ✅ SAFE debug handling
        no_debug = getattr(args, "no_debug", None)

        if no_debug is not None:
            self.debug = not args.no_debug if debug_flag else args.no_debug

    def update_from_args_v1(self, args, debug_flag: bool):
        # iterate only over args (source of truth)
        for key, value in vars(args).items():
            # skip internal/private fields if any
            if key.startswith("_"):
                continue

            # only update if AppContext actually has this field
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)

        # always store raw args
        self.args = args

        # safe debug handling
        if hasattr(args, "no_debug"):
            no_debug = args.no_debug
            self.debug = not no_debug if debug_flag else no_debug

    def update_from_args_and_fields(
        self,
        args,
        debug_flag: bool,
        fields: list[str] | dict[str, str] | None = None,
    ):
        # 🔹 Case 1: No fields provided → fallback (auto mode)
        if fields is None:
            for key, value in vars(args).items():
                if hasattr(self, key) and value is not None:
                    setattr(self, key, value)

        # 🔹 Case 2: List of fields (same name mapping)
        elif isinstance(fields, list):
            for field in fields:
                value = getattr(args, field, None)
                if value is not None:
                    setattr(self, field, value)

        # 🔹 Case 3: Dict mapping (custom names)
        elif isinstance(fields, dict):
            for ctx_field, arg_field in fields.items():
                value = getattr(args, arg_field, None)
                if value is not None:
                    setattr(self, ctx_field, value)

        # store raw args
        self.args = args

        # 🔹 safe debug handling
        no_debug = getattr(args, "no_debug", None)
        if no_debug is not None:
            self.debug = not no_debug if debug_flag else no_debug

def get_context(ctx: typer.Context) -> AppContext:
    if ctx.obj is None:
        ctx.obj = AppContext()
    
    ctx.obj.typer_ctx = ctx
    return ctx.obj
