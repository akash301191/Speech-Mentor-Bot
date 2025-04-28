# Speech Mentor Bot

Speech Mentor Bot is a helpful Streamlit application that guides you in crafting impactful speeches. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot explores real-world examples, delivery techniques, and structure ideas to generate a personalized speech preparation guide tailored to your audience, occasion, and goals.

## Folder Structure

```
Speech-Mentor-Bot/
├── speech-mentor-bot.py
├── README.md
└── requirements.txt
```

- **speech-mentor-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Speech Preparation Input**  
  Fill out your audience type, speaking context, theme, tone, experience level, and speech duration.

- **AI-Powered Speech Research**  
  The Speech Researcher agent crafts a focused Google search using SerpAPI to find relevant speeches, delivery tips, and structural frameworks based on your profile.

- **Personalized Speech Guide**  
  The Speech Mentor agent analyzes the research results and generates a comprehensive speech preparation guide covering suggested titles, key points to cover, delivery tips, and links to inspiring examples.

- **Structured Markdown Output**  
  Your speech guide is presented in a clean Markdown format, divided into clear sections, making it easy to follow and practice.

- **Two-Column Display Layout**  
  Suggested titles and key points are displayed side-by-side with delivery tips and inspirational resources for a polished, professional look.

- **Download Option**  
  Download your personalized speech preparation guide as a `.txt` file for future reference or practice.

- **Clean Streamlit UI**  
  Built with Streamlit to ensure an intuitive, fast, and distraction-free mentoring experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Speech-Mentor-Bot.git
   cd Speech-Mentor-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run speech-mentor-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys in the sidebar.
   - Fill out your audience, theme, style, and speech preferences.
   - Click **🎤 Generate Speech Preparation Guide**.
   - View your personalized, AI-generated speech mentoring guide.
   - Download it for easy practice or event preparation.

3. **Download Option**  
   Use the **📥 Download Speech Preparation Guide** button to save your speech guide as a `.txt` file.

## Code Overview

- **`render_speech_inputs()`**: Captures user inputs about their audience, goals, speaking style, experience, and theme.
- **`render_sidebar()`**: Manages OpenAI and SerpAPI API keys in Streamlit session state.
- **`generate_speech_guide()`**:  
  - Uses the `Speech Researcher` agent to search for real-world examples and techniques via SerpAPI.  
  - Sends the results to the `Speech Mentor` agent to generate a structured speech preparation guide.
- **`display_speech_guide()`**:  
  - Organizes the output into two columns:  
    - Suggested Titles + Key Points on the left  
    - Delivery Tips + Inspirational Resources on the right.
- **`main()`**: Handles layout, collects inputs, and manages the overall flow for guide generation and display.

## Contributions

Contributions are welcome!  
Feel free to fork the repo, suggest features, report bugs, or open a pull request.  
Please ensure your contributions are clean, well-tested, and aligned with the goal of helping users prepare impactful speeches easily.