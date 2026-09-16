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
SRC_DIR = os.path.abspath('$SRC')
SRC_ROOT = os.path.dirname(SRC_DIR)
GITHUB = 'https://github.com/josmithiii/wiki/blob/main/'

existing = {}
for path in glob.glob(f'{WIKI_DIR}/**/*.md', recursive=True):
    bare = os.path.splitext(os.path.basename(path))[0]
    existing[bare] = os.path.relpath(path, WIKI_DIR)

def resolve(target, source_dir):
    # [[page]], [[dir/page]], [[page#anchor]] -> relative path to page.md (+ #anchor)
    target, anchor = (target.strip().split('#', 1) + [''])[:2]
    anchor = ('#' + anchor) if anchor else ''
    bare = os.path.basename(target)
    if bare in existing:
        rel = existing[bare]
    else:
        # Page lives in a sibling sub-wiki (e.g. waveguide_synthesis)? Point at GitHub.
        hits = [h for h in glob.glob(f'{SRC_ROOT}/*/**/{bare}.md', recursive=True)
                if '/raw/' not in h and not h.startswith(SRC_DIR)]
        if hits:
            return GITHUB + os.path.relpath(hits[0], SRC_ROOT) + anchor
        rel = target + '.md'
    return os.path.relpath(os.path.join(WIKI_DIR, rel), source_dir) + anchor

for path in glob.glob(f'{WIKI_DIR}/**/*.md', recursive=True):
    with open(path) as f:
        content = f.read()
    if '[[' not in content:
        continue
    def replace_link(m, sd=os.path.dirname(path)):
        inner = m.group(1)
        target, display = inner.split('|', 1) if '|' in inner else (inner, inner)
        return f'[{display}]({resolve(target, sd)})'
    # Leave literal mentions inside backticks (e.g. SCHEMA.md's \`[[wikilinks]]\`) alone.
    new = re.sub(r'(?<!\`)\[\[([^\]]+)\]\](?!\`)', replace_link, content)
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
    new = re.sub(r'\n  - (~/wiki/[^\n]*/)?raw/[^\n]*', '', content)
    # Clean up sources: [] if now empty
    new = re.sub(r'sources:\n(?=\w|\Z|---)', 'sources: []\n', new)
    if new != content:
        with open(path, 'w') as f:
            f.write(new)
        print(f'  Stripped raw refs: {os.path.relpath(path, WIKI_DIR)}')
"

echo "Synced and converted to $DEST"
