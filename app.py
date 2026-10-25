import os
import gradio as gr
from huggingface_hub import InferenceClient

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=os.environ.get("HF_TOKEN"))

SYSTEM_PROMPT = """
Tu és a Zure IA, criada pela PLEE UNIVERSE
e INÁCIO.U.DANIEL.

O teu nome é Zure IA.
Quando perguntarem quem te criou, identifica
a PLEE UNIVERSE e INÁCIO.U.DANIEL.
Responde em português por padrão.
Sê simpática, clara, útil e respeitosa.
Ajuda com programação, estudos, escrita e tecnologia.
Não inventes informações quando não souberes a resposta.
"""

print("Zure IA configurada com API Serverless...")


def responder(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return "Olá! Sou a Zure IA. Como posso ajudar-te?"

    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}]

    for item in (historico or [])[-8:]:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and content:
                mensagens.append({"role": role, "content": content})
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            mensagens.append({"role": "user", "content": item[0]})
            mensagens.append({"role": "assistant", "content": item[1]})

    mensagens.append({"role": "user", "content": mensagem.strip()})

    try:
        resposta_completa = ""
        for message in client.chat_completion(
            messages=mensagens,
            max_tokens=250,
            stream=True,
            temperature=0.7,
            top_p=0.9,
            model=MODEL_ID,
        ):
            token = message.choices[0].delta.content
            if token:
                resposta_completa += token

        return resposta_completa or "Não consegui gerar uma resposta. Tenta novamente."

    except Exception as erro:
        print(f"Erro na API: {erro}")
        return "A Zure IA está temporariamente indisponível. Tenta novamente em alguns instantes."


CSS = """
.gradio-container {
    max-width: 1000px !important;
    margin: auto !important;
}
"""

with gr.Blocks(
    title="Zure IA",
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="blue"
    ),
    css=CSS
) as app:

    gr.Markdown("""
    # 🤖 Zure IA

    ### A tua inteligência artificial

    Criada pela **PLEE UNIVERSE** e **INÁCIO.U.DANIEL**.

    Pergunta, aprende, programa e cria.
    """)

    gr.ChatInterface(
        fn=responder,
        chatbot=gr.Chatbot(height=480),
        textbox=gr.Textbox(
            placeholder="Escreve uma mensagem para a Zure IA...",
            lines=2
        ),
        type="messages",
        examples=[
            "Olá, quem és tu?",
            "Quem criou a Zure IA?",
            "Ensina-me Python",
            "Ajuda-me a criar um site"
        ]
    )

    gr.Markdown("""
    ---
    *Zure IA © PLEE UNIVERSE e INÁCIO.U.DANIEL*
    """)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)
