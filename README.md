# Good Question - Follow-up Question Evaluation Tool

This repository contains tools for evaluating question quality in human-AI interactions, specifically for the [CogSci2025 conference](https://cognitivesciencesociety.org/cogsci-2025/) presentation.



## Introduction

This project evaluates the quality of follow-up questions (FQs) in conversations based on predefined rubrics. It uses the Anthropic API to assess the effectiveness of these questions according to different contexts and goals, with a focus on cognitive science research.

## Project Structure

- `eval_anth.py`: Main evaluation script that processes sample conversations and applies the rubric
- `Rubric_GQ.json`: Evaluation criteria for good follow-up questions
- `system_prompt.txt`: System prompt template for Claude
- `_src/`: Directory containing sample conversation data
- `_output/`: Directory where evaluation results are stored
- `.env`: Configuration for API keys (not included in repository)

## Requirements

To run this evaluation tool, install the required dependencies:

```bash
pip install -r requirements.txt

```

The requirements include:

- anthropic>=0.19.1
- python-dotenv>=1.0.0
- datetime

## Setup

1. Clone this repository
2. Install dependencies using the command above
3. Create a `.env` file in the root directory with your Anthropic API key:
    ```bash
    ANTHROPIC_API_KEY=your_api_key_here
    ```
    Note: The `.env` file is included in `.gitignore` and will not be uploaded to the repository for security reasons.
    

    

## Usage

Run the evaluation script with:

```bash
python eval_anth.py
```

The script will:

1. Load sample conversations from the specified input file
2. Apply the evaluation rubric with the configured variables
3. Generate evaluations using Claude
4. Save results to the `_output` directory with a timestamp

## Configuration

You can modify the following variables in `eval_anth.py`:

- `RUBRIC_VARIABLES`: Customize context variables like "answerer" and "goal"
- `MODEL_NAME`: Change the Claude model version
- `MODEL_TEMPERATURE`: Adjust the randomness of Claude's responses
- `MAX_TOKENS`: Set the maximum token length for responses