DOCKER_PYTHON_EXEC:= docker compose exec ollama_chat_devcontainer
DOCKER_CHAT_EXEC:= docker compose exec ollama_chat

__start:
	docker compose up -d --remove-orphans

run: __start
	${DOCKER_CHAT_EXEC} ollama pull mistral
	${DOCKER_PYTHON_EXEC} python src/test.multidocument.py

bash: __start
	$(DOCKER_PYTHON_EXEC) bash