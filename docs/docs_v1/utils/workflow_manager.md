<!-- docs/docs_v1/utils/workflow_manager.md -->

| Case | From Branch | From Tier | To Branch   | To Tier |
| ---- | ----------- | --------- | ----------- | ------- |
| 1    | `main`      | release   | `develop`   | dev/a/b |
| 2    | `develop`   | dev/a/b   | `release/*` | rc      |
| 3    | `release/*` | rc        | `main`      | release |
| 4    | `develop`   | release   | `develop`   | dev/a/b |
| 5    | `main`      | release   | `hotfix/*`  | post    |
| 6    | `hotfix/*`  | post      | `main`      | release |
| 7    | `feature/*` | —         | `develop`   | —       |
| 8    | `archive/*` | —         | —           | —       |
| 9    | `ci/*`      | —         | —           | —       |
