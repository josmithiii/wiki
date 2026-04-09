#!/usr/bin/env bash
# Sync the modal_synthesis wiki to the 423gl course site.
# Excludes raw/ (copyrighted sources) and log.md (agent bookkeeping).
set -euo pipefail

SRC="$(dirname "$0")/"
DEST="/l/423gl/modal-synthesis/wiki/"

rsync -av --delete --exclude='raw/' --exclude='log.md' --exclude='sync-to-423gl.bash' "$SRC" "$DEST"

# Convert [[wikilinks]] to standard markdown links for GitLab rendering.
# The source wiki keeps wikilinks (for Obsidian); only the destination is converted.
python3 -c "
import re, os, glob

WIKI_DIR = '$DEST'

existing = {}
for path in glob.glob(f'{WIKI_DIR}/**/*.md', recursive=True):
    bare = os.path.splitext(os.path.basename(path))[0]
    existing[bare] = os.path.relpath(path, WIKI_DIR)

def resolve(target, source_dir):
    target = target.strip()
    if target in existing:
        return os.path.relpath(os.path.join(WIKI_DIR, existing[target]), source_dir)
    return os.path.relpath(os.path.join(WIKI_DIR, target + '.md'), source_dir)

for path in glob.glob(f'{WIKI_DIR}/**/*.md', recursive=True):
    with open(path) as f:
        content = f.read()
    if '[[' not in content:
        continue
    def replace_link(m, sd=os.path.dirname(path)):
        inner = m.group(1)
        target, display = inner.split('|', 1) if '|' in inner else (inner, inner)
        return f'[{display}]({resolve(target, sd)})'
    new = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
    if new != content:
        with open(path, 'w') as f:
            f.write(new)
        print(f'  Converted wikilinks: {os.path.relpath(path, WIKI_DIR)}')
"

# Strip raw/ references from sources: frontmatter (raw files aren't exported).
# Keeps only URL sources.
python3 -c "
import re, os, glob

WIKI_DIR = '$DEST'

for path in glob.glob(f'{WIKI_DIR}/**/*.md', recursive=True):
    with open(path) as f:
        content = f.read()
    # Remove '  - raw/...' lines from sources frontmatter
    new = re.sub(r'\n  - raw/[^\n]*', '', content)
    # Clean up sources: [] if now empty
    new = re.sub(r'sources:\n(?=\w|\Z|---)', 'sources: []\n', new)
    if new != content:
        with open(path, 'w') as f:
            f.write(new)
        print(f'  Stripped raw refs: {os.path.relpath(path, WIKI_DIR)}')
"

echo "Synced and converted to $DEST"
