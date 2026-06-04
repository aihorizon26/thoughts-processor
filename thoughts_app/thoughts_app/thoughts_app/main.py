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

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("Thought Processor with Claude Council")
    print("="*50)
    print("1. Enter a new thought (type or simulate recording)")
    print("2. View all thoughts")
    print("3. View thoughts sorted by ROI (highest first)")
    print("4. Exit")
    print("-"*50)

def get_user_input():
    """Get thought input from user"""
    print("\n💭 Enter your thought (or type 'record' to simulate voice recording):")
    user_input = input("> ").strip()

    if user_input.lower() == 'record':
        print("\n🎤 Simulating voice recording... (in a real app, this would use microphone)")
        thought = input("📝 What did you say? ").strip()
        return thought if thought else None
    return user_input if user_input else None

def main():
    """Main application loop"""
    print("[*] Initializing Thought Processor...")

    # Initialize components
    council = ClaudeCouncil(num_agents=3)
    thought_manager = ThoughtManager()

    print(f"[+] Loaded {len(thought_manager.get_thoughts())} existing thoughts")

    while True:
        display_menu()
        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            thought = get_user_input()
            if not thought:
                print("[!] No thought entered. Please try again.")
                continue

            print("\n[~] Processing thought with Claude Council...")
            classification, roi_score = council.evaluate_thought(thought)

            print(f"\n[+] Results:")
            print(f"   Thought: {thought[:100]}{'...' if len(thought) > 100 else ''}")
            print(f"   Classification: {classification}")
            print(f"   ROI Score: {roi_score}/10.0")

            # Save the thought
            saved_thought = thought_manager.add_thought(thought, classification, roi_score)
            print(f"[+] Thought saved with ID: {saved_thought['id']}")

        elif choice == '2':
            thoughts = thought_manager.get_thoughts()
            if not thoughts:
                print("\n[-] No thoughts recorded yet.")
                continue

            print(f"\n[+] All Thoughts ({len(thoughts)} total):")
            print("-"*70)
            for i, t in enumerate(thoughts, 1):
                timestamp = datetime.fromisoformat(t['timestamp']).strftime("%m/%d %H:%M")
                print(f"{i:2d}. [{t['classification']:.15s}] ROI:{t['roi_rank']:4.1f} | {timestamp}")
                print(f"    {t['thought'][:80]}{'...' if len(t['thought']) > 80 else ''}")
                print()

        elif choice == '3':
            thoughts = thought_manager.get_thoughts(sort_by_roi=True)
            if not thoughts:
                print("\n[-] No thoughts recorded yet.")
                continue

            print(f"\n[+] Thoughts Sorted by ROI (Highest First):")
            print("-"*70)
            for i, t in enumerate(thoughts, 1):
                timestamp = datetime.fromisoformat(t['timestamp']).strftime("%m/%d %H:%M")
                print(f"{i:2d}. ROI:{t['roi_rank']:4.1f} | [{t['classification']:.15s}] | {timestamp}")
                print(f"    {t['thought'][:80]}{'...' if len(t['thought']) > 80 else ''}")
                print()

        elif choice == '4':
            print("\n[+] Goodbye! Your thoughts have been saved.")
            break

        else:
            print("[!] Invalid option. Please select 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[+] Interrupted. Your thoughts have been saved.")
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")
        print("Please try again or contact support.")