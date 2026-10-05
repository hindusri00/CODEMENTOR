# 🧑‍💻 Code Mentor

**An AI coding assistant for beginners that teaches you to understand your Java code instead of just rewriting it.**

Paste or upload Java code and Code Mentor tells you *what the problem is*, *why it happens*, *what to try next*, and *which computer-science concepts are involved*. Students choose how much help they want, from a small nudge to a code sketch.

```
🔍 Code Analysis

Problem:
Your loop has O(n²) time complexity.

Why?
The inner loop executes for every element of the outer loop.

Suggestion:
Consider using a HashMap.

Concepts involved:
→ Time Complexity
→ Hashing
```

## Features
- **Static analysis** of Java using an AST parser (nested loops, `contains()` in loops, String `+=` in loops, `==` on Strings, recursion)
- **RAG**: retrieves relevant teaching notes from a knowledge base to ground explanations
- **Prompt-engineered LLM** that teaches rather than solves, with **3 hint levels**
- **Multi-provider**: free options (Gemini, Groq, OpenRouter, Ollama) plus Anthropic
- "Check yourself" question after each analysis to reinforce learning
- Streamlit web UI with file upload or paste

## Tech stack
Python · Streamlit · javalang · scikit-learn (TF-IDF) · OpenAI-compatible LLM APIs / Anthropic SDK

## Getting started
```bash
git clone https://github.com/<your-username>/code-mentor.git
cd code-mentor
python -m venv .venv
# Windows: .venv\Scripts\activate    |  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # Windows: copy .env.example .env
```
Edit `.env`, choose a provider and add its key, for example:
```
LLM_PROVIDER=groq
GROQ_API_KEY=your-key
```
Then run:
```bash
streamlit run app.py
```
Try the sample in `samples/TwoSum.java`.

## Free API keys
| Provider | Link |
|---|---|
| Google Gemini | https://aistudio.google.com |
| Groq | https://console.groq.com |
| OpenRouter | https://openrouter.ai |
| Ollama (local) | https://ollama.com |

## Project structure
```
code-mentor/
├── app.py          # Streamlit UI
├── pipeline.py     # Orchestrates analysis -> retrieval -> LLM
├── analyzer.py     # Static Java analysis
├── rag.py          # Knowledge-base retrieval
├── llm.py          # Provider-agnostic LLM client
├── prompts.py      # System prompt and prompt builder
├── knowledge/      # Teaching notes (one concept per .md file)
├── samples/        # Example Java programs
└── docs/PROJECT_DOCUMENTATION.md
```
See [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md) for how everything works.

## Roadmap
- Embedding-based retrieval
- Evaluation set for retrieval and explanation quality
- Follow-up chat
- Support for Python and C++

## Security
Never commit `.env`. It is listed in `.gitignore`. If a key is ever exposed, revoke it and create a new one.
