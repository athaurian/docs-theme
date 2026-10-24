# Copy the theme into each site checkout, and report drift without writing.

SITES ?= $(HOME)/Projects/github/athaurian/calpdf $(HOME)/.local/share/chezmoi

.PHONY: sync check favicons

sync:
	@for site in $(SITES); do \
		install -D -m 644 stylesheets/extra.css $$site/docs/stylesheets/extra.css; \
		install -D -m 644 overrides/home.html $$site/overrides/home.html; \
		install -D -m 644 overrides/main.html $$site/overrides/main.html; \
		install -D -m 644 javascripts/theme-transition.js $$site/docs/javascripts/theme-transition.js; \
		printf 'synced %s\n' "$$site"; \
	done

favicons:
	@set -eu; \
	tmp=$$(mktemp -d); \
	trap 'rm -rf "$$tmp"' EXIT; \
	for site in $(SITES); do \
		svg=$$site/docs/favicon.svg; \
		test -f "$$svg" || { printf 'missing %s\n' "$$svg" >&2; exit 1; }; \
		rsvg-convert -w 32 -h 32 "$$svg" -o "$$site/docs/favicon-32x32.png"; \
		rsvg-convert -w 192 -h 192 "$$svg" -o "$$site/docs/favicon-192x192.png"; \
		rsvg-convert -w 180 -h 180 --background-color='#121212' "$$svg" -o "$$site/docs/apple-touch-icon.png"; \
		for size in 16 32 48 64; do \
			rsvg-convert -w $$size -h $$size "$$svg" -o "$$tmp/$$size.png"; \
		done; \
		magick "$$tmp/16.png" "$$tmp/32.png" "$$tmp/48.png" "$$tmp/64.png" "$$site/docs/favicon.ico"; \
		printf 'generated favicons for %s\n' "$$site"; \
	done

check:
	@status=0; \
	for site in $(SITES); do \
		diff -u stylesheets/extra.css $$site/docs/stylesheets/extra.css || status=1; \
		diff -u overrides/home.html $$site/overrides/home.html || status=1; \
		diff -u overrides/main.html $$site/overrides/main.html || status=1; \
		diff -u javascripts/theme-transition.js $$site/docs/javascripts/theme-transition.js || status=1; \
		for file in favicon.ico favicon-32x32.png favicon-192x192.png apple-touch-icon.png; do \
			test -f $$site/docs/$$file || { printf 'missing %s/docs/%s (run make favicons)\n' "$$site" "$$file" >&2; status=1; }; \
		done; \
	done; \
	exit $$status
