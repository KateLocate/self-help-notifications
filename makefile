.PHONY: list-commands run 

list-commands:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | \
	awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | \
	grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'

run:
	@echo "~~~Running The Notification App~~~"
	docker compose up --build & cd src/notification_service && uv run fastapi dev main.py
