# Multi-Agent Research Assistant

A research assistant built with **LangGraph** (multi-agent orchestration),
**MCP** (Model Context Protocol tool server), and **A2A** (agent-to-agent
messaging between independently running services).

## What it does

Given a topic, four agents collaborate to produce a report:

1. **Planner** — breaks the topic into concrete research questions.
2. **Researcher** — calls a **web_search** tool over MCP to gather live
   information, then condenses it into notes.
3. **Writer** — synthesizes notes into a draft report.
4. **Critic** — reviews the draft. If it's not good enough, the graph loops
   back to the researcher with feedback (up to `MAX_REVISION_ITERATIONS`);
   otherwise it finalizes the report.

This loop is a genuine LangGraph `StateGraph` with a conditional edge, not a
linear chain — see `graph.py`.

## Two ways this system runs

### 1. In-process (`main.py`)
All four agents run as LangGraph nodes inside one Python process. Good for
demonstrating the graph/orchestration logic and the revision loop.

### 2. As distributed A2A services (`a2a/`)
`research_agent_service.py` and `coordinator_service.py` are **two separate
FastAPI processes** that talk to each other over HTTP using a structured
`A2AMessage` protocol (`a2a/protocol.py`) — sender, receiver, performative
(`request`/`inform`/`failure`), conversation id, payload. The coordinator
sends a `request`, the research agent replies with `inform`. This is what
actually demonstrates "agent-to-agent communication pipelines" as opposed to
one script calling its own functions.

## How each gap in the job posting is covered

| Requirement | Where |
|---|---|
| LangChain / LangGraph | `graph.py`, `agents/*.py` — real `StateGraph` with nodes + conditional loop |
| MCP tools | `mcp_server/search_server.py` — a real MCP server (stdio transport) exposing `web_search` and `fetch_url_summary` as tools; `agents/mcp_client.py` is the MCP client that calls it |
| Multi-agent / A2A | `a2a/` — two independent FastAPI services exchanging structured A2A messages over HTTP |
| Distributed AI-integrated architecture | `docker-compose.yml` — research agent and coordinator run as separate containers, service-to-service over the Docker network |

Vector DBs and GraphDBs (Neo4j) are **not** in this project on purpose — see
Project 2 (Graph-RAG Knowledge System), which extends this one.

## Setup

```bash
git clone <your-repo>
cd multi-agent-research-assistant
python -m venv venv && source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # then fill in GROQ_API_KEY (get one free at console.groq.com)
```

## Running it

### Option A — single process, LangGraph only
```bash
python main.py "The impact of retrieval-augmented generation on enterprise search"
```

### Option B — distributed A2A services, locally
Terminal 1:
```bash
uvicorn a2a.research_agent_service:app --port 8001
```
Terminal 2:
```bash
uvicorn a2a.coordinator_service:app --port 8000
```
Terminal 3:
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "LangGraph vs CrewAI for agent orchestration"}'
```

### Option C — distributed A2A services, via Docker Compose
```bash
docker compose up --build
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "GraphRAG vs vector-only RAG"}'
```

### Testing the MCP server on its own
```bash
python agents/mcp_client.py
```

## Project structure

```
multi-agent-research-assistant/
├── agents/
│   ├── state.py            # shared LangGraph state schema
│   ├── planner_agent.py
│   ├── researcher_agent.py # calls the MCP web_search tool
│   ├── writer_agent.py
│   ├── critic_agent.py
│   └── mcp_client.py       # MCP client used by researcher_agent
├── mcp_server/
│   └── search_server.py    # MCP server: web_search, fetch_url_summary tools
├── a2a/
│   ├── protocol.py         # A2AMessage / A2AResponse schema
│   ├── research_agent_service.py  # standalone FastAPI agent, port 8001
│   └── coordinator_service.py     # standalone FastAPI agent, port 8000
├── graph.py                 # LangGraph StateGraph wiring + revision loop
├── main.py                  # entry point for in-process run
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Notes / honest caveats

- You need a free `GROQ_API_KEY` from https://console.groq.com for this to
  actually run — it isn't tested end-to-end here since no key is wired in.
  This matches the Groq usage already on your CV from the RAG Chatbot
  project.
- `duckduckgo-search` is used for the web_search tool because it needs no
  API key. Swap in a paid search API if you want more reliable results.
- For a resume bullet, this supports something like: *"Built a multi-agent
  research system using LangGraph with a conditional revision loop, a custom
  MCP tool server, and a distributed A2A messaging layer between
  independently deployed FastAPI agent services, containerized with Docker
  Compose."*
