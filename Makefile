.PHONY: run-main \
            structure \
            lint-ruff lint-ruff-fix format-ruff format-black format-all \
            git-current-branch git-origin-url git-log git-log-tag \
            generate_ignore_files \
            custy-all-major custy-all-minor custy-all-patch  \
            custy-all-alpha custy-all-major-alpha custy-all-minor-alpha custy-all-patch-alpha \
            custy-all-beta custy-all-major-beta custy-all-minor-beta custy-all-patch-beta \
            custy-all-rc custy-all-major-rc custy-all-minor-rc custy-all-patch-rc \
            custy-all-dev custy-all-major-dev custy-all-minor-dev custy-all-patch-dev \
            custy-all-next custy-all-major-next custy-all-minor-next custy-all-patch-next \
            custy-all-preview custy-all-major-preview custy-all-minor-preview custy-all-patch-preview \
            custy-changelog custy-validate custy-push custy-backup

# -----------------------------
# 🔧 variables
# -----------------------------
COMMIT_MESSAGE_FILE_PATH = templates\commit-msg.txt
TAG_COMMIT_MESSAGE_FILE_PATH = templates\tag-msg.txt
APP = app
# APP = app.debug_tag_release_notes

# -----------------------------
# 🚀 Main Applicattion Commands
# -----------------------------

# Example if force commit
# python -m app all templates\commit-msg.txt --tag-msg-file templates\tag-msg.txt --bump minor --force-commit
#
# Example to run the debug version
# python -m app.debug_tag_release_notes all templates\commit-msg.txt --tag-msg-file templates\tag-msg.txt --bump patch
# python -m app all templates\commit-msg.txt --tag-msg-file templates\tag-msg.txt --bump patch --sync-backup --no-debug

run-main:
	python -m $(APP)

custy-all-major:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --sync-backup --no-debug

custy-all-minor:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --sync-backup --no-debug

custy-all-patch:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --sync-backup --no-debug

custy-all-release:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --sync-backup --no-debug

custy-all-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release alpha --sync-backup --no-debug

custy-all-major-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release alpha --sync-backup --no-debug

custy-all-minor-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release alpha --sync-backup --no-debug

custy-all-patch-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release alpha --sync-backup --no-debug

custy-all-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release beta --sync-backup --no-debug

custy-all-major-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release beta --sync-backup --no-debug

custy-all-minor-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release beta --sync-backup --no-debug

custy-all-patch-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release beta --sync-backup --no-debug

custy-all-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release rc --sync-backup --no-debug

custy-all-major-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release rc --sync-backup --no-debug

custy-all-minor-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release rc --sync-backup --no-debug

custy-all-patch-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release rc --sync-backup --no-debug

custy-all-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release dev --sync-backup --no-debug

custy-all-major-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release dev --sync-backup --no-debug

custy-all-minor-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release dev --sync-backup --no-debug

custy-all-patch-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release dev --sync-backup --no-debug

custy-all-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release next --sync-backup --no-debug

custy-all-major-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release next --sync-backup --no-debug

custy-all-minor-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release next --sync-backup --no-debug

custy-all-patch-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release next --sync-backup --no-debug

custy-all-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --pre-release preview --sync-backup --no-debug

custy-all-major-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release preview --sync-backup --no-debug

custy-all-minor-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release preview --sync-backup --no-debug

custy-all-patch-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release preview --sync-backup --no-debug

custy-all-post:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --post-release --sync-backup --no-debug

custy-all-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --dev-release --sync-backup --no-debug

custy-changelog:
	python -m $(APP) changelog --force-changelog --sync-backup --no-debug

custy-validate:
	python -m $(APP) validate

custy-push:
	python -m $(APP) push

custy-backup:
	python -m $(APP) backup

# -----------------------------
# 🧼 Code formating
# -----------------------------
# Format code with ruff (optionally)
lint-ruff:
	ruff check app tools

lint-ruff-fix:
	ruff check app tools --fix

format-ruff:
	ruff format app tools

format-all: lint-ruff lint-ruff-fix format-ruff

# ----------------------------------------------------------
# ⚙️ Custom Tools (Generate Ignore Files)
# ----------------------------------------------------------

generate_ignore_files:
	python -m tools.generate_ignore.generate_ignore_files

# ----------------------------------------------------------
# 🧱 Custom Tools (Project Structure)
# ----------------------------------------------------------
structure:
	py -m tools.project_structure.print_project_structure

# -----------------------------
# ⚙️ Tools Git
# -----------------------------
git-current-branch:
	git branch --show-current

git-origin-url:
	git remote get-url origin

git-log:
	git log --oneline --graph --decorate --all -n 25

git-log-tag:
	git log --no-walk --tags --pretty="format:%h %d %s"

# -----------------------------
# 🆘 Help
# -----------------------------
help:
	@echo "Available targets:"
	@findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile

# @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFI=LE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1. $$2}'
# @findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile | findstr /V ":" | sort
