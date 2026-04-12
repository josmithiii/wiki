# Makefile for the LLM Wiki — build and deploy to CCRMA home page
#
# Targets:
#   make build   — render markdown sub-wikis to HTML in build/wiki/
#   make upload  — tar build/wiki and scp to CCRMA Web staging area
#                  (mirrors /w/scripts/webupd convention)
#   make clean   — remove build/
#
# At CCRMA, after running `make upload` from home, log in and run
#   webinst wiki
# to unpack into ~/Web/wiki and set permissions
# (see /w/scripts/webinst).

WIKI_NAME    := wiki
BUILD_DIR    := build
OUT_DIR      := $(BUILD_DIR)/$(WIKI_NAME)
TARBALL      := $(WIKI_NAME).tgz
BUILD_STAMP  := $(BUILD_DIR)/.BUILD_TIMESTAMP

# Sub-wikis to include (each is a top-level directory with SCHEMA.md/index.md/log.md)
SUBWIKIS     := waveguide_synthesis modal_synthesis

# Top-level files to include
TOPFILES     := README.md

# Pandoc options
PANDOC       := pandoc
PANDOC_OPTS  := --from=gfm --to=html5 --standalone --toc --toc-depth=2 \
                --metadata=lang:en --shift-heading-level-by=0 \
                --wrap=preserve

# CCRMA staging — matches /w/scripts/webupd convention
CCRMA_STAGE  := /w/h/josn

.PHONY: help all build rebuild html index render-md copy-md upload clean check

.DEFAULT_GOAL := help

help: ## Show this help (default target)
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

all: build ## Alias for build

# ---- Build ----

build: ## Render wiki to HTML (reuses existing build if present)
	@if [ -f $(BUILD_STAMP) ]; then \
	  echo "Build already present ($(BUILD_STAMP) — $$(date -r $(BUILD_STAMP)))."; \
	  echo "Run 'make rebuild' or 'make clean build' to force a rebuild."; \
	else \
	  $(MAKE) rebuild; \
	fi

rebuild: clean copy-md render-md index ## Force a clean rebuild
	@touch $(BUILD_STAMP)
	@echo ""
	@echo "Built $(OUT_DIR)"
	@echo "  Markdown sources: $(OUT_DIR)/**/*.md (Obsidian wikilinks preserved)"
	@echo "  Rendered HTML:    $(OUT_DIR)/**/*.html"
	@echo "  Top-level index:  $(OUT_DIR)/index.html"
	@echo "  Timestamp:        $(BUILD_STAMP)"
	@echo ""
	@echo "Next: make upload"

copy-md: ## Copy markdown sources into build dir
	@mkdir -p $(OUT_DIR)
	@for f in $(TOPFILES); do \
	  [ -f $$f ] && cp $$f $(OUT_DIR)/ || true; \
	done
	@for d in $(SUBWIKIS); do \
	  if [ -d $$d ]; then \
	    echo "  copying $$d/"; \
	    rsync -a --exclude='.obsidian' --exclude='raw' --exclude='_archive' \
	          --exclude='*.tex' --exclude='*.bash' \
	          --exclude='SCHEMA.md' --exclude='log.md' \
	          $$d/ $(OUT_DIR)/$$d/; \
	  fi; \
	done

render-md: copy-md ## Render markdown to HTML via pandoc
	@command -v $(PANDOC) >/dev/null 2>&1 || \
	  { echo "*** pandoc not found — install via: brew install pandoc"; exit 1; }
	@python3 scripts/build_wiki.py $(OUT_DIR) $(SUBWIKIS) || exit 1

index: ## Generate top-level index.html
	@python3 scripts/build_wiki_index.py $(OUT_DIR) $(SUBWIKIS) > $(OUT_DIR)/index.html

# ---- Upload ----

upload: build check ## Tar build and copy to CCRMA staging area
	@cd $(BUILD_DIR) && \
	tar --no-xattrs -czf $(TARBALL) $(WIKI_NAME) && \
	echo "Created $(BUILD_DIR)/$(TARBALL)"
	@if [ -d $(CCRMA_STAGE)/$(WIKI_NAME) ]; then \
	  cp $(BUILD_STAMP) $(CCRMA_STAGE)/$(WIKI_NAME)/.BUILD_TIMESTAMP && \
	  echo "Marked upload time in $(CCRMA_STAGE)/$(WIKI_NAME)/.BUILD_TIMESTAMP"; \
	fi
	@if [ -d $(CCRMA_STAGE) ]; then \
	  cp $(BUILD_DIR)/$(TARBALL) $(CCRMA_STAGE)/ && \
	  echo "Copied to $(CCRMA_STAGE)/$(TARBALL)"; \
	  /w/scripts/webupd $(WIKI_NAME).tgz \
	  echo "Ran webupd $(WIKI_NAME).tgz"; \
	  ssh ccrma-gate.stanford.edu webinst $(WIKI_NAME) \
	  echo "Ran webinst $(WIKI_NAME) at CCRMA - test it now"; \
	else \
	  echo ""; \
	  echo "$(CCRMA_STAGE) not found locally."; \
	  echo "Move $(BUILD_DIR)/$(TARBALL) to $(CCRMA_STAGE)/ and run:"; \
	  echo "  webupd $(WIKI_NAME).tgz"; \
	fi

check: ## Verify build dir exists
	@if [ ! -d $(OUT_DIR) ]; then \
	  echo "*** $(OUT_DIR) does not exist — run 'make build' first"; exit 1; \
	fi

clean: ## Remove build/ directory
	@rm -rf $(BUILD_DIR)
	@echo "Cleaned $(BUILD_DIR)/"
