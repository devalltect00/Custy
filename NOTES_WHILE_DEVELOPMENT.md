on Frontend
cli run()
use pipeline

so we can call command like
custy run commit tag push
So the architecture like

CLI command -> use PIPELINE and presets on CLI part on frontend -> and that each of PIPELINE call the Services part -> each services call GitWorkflowManager class as tool -> GitWorkflowManager as tool call the logic to run the commands based on another pipeline things, different from frontend part. The PIPELINE, pipeline profiles, step registry, use context, and use command resolver. This part another thing from backend -> each pipeline from core or backend side have their own logic and pipeline logic and steps or the flow to run the commands.

Actually I don't know if it is a good design.

So basically let's say we run command like `custy run commit tag push changelog`.
-> what happen next is because it run `custy run`. then use pipeline. we have commit, tag, push, changelog as steps. commit and tag and push, each of them have decorators or wrapper to required_validation(). and changelog not required it (required_validation()). This use app context, decorators/wrapper, registry for PIPELINE and PRESETS

```
PIPELINE = {
    "validate": validate_step,
    "commit": commit_changes_step,
    "tag": tag_bump_step,
    "push": push_changes_step,
    "changelog": changelog_step,
    "workflow": workflow_step,
    "backup-commit": backup_commit_step,
    "backup-tag": backup_tag_step,
    "cleanup-backups": cleanup_backups_step,
    "cleanup-branches": cleanup_branches_step,
}
```

and for example

```
PRESETS = {
    "commit": ["validate", "commit"],
    "release": ["validate", "commit", "tag", "push"],
```

-> each steps call their own services.

- commit call GitOpsService.commit_changes()
- tag call GitOpsService.tag_bump()
- push call GitOpsService.push_changes()
- changelog call ChangelogService.generate_changelog()
  -> each services call the GitWorkflowManager class as tool. where there are functions like run_all() basically run the full workflow and run_commands() can be use like run_commands(["commmit", "tag", "push", "changelog"]), that use the own pipeline logic on core parts or backend. separated pipeline on CLI or frontend.
  -> The pipeline. It use
- StepRegistry class to registry for pipline steps. have method register(), get(), and create() and each steps based on an abstract class BaseStep.
- registry_all_steps() to register all pipeline steps on core or backend side.
- PIPLINE_PROFILES like

```
"release": [
        {"name": "validate"},
        {"name": "workflow_init"},
        {"name": "edit_commit"},
        {"name": "changelog"},
        {"name": "stage"},
        {"name": "commit"},
        {"name": "tag"},
        {"name": "push"},
        {"name": "finalize"},
    ],
```

- use the shared context passed across pipeline steps.
- PipelineBuilder class to Builds pipelines from configuration.
- CommandResolver class to Resolve commands into pipeline step configuration.
  -> each steps on core or backend side call the GitWorkflowManager class method reight there to run the logic or core things.

I don't know, seems the architecture seems complicated and confusing. the Flow seems really complicated and hard to understand
