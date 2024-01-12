# Ollama QA - Fully dockerized with Nvidia GPU support

## Summary

A document-oriented chatbot is an interactive system designed to respond to user inquiries about various types of documents. This chatbot employs an advanced language model to understand user queries and then searches the specified document repository for relevant information. The system leverages the Retrieval-Augmented Generation (RAG) approach to generate contextually appropriate responses. By combining generative capabilities with information retrieval from an external knowledge base, this chatbot is able to provide more informative and comprehensive answers across a diverse range of document-related prompts and questions.

## 🚦Why Ollama?

Ollama empowers users to locally execute open-source large language models like Llama 2 and Mistral AI. It consolidates model weights, configuration, and data into a unified package known as a Modelfile. This streamlines the setup process and handles configuration intricacies, including efficient GPU utilization. Refer to the Ollama model library for an exhaustive compilation of supported models and their variants.

Credits to [Ollama](https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image).

## 📝 Nvidia CUDA

CUDA is a platform and programming model by NVIDIA to tap into the computational power of GPUs. Key features include extending standard programming languages, supporting CPU-GPU heterogeneous computing, incremental application to existing code, separate CPU and GPU memory spaces, utilizing multiple cores for simultaneous thread execution, and sharing resources among cores to enhance parallel processing efficiency.

Credits to [NVIDIA](https://developer.nvidia.com/cuda-zone) for the CUDA.

## 📦 Requirements

* [Docker](https://docs.docker.com/get-docker/)
* [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.14.3/install-guide.html)

## 🚀 Getting started

Clone the repository, install (download model and install the requirements for python) and run

```
make setup
```

## 🚶Start

Initiate the multi-document chatbot and begin engaging with your files. Deposit any files you wish to interact with into the /docs directory. To exit the prompt at any point, enter q.

```python
make run
```

## 📝 References

* [Ollama](https://ollama.ai/blog/ollama-is-now-available-as-an-official-docker-image)
* [NVIDIA](https://developer.nvidia.com/cuda-zone)
* [Docker](https://docs.docker.com/get-docker/)
* [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.14.3/install-guide.html)
* [Mistral AI](https://mistral.ai/news/mixtral-of-experts/)
