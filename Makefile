.PHONY: run-main \
            structure \
            lint-ruff lint-ruff-fix format-ruff format-black format-all \
            git-current-branch git-origin-url git-show-log git-show-log-tag \
            generate_ignore_files \
            custy-all-major custy-all-minor custy-all-patch  \
            custy-all-major-alpha custy-all-minor-alpha custy-all-patch-alpha \
            custy-all-major-beta custy-all-minor-beta custy-all-patch-beta \
            custy-all-major-rc custy-all-minor-rc custy-all-patch-rc \
            custy-all-major-dev custy-all-minor-dev custy-all-patch-dev \
            custy-all-major-next custy-all-minor-next custy-all-patch-next \
            custy-all-major-preview custy-all-minor-preview custy-all-patch-preview \
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

run-main:
	python -m $(APP)

custy-all-major:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major

custy-all-minor:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor

custy-all-patch:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch

custy-all-major-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release alpha

custy-all-minor-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release alpha

custy-all-patch-alpha:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release alpha

custy-all-major-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release beta

custy-all-minor-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release beta

custy-all-patch-beta:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release beta

custy-all-major-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release rc

custy-all-minor-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release rc

custy-all-patch-rc:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release rc

custy-all-major-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release dev

custy-all-minor-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release dev

custy-all-patch-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release dev

custy-all-major-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release next

custy-all-minor-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release next

custy-all-patch-next:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release next

custy-all-major-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump major --pre-release preview

custy-all-minor-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump minor --pre-release preview

custy-all-patch-preview:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --pre-release preview

custy-all-post:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --post-release

custy-all-dev:
	python -m $(APP) all $(COMMIT_MESSAGE_FILE_PATH) --tag-msg-file $(TAG_COMMIT_MESSAGE_FILE_PATH) --bump patch --dev-release

custy-changelog:
	python -m $(APP) changelog

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

git-show-log:
	git log --oneline --graph --decorate --all

git-show-log-tag:
	git log --no-walk --tags --pretty="format:%h %d %s"

# -----------------------------
# 🆘 Help
# -----------------------------
help:
	@echo "Available targets:"
	@findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile

# @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFI=LE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1. $$2}'
# @findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile | findstr /V ":" | sort
