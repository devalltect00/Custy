[33mcommit 20a8549bd42bc07a76a6bf3f93f73ef0eb6f9e94[m[33m ([m[1;36mHEAD -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m, [m[1;31mbackup/main[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Sat Aug 2 00:13:04 2025 +0700

    docs(changelog): update changelog

[33mcommit d7c82ab620872306f83b5b95f243d75116863682[m[33m ([m[1;33mtag: 1.8.0[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Sat Aug 2 00:12:33 2025 +0700

    release(core): 1.8.0
    
    Final release of **Custy 1.8.0**, promoted from the latest release candidate.
    includes all feature and fixes from pre-releases: 1.8.0rc2, 1.8.0rc1.
    
    This final release includes all validated features and fixes from earlier pre-releases:
    - Git workflow validation via WorkflowManager
    - Temporary branch cleanup with Branch Cleaner
    - Dual remote strategy: GitLab (main), GitHub (backup)
    - Strategy-specific version helpers (PEP 440, SemVer)
    - Cleaner code structure with VersionHelperBase
    - Updated Makefile and improved documentation
    
    🛠 Final tweaks after rc2:
    - Allow `custy all` to run `--sync-backup` automatically
    - Minor improvements to support `release` commit type
    - Refined docs and cleaned up TODO list
    
    Tag: 1.8.0
    Changelog: handled separately

[33mcommit 17172ceae03cc48d2e1e7bd600d2e1b9e4eda16e[m[33m ([m[1;33mtag: 1.8.0rc2[m[33m, [m[1;31morigin/release/1.8[m[33m, [m[1;31mbackup/release/1.8[m[33m, [m[1;32mrelease/1.8[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 23:48:24 2025 +0700

    refactor(workflow): 1.8.0rc2
    
    Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
    Feature-complete and undergoing final validation before stable release.
    
    This refactor decouples strategy-specific logic (PEP 440, SemVer) from the core
    WorkflowManager class by introducing a VersionHelperBase interface. Both
    PEP440VersionHelper and SemverVersionHelper now implement:
    
    - classify(): identify version tier
    - tier_order(): precedence for tier promotion
    - suggest_tag(): next tag suggestion based on branch
    - get_transition_cases(): valid CASE transitions
    
    WorkflowManager is now cleaner and delegates classification, version suggestion,
    and transition validation to the appropriate strategy helper dynamically.
    
    This release candidate consolidates finalized features and bug fixes before the stable release:
    - Update `docs/TODO.md` to reflect recent changes and clean up outdated entries
    
    Other improvements:
    - Reduced branching logic in check_transition()
    - Added docstrings across all helper classes
    - Improved extensibility for future strategies (e.g., CalVer)
    
    BREAKING CHANGE: version helpers must now implement VersionHelperBase interface
    
    Tag: 1.8.0rc2

[33mcommit 3d51cabdea633089e0c3bfa2a6af0cc4a28b20c2[m[33m ([m[1;33mtag: 1.8.0rc1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 21:26:07 2025 +0700

    fix(core): 1.8.0rc1
    
    Release candidate for **Custy 1.8.0**, consolidating all pre-release changes and preparing for stable release.
    Feature-complete and undergoing final validation before stable release.
    
    This release candidate consolidates finalized features and bug fixes before the stable release:
    - use 2 permanent branches: `main` (stable) and `develop` (experimental)
    - configure dual remote setup: GitLab as main, GitHub as backup
    - implement branching workflow checking (WorkflowManager)
    - add branch cleaner to prune temporary branches
    - update Makefile with latest tasks
    - expand documentation
    
    Tag: 1.8.0rc1

[33mcommit 086a5c8f00338a8da6e2aff5b76cc62ea9db9502[m[33m ([m[1;33mtag: n[m[33m, [m[1;31morigin/develop[m[33m, [m[1;31mbackup/develop[m[33m, [m[1;32mdevelop[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 00:19:03 2025 +0700

    docs(changelog): update changelog

[33mcommit 9cbdb936b60c28c3f2ead5f334790ae66433b96f[m[33m ([m[1;33mtag: 1.7.1.post1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 00:18:40 2025 +0700

    fix(release): 1.7.1.post1
    
    Post-release patch for **Custy 1.7.1**, addressing minor updates or corrections.
    Includes minor updates or documentation fixes after release 1.7.1.
    
    This post-release includes minor updates and corrections after the official release:
    - Allow CLI to accept arguments without explicitily requiring the `--bump` flag
    - Fix issue in the `Makefile` execution flow
    - Update `docs/TODO.md` to reflect recent changes and clean up outdated entries
    
    Tag: 1.7.1.post1
    Changelog: handled separately

[33mcommit dd4fe615173484248adf860c826efd834a18686e[m
Merge: 48fc183 c260b9b
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 00:04:18 2025 +0700

    merge release 1.7.1 into main

[33mcommit c260b9b259cca22f8d2302e556df05123f732b19[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 00:01:26 2025 +0700

    docs(changelog): update changelog

[33mcommit cd9369345015f6f0a5918da140508c4de0f3de40[m[33m ([m[1;33mtag: 1.7.1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Aug 1 00:01:07 2025 +0700

    fix(release): 1.7.1
    
    Final release of **Custy 1.7.1**, promoted from the latest release candidate.
    includes all feature and fixes from pre-releases: .
    
    This final release includes all validated features and fixes from earlier pre-releases:
    - Fix the file name from `pep404_strategy.py` → `pep440_strategy.py`
    - Rename class from `PEP404Strategy` → `PEP440Strategy`
    - Bug fix: Switch to post-release uses `1.5.0.post1` instead of bumping minor to `1.6.0.post1`
    - Refactor and clean up `SemverStrategy` and `PEP440Strategy` classes
    - Add test coverage for both strategy classes
    - Add documentation: `docs/versioning/switching version.md`
    - Verbose step logging before changelog generation to improve debugging
    - Ensure commit and tag backup files are staged before commit
    - Improve dry-run flow in message generation
    - Update `TODO.md` to reflect current feature status
    
    Tag: 1.7.1
    Changelog: handled separately

[33mcommit 48fc1830759e29e7cb4cb3badf24fe5dbe49d8bc[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 02:15:58 2025 +0700

    docs(changelog): update changelog

[33mcommit 6bdd038163ea4b406c1058d699bbebb757f6a33a[m[33m ([m[1;33mtag: 1.7.0.post3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 02:15:39 2025 +0700

    docs(release): 1.7.0.post3
    
    Post-release patch for **Custy 1.7.0**, addressing minor updates or corrections.
    Includes minor updates or documentation fixes after release 1.7.0.
    
    This post-release includes minor updates and corrections after the official release:
    - modified documentation `docs/TODO.md`
    
    Tag: 1.7.0.post3
    Changelog: handled separately

[33mcommit add1ba4016aae3853025ec7d1e2efe03c7052cc0[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 02:12:15 2025 +0700

    docs(changelog): update changelog

[33mcommit bc909034e4e24fcbba7be12ffe701a99729abcae[m[33m ([m[1;33mtag: 1.6.0.post2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 02:11:55 2025 +0700

    fix(release): 1.6.0.post2
    
    Post-release patch for **Custy 1.6.0**, addressing minor updates or corrections.
    Includes minor updates or documentation fixes after release 1.6.0.
    
    This post-release includes minor updates and corrections after the official release:
    - Bug fixed case example changes from 1.5.0.post1 → 1.5.0.post2
    - Bug fixed on `Makefile`
    - modified documentation `docs/TODO.md`
    
    Tag: 1.6.0.post2
    Changelog: handled separately

[33mcommit 14f09c9929c246c9dd9c30dfdce081f70d7c0fd8[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 01:48:38 2025 +0700

    docs(changelog): update changelog

[33mcommit b4b83b8af19982823cf9dec6de17edbd9724b5f4[m[33m ([m[1;33mtag: v1.5.0.post1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 01:48:20 2025 +0700

    docs(release): v1.5.0.post1
    
    Post-release patch for **Custy v1.5.0**, addressing minor updates or corrections.
    Includes minor updates or documentation fixes after release v1.5.0.
    
    This post-release includes minor updates and corrections after the official release:
    - Added a new documentation `docs/Q&A/git/footer section on tag message.md`
    - modified documentations `docs/Q&A/git/changelogs approach.md`, `docs/Q&A/git/comparison commit and tag message.md`, `docs/TODO.md`
    - Modified Makefile by adding documentations
    
    Tag: v1.5.0.post1
    Changelog: handled separately

[33mcommit 17bb6b22774d2cbcc2020d39294236d5bdad01e5[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 01:14:44 2025 +0700

    docs(changelog): update changelog

[33mcommit dfc0fe7b2f5fb2269177c4c948e19e31749758c8[m[33m ([m[1;33mtag: 1.5.0[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 01:14:26 2025 +0700

    feat(release): 1.5.0
    
    Final release of **Custy 1.5.0**, promoted from the latest release candidate.
    includes all feature and fixes from pre-releases: 1.5.0rc1, 1.5.0b3, 1.5.0b2, 1.5.0b1.
    
    This final release includes all validated features and fixes from earlier pre-releases:
    - Add structured generation of `commit-msg.txt` and `tag-msg.txt`
    - Improve message clarity, flexibility, and consistency
    - Enhance template customization for different version types (alpha, beta, rc, final)
    - Ensure commit/tag message files are properly staged and backed up
    - Fix dry-run behavior in message generation flow
    - Address minor edge cases in automation
    - Reference commit/tag standards in `docs\git\commit_message.md`
    - Add internal usage notes and automation guidance
    - Ensure commit and tag backup files and odl files to staged and commit
    - Handle staged and commit when no staged changes detected
    - Updated `TODO.md`
    
    Tag: 1.5.0
    Changelog: handled separately

[33mcommit 149b2969439816b63f5476de6d9b17c8d3f01c84[m[33m ([m[1;33mtag: 1.5.0rc1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 00:37:42 2025 +0700

    docs(release): 1.5.0rc1
    
    Release candidate for **Custy 1.5.0**, consolidating all pre-release changes and preparing for stable release.
    Feature-complete and undergoing final validation before stable release.
    
    This release candidate consolidates finalized features and bug fixes before the stable release:
    - *(Nothing yet)* — See tag message for full context.
    
    Tag: 1.5.0rc1

[33mcommit 45c5b0cfb388336a93b002354d5f9918fcdff633[m[33m ([m[1;33mtag: 1.5.0b3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 31 00:31:43 2025 +0700

    fix(release): 1.5.0b3
    
    Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
    Partially validated features and improvements. Some issue still remain.
    
    This beta includes several bug fixes and enhancements:
    - *(Nothing yet)* — See tag message for full context.
    
    Tag: 1.5.0b3

[33mcommit 829d5b5b7a844b5bdaa2837a942f2086357a60bd[m[33m ([m[1;33mtag: 1.5.0b2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Wed Jul 30 23:57:17 2025 +0700

    fix(release): 1.5.0b2
    
    Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
    Partially validated features and improvements. Some issue still remain.
    
    This beta includes several bug fixes and enhancements:
    - *(Nothing yet)* — See tag message for full context.
    
    Tag: 1.5.0b2

[33mcommit 7772841096ee1b2d5a5a575cee1531b90a6494c7[m[33m ([m[1;33mtag: 1.5.0b1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Wed Jul 30 22:08:27 2025 +0700

    feat(release): 1.5.0b1
    
    Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
    Partially validated features and improvements. Some issue still remain.
    
    This beta includes several bug fixes and enhancements:
    - *(Nothing yet)* — See tag message for full context.
    
    Tag: 1.5.0b1

[33mcommit e0a6e8e497d9da8ef32162a33106299c51dd4808[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Wed Jul 30 21:56:01 2025 +0700

    chore(release): 1.5.0b1
    
    Beta release for **Custy 1.5.0**, introducing mid-stage features and workflow improvements.
    Partially validated features and improvements. Some issue still remain.
    
    This beta includes several bug fixes and enhancements:
    - *(Nothing yet)* — See tag message for full context.
    
    Tag: 1.5.0b1

[33mcommit 0cda3899451ad5a293377bc5b304410f1cc7de1c[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:42:12 2025 +0700

    chore(release): v1.5.0a1
    
    - _(Nothing yet)_
    
    Tag: v1.5.0a1

[33mcommit 0e4f9bfb3b8efe08b8092d1ccdc41fc104b1047f[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:41:45 2025 +0700

    chore(release): v1.5.0a2
    
    - _(Nothing yet)_
    
    Tag: v1.5.0a2

[33mcommit 8c6acf8d9ff87e55ac81ac12b168e45787470a3c[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:40:52 2025 +0700

    chore(release): v1.5.0rc1
    
    - _(Nothing yet)_
    
    Tag: v1.5.0rc1

[33mcommit da30be48298120dfaae7f35156777ccc45e9c9e9[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:37:24 2025 +0700

    chore(release): v1.5.0
    
    - _(Nothing yet)_
    
    Tag: v1.5.0

[33mcommit 9fecd4a5373bd5f32a01c64006d3bf4d19f799a8[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:16:10 2025 +0700

    docs(changelog): update changelog

[33mcommit fb2dfd93349baa92ec71b1193e9dae71d55a8aa5[m[33m ([m[1;33mtag: 1.4.3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:15:54 2025 +0700

    refactor(release): v1.4.3
    
    Final release of Custy v1.4.3
    
    Refactor Code using Ruff
    
    Tag: v1.4.3
    Changelog: handled separately

[33mcommit 7c19118f6421a8cc2e53432468beadd8eda121cc[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:06:04 2025 +0700

    docs(changelog): update changelog

[33mcommit 17f4b4455500a3b1896eefa35c89bc6cc58a778b[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:05:52 2025 +0700

    chore(release): v1.4.2
    
    Final release of Custy v1.4.2
    
    Includes modified documentation.
    
    Tag: v1.4.2
    Changelog: handled separately

[33mcommit 52929fdaee75ae0e8ff9609616cf8c2ba10efd30[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:03:46 2025 +0700

    docs(changelog): update changelog

[33mcommit 8696bc6e39bc68078105bb613a2a0820e0b00410[m[33m ([m[1;33mtag: 1.4.2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 20:03:30 2025 +0700

    docs(release): v1.4.1
    
    Final release of Custy v1.4.1
    
    Includes modified documentation.
    
    Tag: v1.4.1
    Changelog: handled separately

[33mcommit 5070549ca510b0870c5d49a15b5b35cbf1c2026f[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:51:48 2025 +0700

    docs(changelog): update changelog

[33mcommit 000ed9f706352ccb5d947bb89a2aee1a7a3cdf90[m[33m ([m[1;33mtag: 1.4.1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:51:33 2025 +0700

    fix(release): v1.4.1
    
    Final release of Custy v1.4.1
    
    Includes bug fixes.
    
    Tag: v1.4.1
    Changelog: handled separately

[33mcommit d2d24c16d61c4c53f95734ab8fa2ade7e5ac5651[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:47:45 2025 +0700

    docs(changelog): update changelog

[33mcommit 8a95deb8d328704cdc06b631641d8b0a493840a4[m[33m ([m[1;33mtag: 1.4.0[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:47:31 2025 +0700

    docs(release): v1.4.1
    
    Final release of Custy v1.4.1
    
    Includes bug fixes.
    
    Tag: v1.4.1
    Changelog: handled separately

[33mcommit bf4a9a2432784974df551c5a0a088e79c9c30ab3[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:40:47 2025 +0700

    docs(changelog): update changelog

[33mcommit bb60477b0add0d66c920d7cd882bc20a0ae293b3[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:40:37 2025 +0700

    chore(release): v1.4.0
    
    Final release of Custy v1.4.0 - prompted from release candidate.
    
    Includes all feature and fixes from alpha and RC pre-releases.
    
    Tag: v1.4.0
    Changelog: handled separately

[33mcommit 0744a080f8664808ce0220a1b68682d2ef6361b5[m[33m ([m[1;33mtag: 1.4.0rc3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:31:25 2025 +0700

    fix(release): v1.4.0rc5
    
    Release candidate for v1.4.0, consolidating all pre-release changes.
    
    - Resolved issue with `get_commits_between_tags()` in `GitHelper`(`app\utils\git.py`).
    
    Tag: v1.4.0rc5

[33mcommit d14689066122993c15b7eaa7dd52ffaffc86e39b[m[33m ([m[1;33mtag: 1.4.0rc2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:24:45 2025 +0700

    fix(release): v1.4.0rc4
    
    Release candidate for v1.4.0, consolidating all pre-release changes.
    
    - Resolved issue with `_prepare_release_message_from_prereleases()` in `GitCommitTagger`(`app\git_commit_tagger.py`).
    
    Tag: v1.4.0rc4

[33mcommit 5a216e38e7d9d58245e840fcd609a760620ed7d1[m[33m ([m[1;33mtag: 1.4.0rc1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 19:13:11 2025 +0700

    fix(release): v1.4.0rc3
    
    Release candidate for v1.4.0, consolidating all pre-release changes.
    
    - Resolved issue with `get_last_tag_before()` in `GitHelper`(`app\utils\git.py`).
    
    Tag: v1.4.0rc3

[33mcommit 52a740f03be017064c3cd0049e13e3010bedf934[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 18:54:43 2025 +0700

    chore(release): v1.4.0rc2
    
    Release candidate for v1.4.0, consolidating all pre-release changes.
    
    - Improve docs
    
    Tag: v1.4.0rc2

[33mcommit 5ff2fdbce267176fa59586bbe4769bc974e29539[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 18:35:56 2025 +0700

    chore(release): v1.4.0rc1
    
    Release candidate for v1.4.0, consolidating all pre-release changes.
    
    Includes:
    - Version bump protection within pre-release tier (e.g., rc1 → rc2)
    - Restriction of changelog to final releases only
    - Commit type validation for bump/tag operations
    - Project type detection (PEP 440 or SemVer) for versioning
    - External tag message support (`tag-msg.txt`)
    - Auto-generation of release commit/tag message templates
    - RC → final bump without patch increment
    - `cleanup-backups` CLI command
    - Improved dry-run behavior
    - Expanded documentation and Makefile updates
    - Backup/template folder resolution fixes
    
    Tag: v1.4.0rc1

[33mcommit 0e24bf216523ccf9bac093d441fb6444c6faeffc[m[33m ([m[1;33mtag: 1.4.0a1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Tue Jul 29 16:19:28 2025 +0700

    feat(core): implement advanced versioning rules and CLI behavior controls
    
    This commit introduces a series of improvements across versioning, tagging, changelog generation, and backup handling in Custy CLI.
    
    - Prevents major.minor.patch bump when incrementing within same pre-release tier (e.g. rc1 → rc2)
    - Generates changelog only on final releases (e.g. v1.2.3), skipping pre-releases
    - Enforces bump/tag only for specific types [feat, fix, perf, docs, refactor]; others require CLI override
    - Detects project type (Python or JavaScript) to apply correct versioning scheme (PEP 440 or SemVer)
    - Tag messages now opened in external file like commit-msg.txt; supports default message via flag
    - For release tags, auto-generates commit/tag message template from all prereleases (pre, dev, etc.)
    - Prevents bump from rc → final from incrementing patch (v1.2.3rc1 → v1.2.3, not v1.2.4)
    - Adds cleanup logic for `backups/`, keeping 10 latest (customizable via CLI)
    - Fixes backup and template folder resolution; commit-msg.txt placement corrected
    - Adds `cleanup-backups` CLI handler
    - Updated `.gitignore` to ignore `templates/tag-msg.txt`
    - Updated `.projectignore` to ignore `templates/tag-msg.txt`
    
    Changelog: handled separately

[33mcommit b9841b2139269d2c39f72995e2215efe752d4409[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:41:22 2025 +0700

    docs(changelog): update changelog

[33mcommit 7f3cd6a30ba490ea73fab47548abadbe8901bf25[m[33m ([m[1;33mtag: 1.3.3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:41:11 2025 +0700

    docs(TODO.md): add or change todo
    
    - add or change todo
    
    Changelog: handled separately

[33mcommit 0e6e37864143a74c645a70f35cc507702d1b3034[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:39:19 2025 +0700

    docs(changelog): update changelog

[33mcommit 03fcda08983d826388749eb6a341726dcdde5415[m[33m ([m[1;33mtag: 1.3.2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:39:08 2025 +0700

    docs(TODO.md): add or change todo
    
    - add or change todo
    
    Changelog: handled separately

[33mcommit 5a2b9e5cfd23dcc0554f97d934370cdb5bb8c723[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:28:37 2025 +0700

    docs(changelog): update changelog

[33mcommit 04780490ee681c259a5afb27a07190f49e81dbb2[m[33m ([m[1;33mtag: 1.3.1rc2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 20:28:19 2025 +0700

    chore(commit_msg): support 'release' as valid Conventional Commit type
    
    - Added 'release' to allowed commit types in the validator
    
    Changelog: handled separately

[33mcommit 26b301749deca7e16964d4ed1a9c9d6491cb571b[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 19:58:48 2025 +0700

    docs(changelog): update changelog

[33mcommit 80e4d6b35f1af02f2a696bccca6c7bbb2de15cdc[m[33m ([m[1;33mtag: 1.3.0rc1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 19:58:34 2025 +0700

    feat(versioning): Improve pre-release and full versioning support with PEP 440
    
    - Fix pre-release version format to comply with pep440 for python
    - Add support for full format: [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
    - Additionally support Post-release, development, local identifiers, and epoch segment
    
    Changelog: handled separately

[33mcommit 23ac55ebb1022b4c958bca603d0f7c5b3b346c7b[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 14:16:38 2025 +0700

    docs(changelog): update changelog

[33mcommit 7b2735623cbfc54bae016941376120495eea688c[m[33m ([m[1;33mtag: v1.2.0[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 14:16:29 2025 +0700

    feat(git_commit_tagger): replace cz check with custom commit message checker
    
    - Replaces Commitizen's `cz check` with a built-in custom validator
    - Supports multi-line messages with header, body, and footer.
    - Includes structured error handling via custom ValidationError exception.
    
    Changelog: handled separately

[33mcommit fdd7534d4deffe5365b0dde2f3062ccc9f431c2b[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 12:56:27 2025 +0700

    docs(changelog): update changelog

[33mcommit edd1e7993464b0049bbae2397ad6213e5eff3159[m[33m ([m[1;33mtag: v1.1.5[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 12:56:17 2025 +0700

    fix(git_commit_tagger): add or change todo
    
    - Fix issue where added to stage and commit after change version on `.cz.toml` and `app/__version__.py` files
    - stage files before commit. stage the  `.cz.toml`, `app/__version__.py`, and backup file creared
    
    Changelog: handled separately

[33mcommit dc737c5c9922e9dd81e868f0fd3ca88ae15f14fc[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:44:51 2025 +0700

    docs(changelog): update changelog

[33mcommit 4af92997abe1597faf047bc12bf3567923e197de[m[33m ([m[1;33mtag: v1.1.4[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:44:42 2025 +0700

    docs(TODO.md): add or change todo
    
    - add or change todo
    
    Changelog: handled separately

[33mcommit c50c313936b0352d6b1ad8d1070052e21fad4504[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:37:20 2025 +0700

    docs(changelog): update changelog

[33mcommit de4c3bb17498747abe3959498a6361c40d7bf2fc[m[33m ([m[1;33mtag: v1.1.3[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:37:11 2025 +0700

    fix(Makefile): correct commands
    
    - Fixed broken or unclear `Makefile` commands
    
    Changelog: handled separately

[33mcommit 25846033fbfc7dd6b1655ed6e189b72e459cd0a8[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:29:20 2025 +0700

    docs(changelog): update changelog

[33mcommit f0544627e9f05bf39468bce9399f6be4414af693[m[33m ([m[1;33mtag: v1.1.2[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:29:10 2025 +0700

    chore(release): manually fix and update version to v1.1.2
    
    - Update version in `app/__version__.py
    - synced version in `cz.toml`
    
    Changelog: handled separately

[33mcommit 9ef7b1f4a493fa11f6c7369a8e42ce537d174a91[m[33m ([m[1;33mtag: v0.0.1[m[33m)[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Fri Jul 25 11:11:17 2025 +0700

    fix(Makefile): correct commands and update documentation
    
    This commit fixes issues with Makefile command syntax and improves documentation for CLI usage and project structure.
    
    - Fixed broken or unclear `Makefile` commands
    - Updated `README.md` for clarity
    - Added CLI command docs to `docs/cli_commands_custy.md`
    - Modified `docs/project_structure.md`
    - Removed unnecessary `app/__init__.py` to silence warning
    - Updated `.gitignore` to ignore `commit-msg.txt` and allow `TODO.md`
    - Updated `.projectignore` to ignore `commit-msg.txt` and allow `TODO.md`
    - Added more documentation under `docs/versioningd/`
    
    Changelog: handled separately

[33mcommit 5741f8f5aa110c1b4da017f37a7cbaca1fa215da[m
Author: devalltect00 <rizkyslenovo29@gmail.com>
Date:   Thu Jul 24 21:12:26 2025 +0700

    Initial commit
