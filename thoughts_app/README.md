# Thought Processor with Claude Council

An offline application for recording and processing random thoughts using a simulated Claude Council AI system that classifies ideas and ranks them by potential ROI.

## Features

- 💭 Record thoughts via typing or simulate voice recording
- 🤖 Claude Council (3 AI agents) processes each thought
- 🏷️ Automatic classification into categories:
  - Random Thought
  - Goal
  - Business Idea
  - Implementation
  - Other
- 📊 ROI scoring (0-10 scale) based on potential value
- 💾 Local storage - works completely offline
- 📈 View thoughts sorted by ROI (highest first)
- 🕒 Timestamp tracking for all entries

## How It Works

1. Enter a thought by typing or simulating voice recording
2. The Claude Council (3 simulated AI agents) independently evaluates:
   - Classification of the thought
   - Potential ROI score (0-10)
3. The council reaches consensus on classification and averages ROI scores
4. Thought is saved locally with timestamp
5. View all thoughts or see them ranked by ROI potential

## Classification Categories

- **Random Thought**: Fleeting ideas, observations, or musings
- **Goal**: Personal or professional objectives
- **Business Idea**: Potential ventures, products, or services
- **Implementation**: Specific plans, steps, or technical solutions
- **Other**: Anything that doesn't fit the above categories

## ROI Scoring

Scores are on a 0-10 scale where:
- 0-3: Low potential value (exploratory, entertainment)
- 4-6: Moderate potential value (worth considering)
- 7-10: High potential value (pursue actively)

## Installation

1. Ensure you have Python 3.6+ installed
2. Clone or download this repository
3. Navigate to the project directory
4. Run: `python main.py`

## Usage

```
$ python main.py
🚀 Initializing Thought Processor...
✅ Loaded 0 existing thoughts

==================================================
🧠 Thought Processor with Claude Council
==================================================
1. Enter a new thought (type or simulate recording)
2. View all thoughts
3. View thoughts sorted by ROI (highest first)
4. Exit
--------------------------------------------------
Select an option (1-4): 1

💭 Enter your thought (or type 'record' to simulate voice recording):
> I wonder if we could create an app that helps people track their water intake throughout the day
...
[Processing output]
💾 Thought saved with ID: 1
```

## Offline First

This application stores all data locally in a `thoughts.json` file in the same directory. No internet connection is required for any functionality.

## Customization

To adjust the number of AI agents in the council, modify the `num_agents` parameter when initializing `ClaudeCouncil` in `main.py`.

To change classification categories or ROI scoring logic, edit the `MockAIAgent.process_thought` method.

## License

MIT