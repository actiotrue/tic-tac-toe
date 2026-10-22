.PHONY: dev local migrate

dev:
	docker compose up -d redis
	cd services/api-service && uv run uvicorn app.main:app --reload &\
	cd services/socket-server && go run cmd/server/main.go &\
	cd frontend && bun dev & \
	wait

local:
	cd services/api-service && uv run uvicorn app.main:app --reload &\
	cd services/socket-server && go run cmd/server/main.go &\
	cd frontend && bun dev & \
	wait

migrate:
	@which dbmate >/dev/null 2>&1 || (echo "Dbmate not install";exit 1)
	@echo "Migrating..."
	cd services/api-service && dbmate --env-file "../../.env" up