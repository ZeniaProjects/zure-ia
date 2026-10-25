import os
from flask import Flask, request, jsonify, render_template_string
from huggingface_hub import InferenceClient

app = Flask(__name__)
MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"
client = InferenceClient(token=os.environ.get("HF_TOKEN"))

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

HTML_PAGE = """
<!doctype html>
<html lang="pt">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Zure IA</title>
  <style>
    :root {
      --bg: #0f172a;
      --panel: #111827;
      --panel-2: #1f2937;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #8b5cf6;
      --accent-2: #3b82f6;
      --user: #312e81;
      --bot: #1f2937;
      --border: rgba(255,255,255,0.08);
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; height: 100%; font-family: Arial, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); color: var(--text); }
    body { display: flex; justify-content: center; padding: 30px 12px; }
    .app { width: min(980px, 100%); }
    .header {
      padding: 20px 22px; border-radius: 22px 22px 0 0; background: rgba(17,24,39,0.92);
      border: 1px solid var(--border); border-bottom: none;
    }
    h1 { margin: 0; font-size: clamp(1.8rem, 3vw, 2.5rem); }
    .subtitle { color: var(--muted); margin-top: 8px; }
    .chat {
      background: rgba(17,24,39,0.96); border: 1px solid var(--border); border-top: none;
      min-height: 520px; max-height: 64vh; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 14px;
    }
    .msg {
      max-width: 75%; padding: 12px 14px; border-radius: 16px; line-height: 1.5; white-space: pre-wrap;
      word-wrap: break-word; border: 1px solid var(--border);
    }
    .user { align-self: flex-end; background: var(--user); }
    .bot { align-self: flex-start; background: var(--bot); }
    .composer {
      display: flex; gap: 10px; padding: 18px; background: rgba(17,24,39,0.96); border: 1px solid var(--border);
      border-radius: 0 0 22px 22px; border-top: none;
    }
    textarea {
      flex: 1; min-height: 52px; max-height: 180px; resize: vertical; border-radius: 14px; border: 1px solid var(--border);
      background: var(--panel-2); color: var(--text); padding: 12px 14px; font-size: 1rem;
    }
    button {
      border: none; border-radius: 14px; background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: white; font-weight: 700; padding: 0 22px; min-width: 120px; cursor: pointer;
    }
    button:hover { filter: brightness(1.06); }
    .badge { display: inline-block; padding: 6px 10px; border-radius: 999px; background: rgba(139,92,246,0.15); color: #d8b4fe; border: 1px solid rgba(139,92,246,.35); font-size: 12px; }
    @media (max-width: 640px) {
      .msg { max-width: 90%; }
      .composer { flex-direction: column; }
      button { min-height: 46px; }
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="header">
      <div class="badge">PLEE UNIVERSE • INÁCIO.U.DANIEL</div>
      <h1>Zure IA</h1>
      <div class="subtitle">Sua inteligência artificial em português, leve, estável e pronta para Render.</div>
    </div>

    <div id="chat" class="chat" aria-live="polite"></div>

    <div class="composer">
      <textarea id="message" rows="2" placeholder="Escreve uma mensagem para a Zure IA..."></textarea>
      <button id="sendBtn">Enviar</button>
    </div>
  </div>

  <script>
    const chat = document.getElementById('chat');
    const textarea = document.getElementById('message');
    const button = document.getElementById('sendBtn');
    const history = [];

    function addMessage(role, text) {
      const el = document.createElement('div');
      el.className = 'msg ' + (role === 'user' ? 'user' : 'bot');
      el.textContent = text;
      chat.appendChild(el);
      chat.scrollTop = chat.scrollHeight;
    }

    function send() {
      const text = textarea.value.trim();
      if (!text) return;

      addMessage('user', text);
      textarea.value = '';
      button.disabled = true;
      button.textContent = 'Pensando...';

      history.push({ role: 'user', content: text });

      fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: history })
      })
      .then(async r => {
        const data = await r.json();
        const reply = data.reply || 'Não consegui gerar uma resposta.';
        addMessage('bot', reply);
        history.push({ role: 'assistant', content: reply });
      })
      .catch(() => {
        addMessage('bot', 'A Zure IA está temporariamente indisponível. Tenta novamente.');
      })
      .finally(() => {
        button.disabled = false;
        button.textContent = 'Enviar';
      });
    }

    button.addEventListener('click', send);
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        send();
      }
    });

    addMessage('bot', 'Olá! Sou a Zure IA. Como posso ajudar-te?');
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(HTML_PAGE)


@app.post("/api/chat")
def api_chat():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()
    history = payload.get("history") or []

    if not user_message:
        return jsonify({"reply": "Olá! Sou a Zure IA. Como posso ajudar-te?"})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for item in (history or [])[-8:]:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat_completion(
            messages=messages,
            model=MODEL_ID,
            max_tokens=220,
            temperature=0.7,
            top_p=0.9,
        )

        if hasattr(response, "choices"):
            choice = response.choices[0]
            message = getattr(choice, "message", None)
            if message is not None:
                content = getattr(message, "content", "")
                if isinstance(content, list):
                    content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
                reply = content or "Não consegui gerar uma resposta. Tenta novamente."
            else:
                reply = getattr(choice, "text", "") or "Não consegui gerar uma resposta. Tenta novamente."
        else:
            reply = "Não consegui gerar uma resposta. Tenta novamente."

        return jsonify({"reply": reply.strip() or "Não consegui gerar uma resposta. Tenta novamente."})

    except Exception as erro:
        print(f"Erro na API: {erro}")
        return jsonify({"reply": "A Zure IA está temporariamente indisponível. Tenta novamente em alguns instantes."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
