
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

RESEARCH_AGENT_PORT = int(os.getenv("RESEARCH_AGENT_PORT", "8001"))
COORDINATOR_PORT = int(os.getenv("COORDINATOR_PORT", "8000"))

MAX_REVISION_ITERATIONS = int(os.getenv("MAX_REVISION_ITERATIONS", "2"))
