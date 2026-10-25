# Zure IA

Aplicação Gradio para chatbot com modelo serverless da Hugging Face, pronta para deploy na Render.

## Estrutura

- `app.py`: interface Gradio + integração com Hugging Face Inference API
- `requirements.txt`: dependências mínimas para o deploy
- `README.md`: documentação do projeto

## Como funciona

A aplicação usa `huggingface_hub.InferenceClient` para enviar as mensagens para um modelo serverless gratuito da Hugging Face, evitando o consumo pesado de RAM na Render.

## Deploy na Render

1. Faça push deste repositório para o GitHub.
2. Crie um novo Web Service na Render.
3. Conecte este repositório.
4. Defina o comando de inicialização: `python app.py`
5. Garanta que a variável de ambiente `PORT` é usada automaticamente pela Render.
6. Opcional: adicione `HF_TOKEN` nas variáveis de ambiente para reduzir limites do modelo gratuito.

## Executar localmente

```bash
pip install -r requirements.txt
python app.py
```

A aplicação ficará disponível em `http://localhost:7860`.
