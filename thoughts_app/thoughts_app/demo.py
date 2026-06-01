"""
Demo script to show how the Thought Processor works
without requiring interactive input.
"""
import json
import os
import random
from datetime import datetime
from enum import Enum

class Classification(Enum):
    RANDOM_THOUGHT = "random thought"
    GOAL = "goal"
    BUSINESS_IDEA = "business idea"
    IMPLEMENTATION = "implementation"
    OTHER = "other"

class MockAIAgent:
    """Mock AI agent for processing thoughts"""
    def __init__(self, name):
        self.name = name

    def process_thought(self, thought):
        """Process a thought and return classification and ROI score"""
        # Simulate different agents having different biases
        classifications = list(Classification)
        weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # Favors random thoughts slightly
        classification = random.choices(classifications, weights=weights)[0]

        # ROI score based on classification type
        base_scores = {
            Classification.RANDOM_THOUGHT: (1.0, 3.0),
            Classification.GOAL: (4.0, 7.0),
            Classification.BUSINESS_IDEA: (6.0, 9.0),
            Classification.IMPLEMENTATION: (5.0, 8.0),
            Classification.OTHER: (2.0, 5.0)
        }

        low, high = base_scores[classification]
        roi_score = round(random.uniform(low, high), 1)

        return classification.value, roi_score

class ClaudeCouncil:
    """Simulates a council of Claude AI agents"""
    def __init__(self, num_agents=3):
        self.agents = [MockAIAgent(f"Claude-Agent-{i+1}") for i in range(num_agents)]

    def evaluate_thought(self, thought):
        """Have the council evaluate a thought and return consensus"""
        classifications = []
        roi_scores = []

        for agent in self.agents:
            classification, roi = agent.process_thought(thought)
            classifications.append(classification)
            roi_scores.append(roi)

        # Consensus classification (most common)
        consensus_classification = max(set(classifications), key=classifications.count)

        # Average ROI score
        average_roi = sum(roi_scores) / len(roi_scores)

        return consensus_classification, round(average_roi, 1)

class ThoughtManager:
    """Manages storing and retrieving thoughts"""
    def __init__(self, storage_file="thoughts.json"):
        self.storage_file = storage_file
        self.thoughts = self._load_thoughts()

    def _load_thoughts(self):
        """Load thoughts from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_thoughts(self):
        """Save thoughts to storage file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.thoughts, f, indent=2)

    def add_thought(self, thought, classification, roi_score):
        """Add a new thought to the collection"""
        new_thought = {
            "id": len(self.thoughts) + 1,
            "thought": thought,
            "classification": classification,
            "roi_rank": roi_score,
            "timestamp": datetime.now().isoformat()
        }
        self.thoughts.append(new_thought)
        self._save_thoughts()
        return new_thought

    def get_thoughts(self, sort_by_roi=False):
        """Get all thoughts, optionally sorted by ROI"""
        thoughts = self.thoughts.copy()
        if sort_by_roi:
            thoughts.sort(key=lambda x: x['roi_rank'], reverse=True)
        return thoughts

def run_demo():
    """Run a demonstration of the thought processor"""
    print("=== Thought Processor Demo ===\n")

    # Initialize components
    council = ClaudeCouncil(num_agents=3)
    thought_manager = ThoughtManager(storage_file="demo_thoughts.json")

    # Clear any existing demo data
    if os.path.exists("demo_thoughts.json"):
        os.remove("demo_thoughts.json")

    thought_manager = ThoughtManager(storage_file="demo_thoughts.json")

    # Sample thoughts to process
    sample_thoughts = [
        "I wonder if we could create an app that helps people track their water intake throughout the day",
        "I should exercise more regularly to improve my health",
        "What if we started a subscription box service for remote workers?",
        "Need to refactor the authentication module to use OAuth2 instead of JWT",
        "It's a beautiful day outside, makes me want to go for a walk",
        "I want to learn Spanish this year",
        "Could we implement a machine learning model to predict customer churn?",
        "The login page is loading slowly, we should optimize the database queries",
        "Wouldn't it be nice to have a personal AI assistant for daily tasks?",
        "I should save more money for emergencies"
    ]

    print(f"Processing {len(sample_thoughts)} sample thoughts...\n")

    # Process each thought
    for i, thought in enumerate(sample_thoughts, 1):
        print(f"{i:2d}. Processing: \"{thought[:60]}{'...' if len(thought) > 60 else ''}\"")

        # Process with Claude Council
        classification, roi_score = council.evaluate_thought(thought)

        # Save the thought
        saved_thought = thought_manager.add_thought(thought, classification, roi_score)

        print(f"    -> Classification: {classification}")
        print(f"    -> ROI Score: {roi_score}/10.0")
        print(f"    -> Saved with ID: {saved_thought['id']}\n")

    # Show results
    print("=" * 50)
    print("ALL THOUGHTS:")
    print("=" * 50)
    thoughts = thought_manager.get_thoughts()
    for i, t in enumerate(thoughts, 1):
        timestamp = datetime.fromisoformat(t['timestamp']).strftime("%m/%d %H:%M")
        print(f"{i:2d}. [{t['classification']:.15s}] ROI:{t['roi_rank']:4.1f} | {timestamp}")
        print(f"    {t['thought'][:70]}{'...' if len(t['thought']) > 70 else ''}")
        print()

    print("=" * 50)
    print("THOUGHTS SORTED BY ROI (HIGHEST FIRST):")
    print("=" * 50)
    thoughts_sorted = thought_manager.get_thoughts(sort_by_roi=True)
    for i, t in enumerate(thoughts_sorted, 1):
        timestamp = datetime.fromisoformat(t['timestamp']).strftime("%m/%d %H:%M")
        print(f"{i:2d}. ROI:{t['roi_rank']:4.1f} | [{t['classification']:.15s}] | {timestamp}")
        print(f"    {t['thought'][:70]}{'...' if len(t['thought']) > 70 else ''}")
        print()

    # Clean up demo file
    if os.path.exists("demo_thoughts.json"):
        os.remove("demo_thoughts.json")

    print("Demo completed! The application works offline and stores data locally.")

if __name__ == "__main__":
    run_demo()