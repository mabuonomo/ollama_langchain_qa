DOCKER_EXEC:= docker compose exec ollama_chat_devcontainer

__start:
	docker compose up -d --remove-orphans

# control + D to exit
ollama_download_mistral: __start
	docker compose exec -it ollama_chat ollama run mistral  

run: __start
	$(DOCKER_EXEC) python src/test.multidocument.py

bash: __start
	$(DOCKER_EXEC) bash