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

# Sub-wikis to include (each is a top-level directory with SCHEMA.md/index.md/log.md)
SUBWIKIS     := modal_synthesis waveguide_synthesis projects

# Top-level files to include
TOPFILES     := README.md

# Pandoc options
PANDOC       := pandoc
PANDOC_OPTS  := --from=gfm --to=html5 --standalone --toc --toc-depth=2 \
                --metadata=lang:en --shift-heading-level-by=0 \
                --wrap=preserve

# CCRMA staging — matches /w/scripts/webupd convention
CCRMA_STAGE  := /w/h/josn

.PHONY: all build html index render-md copy-md upload clean check

all: build

# ---- Build ----

build: clean copy-md render-md index
	@echo ""
	@echo "Built $(OUT_DIR)"
	@echo "  Markdown sources: $(OUT_DIR)/**/*.md (Obsidian wikilinks preserved)"
	@echo "  Rendered HTML:    $(OUT_DIR)/**/*.html"
	@echo "  Top-level index:  $(OUT_DIR)/index.html"
	@echo ""
	@echo "Next: make upload"

copy-md:
	@mkdir -p $(OUT_DIR)
	@for f in $(TOPFILES); do \
	  [ -f $$f ] && cp $$f $(OUT_DIR)/ || true; \
	done
	@for d in $(SUBWIKIS); do \
	  if [ -d $$d ]; then \
	    echo "  copying $$d/"; \
	    rsync -a --exclude='.obsidian' --exclude='raw' --exclude='_archive' \
	          --exclude='*.tex' --exclude='*.bash' \
	          $$d/ $(OUT_DIR)/$$d/; \
	  fi; \
	done

render-md: copy-md
	@command -v $(PANDOC) >/dev/null 2>&1 || \
	  { echo "*** pandoc not found — install via: brew install pandoc"; exit 1; }
	@python3 scripts/build_wiki.py $(OUT_DIR) $(SUBWIKIS) || exit 1

index:
	@python3 scripts/build_wiki_index.py $(OUT_DIR) $(SUBWIKIS) > $(OUT_DIR)/index.html

# ---- Upload ----

upload: build check
	@cd $(BUILD_DIR) && \
	tar --no-xattrs -czf $(TARBALL) $(WIKI_NAME) && \
	echo "Created $(BUILD_DIR)/$(TARBALL)"
	@if [ -d $(CCRMA_STAGE) ]; then \
	  cp $(BUILD_DIR)/$(TARBALL) $(CCRMA_STAGE)/ && \
	  echo "Copied to $(CCRMA_STAGE)/$(TARBALL) — now run: webupd $(WIKI_NAME)"; \
	else \
	  echo ""; \
	  echo "$(CCRMA_STAGE) not found locally."; \
	  echo "Move $(BUILD_DIR)/$(TARBALL) to $(CCRMA_STAGE)/ and run:"; \
	  echo "  webupd $(WIKI_NAME)"; \
	fi

check:
	@if [ ! -d $(OUT_DIR) ]; then \
	  echo "*** $(OUT_DIR) does not exist — run 'make build' first"; exit 1; \
	fi

clean:
	@rm -rf $(BUILD_DIR)
	@echo "Cleaned $(BUILD_DIR)/"
