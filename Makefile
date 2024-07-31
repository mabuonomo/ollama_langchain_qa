DOCKER_PYTHON_EXEC:= docker compose exec qa_ollama_python
DOCKER_CHAT_EXEC:= docker compose exec qa_ollama_server

__start:
	docker compose up -d --remove-orphans

run: __start
	${DOCKER_PYTHON_EXEC} python src/test.multidocument.py

bash: __start
	$(DOCKER_PYTHON_EXEC) bash

setup: __start
	${DOCKER_CHAT_EXEC} ollama pull llama3.1
	${DOCKER_PYTHON_EXEC} pip install --no-cache-dir -r src/requirements.txt