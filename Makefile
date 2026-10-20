# Copy the theme into each site checkout, and report drift without writing.

SITES ?= $(HOME)/Projects/github/athaurian/calpdf $(HOME)/.local/share/chezmoi

.PHONY: sync check

sync:
	@for site in $(SITES); do \
		install -D -m 644 stylesheets/extra.css $$site/docs/stylesheets/extra.css; \
		install -D -m 644 overrides/home.html $$site/overrides/home.html; \
		install -D -m 644 overrides/main.html $$site/overrides/main.html; \
		install -D -m 644 javascripts/theme-transition.js $$site/docs/javascripts/theme-transition.js; \
		printf 'synced %s\n' "$$site"; \
	done

check:
	@status=0; \
	for site in $(SITES); do \
		diff -u stylesheets/extra.css $$site/docs/stylesheets/extra.css || status=1; \
		diff -u overrides/home.html $$site/overrides/home.html || status=1; \
		diff -u overrides/main.html $$site/overrides/main.html || status=1; \
		diff -u javascripts/theme-transition.js $$site/docs/javascripts/theme-transition.js || status=1; \
	done; \
	exit $$status
