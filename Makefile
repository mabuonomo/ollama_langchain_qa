DOCKER_EXEC:= docker compose exec cowtechgo_chat_devcontainer

__start:
	docker compose up -d --remove-orphans

# control + D to exit
ollama_download_mistral: __start
	docker compose exec -it cowtechgo_chat_ollama ollama run mistral  

run:
	$(DOCKER_EXEC) python src/app.py

run_test1: __start
	$(DOCKER_EXEC) python src/test.singledocument.py

run_test2: __start
	$(DOCKER_EXEC) python src/test.multidocument.py

bash: __start
	$(DOCKER_EXEC) bash