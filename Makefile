.POSIX:

# default to opening in browser
all: view

# create db from schema
create:
	./scripts/create.sh

# open db
open:
	./scripts/open.sh

# view data in browser
view:
	./scripts/view.sh

# full end-to-end demo
demo:
	./scripts/demo.sh

.PHONY: all create open view demo

