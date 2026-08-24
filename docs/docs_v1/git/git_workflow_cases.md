<!-- docs/docs_v1/git/git_workflow_cases.md -->

# Git Workflow Transition CASEs

| CASE   | From Branch | From Tier   | To Branch | To Tier     | Purpose                                                     | Initial Workflow                   | Final Workflow                         |
| :----- | :---------- | :---------- | :-------- | :---------- | :---------------------------------------------------------- | :--------------------------------- | :------------------------------------- |
| CASE 1 | develop     | release     | develop   | dev/a/b     | Restart dev cycle after a release (prepare next version)    | checkout develop, pull develop     | None                                   |
| CASE 2 | develop     | dev/a/b     | release   | rc          | Start release candidate process                             | create release/x.y branch          | None                                   |
| CASE 3 | release     | rc          | main      | release     | Finalize and ship release to production                     | checkout main, merge release/x.y   | rebase develop onto main, push develop |
| CASE 4 | main        | release     | main      | dev/a/b     | Continue dev after release from main (e.g. legacy strategy) | checkout main, pull main           | None                                   |
| CASE 5 | main        | release     | hotfix    | post        | Create hotfix branch to patch production                    | checkout main, create hotfix/x.y.z | No-op (actual finalization in CASE 6)  |
| CASE 6 | hotfix      | post        | main      | release     | Merge hotfix into main, delete hotfix branch                | None                               | merge to main, push, delete hotfix     |
| CASE 7 | feature     | dev/release | develop   | dev         | Merge feature branch to develop                             | checkout develop, merge feature/\* | No-op                                  |
| CASE 8 | archive     | release/dev | main      | release     | Preserve or mark branch for archive                         | No-op                              | Informational                          |
| CASE 9 | ci          | release/dev | main      | release/dev | CI/CD branch merged into main (deployment updates)          | checkout develop, merge ci/\*      | merge to main, push                    |
