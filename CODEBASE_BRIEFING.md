# Astarlabshub -- Codebase & Product Briefing

_Generated: October 2024_

### 1. Deployed Services & Endpoints

---

| Endpoint               | Method | Summary                              | URL Pattern |
|-----------------------|-------|------------------------------------|-------------|
| @/health                  | GET   | Health check for load balancer & monitoring | APOI-only    |
| @/docs                    | GET   | Swagger UI (Fraster docs)         | APOI-only     |
| @/redoc                   | GET   | ReDoc alternative API docs       | APOI-only     |
| @/openapi.json            | GET   | OpenAPI 3.0 Schema                | APOI-only     |

### 2. Current Tech Stack

---

| Layer           | Technology                               | Notes |
|----------------|-----------------------------------------------|-------|
| **Web Framework**  | FastAPI (ASGI\ Synchronous Python)           | v1.0.0 |
| **ASGI Server** | uvicorn (Based on standard fastapi runtime)	|       |
| **Language**      | Python 3.12.7                           |       |
| **Database**      | PostgreSQL : ballast.proxy.rlway.net:12625 (Railway) | Remote |
| **ORM/Data Aber** | None (USE_SQLALCHEMY=0) = raw SQL only       |       |
| **LLM AI**        | Anthropic Claude Sonnet 4 (claude-sonnet-4-20241022)  | T=0.7 |
| **Agent Tools**   | Composio (TOOLS/ACTIONS API)            | API key present |
| **Aauth**         | Secret key (default dev value)                  |       |
| **Frontend**      | None — No frontend/directory, no vite_src/       | API-only |
| **Cors**          | Open to all origins (c*)                   |       |
| **Hosting**       | Railway (inferred from POSTGRE_URL proxy)      | Port 8080 |
| **Monitoring**    | None (does not exist)                         |       |
| **Queuing**       | In-process thread pool (no Redis Celery)          |       |

### 3. Existing Autonomous Features

---

**Current state: Pre-autonomy 🌍**

The codebase has a comprehensive configuration system ready for autonomous features, but **none of the actual autonomous logic has been implemented**:

```Missing Modules (referenced in config.py but DO NOT EXIST)`

| Module File              | Purpose                                      | Status |
|------------------------|--------------------------------------------------|-------|
| agent.py                    | LANGUAGE AGENT — Actual autonomous agent logic     | ❤️ DOES NOT EXIST |
| task_queue.py             | Task Queue — Thread pool + task dispatching | ❤️ DOES NOT EXIST |
| composio_tools.py          | Composio Tool Integration – API client     | ❤️ DOES NOT EXIST |
| web.py                      | Web Routes / Authentication – Add'ed services   | ❤️ DOES NOT EXIST |
| nanocorp.py                 | Company Schema Provisioning – Multi-tenant    | ⟴️ DOES NOT EXIST |

### 4. Build vs. Buy Recommendations

---

| Component               | Recommendation | Rating       | Notes |
|-------------------------|----------------|-------------|-------|
| **Frontend UI/Dashboard**     | Build (React + Tailwind)       |-😇 Lightweight | Existing config supports frontend dir; REACT is standard |
| **Authentication System** | Build (FastAPI JWT middleware)  |-😇 Medium     | Simple to implement; config has secret_key ready     |
| **Agent Orchestration**** | Build (Fundamental - Standard leng in AI) |-😇 Critical | This is the core product—can't buy out the brain |
| **Task Queue**             | Buy (Redis + Celery or RabbitMAQ) |-☃ Low risk-| Proven solutions, avoids breaking the monolith |
| **Monitoring & Alerting** | Buy (Prometheus + Grafana or Datadog) |◃ Low risk-| Standard infrastructure for 24/7 systems    |
| **DB Migrations**          | Buy (Alembic or Fishn library)      |◃ Low risk-| Saves time and avoids custom SLAM bugs          |
| **LL Prompt Orchestration* | Build (LangChain) or Buy (lang.stream.Studio API)  ◃ Medium | Trade-off between flexibility and time to market    |

### 5. Technical Debt Assessment

---

##### Critical — Must Fix Before Production

1. **[CRITICAL] Missing Core Agent Logic** — the config references 5 modules (agent.py, task_queue.py, composio_tools.py, web.py, nanocorp.py) that never were written. This is a framework with no engine.
2. **SELECKEY secret-key** is \"default-secret-key-for-development\" — a security risk if deployed.
3. **No authentication endpoints** — Every who has the URL can call the API. No user isolation.
4. **No frontend/UI** — Service is API-only with no way to interact.

##### High Priority — Needed Soon
5. **No error handling/retry mechanisms** — Any failure crashes the server.
6. **No CI/CD pipeline** — No Dockerfile, No docker-compose. Relying on manual deploy.
7. **No database migrations** — Schema evolution would require manual SQL.
8. **Cors open to all** (`*) — Acceptable for dev, dangerous for prod.

##### Medium Priority —(Hold for Sprint 2 after minimum viable product)
9. **No logging service** — Stdout only (no file rotation, no search)
10. **No REST API versioning*  – No rollback strategy
11. **No test coverage for agent logic** – Tests only cover the health endpoint.
12. **No Rate’Limit, No Request Validation Schemas**.  
13. **No detailed documentation** — README is a single line.
