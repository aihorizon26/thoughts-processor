import os
import json
import random
from datetime import datetime
from enum import Enum
from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# ---------- Claude Council logic ----------
class Classification(Enum):
    RANDOM_THOUGHT = "random thought"
    GOAL = "goal"
    BUSINESS_IDEA = "business idea"
    IMPLEMENTATION = "implementation"
    OTHER = "other"

class MockAIAgent:
    def __init__(self, name):
        self.name = name

    def process_thought(self, thought):
        classifications = list(Classification)
        # Slight bias towards random thoughts and goals
        weights = [0.3, 0.2, 0.2, 0.2, 0.1]
        classification = random.choices(classifications, weights=weights)[0]

        base_scores = {
            Classification.RANDOM_THOUGHT: (1.0, 3.0),
            Classification.GOAL: (4.0, 7.0),
            Classification.BUSINESS_IDEA: (6.0, 9.0),
            Classification.IMPLEMENTATION: (5.0, 8.0),
            Classification.OTHER: (2.0, 5.0)
        }
        low, high = base_scores[classification]
        roi = round(random.uniform(low, high), 1)
        return classification.value, roi

class ClaudeCouncil:
    def __init__(self, num_agents=3):
        self.agents = [MockAIAgent(f"Claude-Agent-{i+1}") for i in range(num_agents)]

    def evaluate_thought(self, thought):
        classifications, roi_scores = [], []
        for agent in self.agents:
            c, r = agent.process_thought(thought)
            classifications.append(c)
            roi_scores.append(r)

        # Consensus classification (most common)
        consensus = max(set(classifications), key=classifications.count)
        avg_roi = sum(roi_scores) / len(roi_scores)
        return consensus, round(avg_roi, 1)

council = ClaudeCouncil()

# Optional: write each thought as markdown file for Obsidian sync via GitHub
def write_obsidian_markdown(thought_id, thought, classification, roi):
    """
    Writes a markdown file to ./obsidian_sync/ (intended to be tracked by git).
    Caller should ensure the directory exists and is a git repo.
    """
    os.makedirs("obsidian_sync", exist_ok=True)
    slug = thought.strip().lower().replace(" ", "-")[:40]
    filename = f"{thought_id:04d}-{slug}.md"
    frontmatter = f"""---
id: {thought_id}
classification: {classification}
roi: {roi}
created: {datetime.utcnow().isoformat()}Z
---
{thought}
"""
    with open(os.path.join("obsidian_sync", filename), "w", encoding="utf-8") as f:
        f.write(frontmatter)

# ---------- API Endpoints ----------
@app.route("/api/thoughts", methods=["GET"])
def get_thoughts():
    """Return all thoughts, newest first by default; support ?order=roi.desc"""
    order = request.args.get("order", "created_at.desc")
    if order == "roi.desc":
        resp = supabase.table("thoughts").select("*").order("roi", desc=True).execute()
    else:
        resp = supabase.table("thoughts").select("*").order("created_at", desc=True).execute()
    return jsonify(resp.data)

@app.route("/api/thoughts", methods=["POST"])
def add_thought():
    data = request.get_json(force=True)
    raw = data.get("thought", "").strip()
    if not raw:
        return jsonify({"error": "empty thought"}), 400

    classification, roi = council.evaluate_thought(raw)

    insert = supabase.table("thoughts").insert({
        "thought": raw,
        "classification": classification,
        "roi": roi,
        "created_at": datetime.utcnow().isoformat()
    }).execute()
    new_id = insert.data[0]["id"]

    # Optionally create markdown for Obsidian sync (uncomment if using)
    # write_obsidian_markdown(new_id, raw, classification, roi)

    return jsonify({
        "id": new_id,
        "thought": raw,
        "classification": classification,
        "roi": roi,
        "created_at": insert.data[0]["created_at"]
    }), 201

# For local testing only
if __name__ == "__main__":
    app.run(debug=True, port=5000)