.PHONY: run-main \
            structure \
            lint-ruff lint-ruff-fix format-ruff format-black format-all \
            git-current-branch git-origin-url \
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

# -----------------------------
# 🚀 Main Applicattion Commands
# -----------------------------

run-main:
	python -m app

custy-all-major:
	python -m app all --bump major $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor:
	python -m app all --bump minor $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch:
	python -m app all --bump patch $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-alpha:
	python -m app all --bump major --pre-release alpha $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-alpha:
	python -m app all --bump minor --pre-release alpha $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-alpha:
	python -m app all --bump patch --pre-release alpha $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-beta:
	python -m app all --bump major --pre-release beta $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-beta:
	python -m app all --bump minor --pre-release beta $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-beta:
	python -m app all --bump patch --pre-release beta $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-rc:
	python -m app all --bump major --pre-release rc $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-rc:
	python -m app all --bump minor --pre-release rc $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-rc:
	python -m app all --bump patch --pre-release rc $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-dev:
	python -m app all --bump major --pre-release dev $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-dev:
	python -m app all --bump minor --pre-release dev $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-dev:
	python -m app all --bump patch --pre-release dev $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-next:
	python -m app all --bump major --pre-release next $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-next:
	python -m app all --bump minor --pre-release next $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-next:
	python -m app all --bump patch --pre-release next $(COMMIT_MESSAGE_FILE_PATH)

custy-all-major-preview:
	python -m app all --bump major --pre-release preview $(COMMIT_MESSAGE_FILE_PATH)

custy-all-minor-preview:
	python -m app all --bump minor --pre-release preview $(COMMIT_MESSAGE_FILE_PATH)

custy-all-patch-preview:
	python -m app all --bump patch --pre-release preview $(COMMIT_MESSAGE_FILE_PATH)

custy-changelog:
	python -m app changelog

custy-validate:
	python -m app validate

custy-push:
	python -m app push

custy-backup:
	python -m app backup

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

# -----------------------------
# 🆘 Help
# -----------------------------
help:
	@echo "Available targets:"
	@findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile

# @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFI=LE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1. $$2}'
# @findstr /B /R "^[a-zA-Z0-9_-]*:" Makefile | findstr /V ":" | sort
