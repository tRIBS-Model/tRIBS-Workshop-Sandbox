#!/usr/bin/env bash
# Enable the notebook clean filter for this clone. Run once after cloning.
#
# Git filters are configured per-clone (.gitattributes alone is not enough),
# so this cannot be committed as "already on". Clones that skip it get the
# unfiltered behavior, nothing breaks.
# To enable the filter run: bash tools/setup-git-filters.sh
set -euo pipefail

repo_root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$repo_root"

git config filter.nbclean.clean "python3 tools/clean_notebook.py"
git config filter.nbclean.smudge cat
git config filter.nbclean.required false

echo "Notebook clean filter enabled for $repo_root"
