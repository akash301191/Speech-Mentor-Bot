import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_speech_inputs():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Audience & Context
    with col1:
        st.subheader("🎯 Audience & Context")
        audience_type = st.selectbox(
            "Who is your audience?*",
            ["High School Students", "University Students", "Corporate Team", "General Public", "Conference Attendees", "Wedding Guests", "Other"]
        )
        occasion = st.selectbox(
            "What is the occasion?*",
            ["School Competition", "Business Meeting", "Conference Talk", "Social Event", "Ceremonial Speech", "Other"]
        )
        speech_goal = st.selectbox(
            "What is your main goal?*",
            ["Inform", "Persuade", "Entertain", "Inspire", "Celebrate", "Other"]
        )

    # Column 2: Content & Style
    with col2:
        st.subheader("📝 Content & Style")
        speech_theme = st.text_input(
            "What is the general theme or subject of your speech?*", 
            placeholder="e.g., Leadership, Environmental Awareness, Overcoming Challenges"
        )
        important_points = st.text_area(
            "Specific points, stories, or ideas you definitely want to include (optional)",
            placeholder="E.g., Share a personal story about teamwork"
        )
        speaking_style = st.selectbox(
            "What tone do you want your speech to have?*",
            ["Formal", "Semi-formal", "Casual", "Humorous", "Inspirational", "Storytelling"]
        )

    # Column 3: Duration & Comfort
    with col3:
        st.subheader("⏱️ Duration & Comfort")
        speech_duration = st.selectbox(
            "How long should your speech be?*",
            ["1–3 minutes", "3–5 minutes", "5–10 minutes", "10+ minutes"]
        )
        speaking_experience = st.radio(
            "How comfortable are you with public speaking?",
            ["Beginner", "Some experience", "Confident speaker"]
        )
        final_message = st.text_input(
            "If your audience remembers just one thing from your speech, what should it be? (optional)",
            placeholder="E.g., Never stop learning, teamwork drives success, every small effort matters."
        )

    # Assemble the full speech preparation profile
    speech_profile = f"""
    **Audience & Context:**
    - Audience Type: {audience_type}
    - Occasion: {occasion}
    - Speech Goal: {speech_goal}

    **Content & Style:**
    - Theme/Subject: {speech_theme}
    - Important Points: {important_points if important_points.strip() else 'Not specified'}
    - Speaking Tone: {speaking_style}

    **Duration & Comfort:**
    - Expected Duration: {speech_duration}
    - Public Speaking Experience: {speaking_experience}
    - Core Message to Emphasize: {final_message if final_message.strip() else 'Not specified'}
    """

    return speech_profile

def generate_speech_guide(user_speech_profile: str) -> str:
    speech_research_agent = Agent(
        name="Speech Researcher",
        role="Finds inspirational speech examples, delivery techniques, and structural ideas based on the user's speech profile.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a speech preparation mentor. Given a detailed user speech profile, your job is to suggest a strong speech title,
            key points to cover, tips for effective delivery, and links to inspiring example speeches.
            You will generate a focused, real-world search query, search the web, and extract the 10 most relevant examples or resources.
        """),
        instructions=[
            "Carefully read the user's speech profile to understand the audience, theme, tone, goal, and other inputs.",
            "Based on this, generate ONE highly focused and specific search query. Examples: 'motivational 5-minute speeches for high school students', 'funny wedding toast ideas', or 'storytelling speeches for business presentations'.",
            "Avoid generic searches like 'good speeches'. Keep it targeted toward the user's audience, theme, tone, and occasion.",
            "Use search_google with the generated query.",
            "From the search results, extract the top 10 most relevant resources — examples of speeches, tips on structure and delivery, or frameworks that match the user profile.",
            "Prioritize links or summaries that include practical takeaways: speech examples, structural templates, opening lines, delivery strategies, emotional techniques, audience engagement ideas.",
            "Do not fabricate or invent information. Only use what’s actually found in the search results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = speech_research_agent.run(user_speech_profile)
    research_results = research_response.content

    speech_mentor_agent = Agent(
        name="Speech Mentor",
        role="Creates a personalized speech guideline using user requirements and extracted insights from trusted URLs.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are an expert speech mentor. You are provided with:
            1. A structured summary of the user's speech preparation details.
            2. A list of URLs pointing to trusted speech examples, delivery techniques, and structuring guides.

            Your job is to analyze the content from the URLs and extract useful insights that align with the user's profile.
            Then, create a practical, easy-to-follow speech preparation guide tailored to the user's goals and speaking style.
        """),
        instructions=[
            "Carefully review the user's structured speech profile. Pay close attention to:",
            "- **Audience Type**: Match the tone, content, and delivery suggestions to suit the audience (e.g., students, corporate teams, wedding guests).",
            "- **Occasion**: Ensure the speech outline fits the occasion's formality and emotional tone (e.g., competition, business meeting, celebration).",
            "- **Speech Goal**: Focus the speech structure around the primary goal (e.g., inspire, entertain, inform, celebrate).",
            "- **Theme/Subject**: Align examples, story choices, and emphasis with the user's intended theme or subject.",
            "- **Speaking Style**: Match the recommended speaking style (e.g., formal, semi-formal, casual, humorous, inspirational, storytelling).",
            "- **Speech Duration**: Structure the number and depth of points according to the duration (e.g., 1–3 minutes = 2–3 key points; 5–10 minutes = 3–5 key points).",
            "- **Important Points**: If the user has provided specific ideas, stories, or topics, prioritize weaving them into the speech structure meaningfully.",
            "- **Public Speaking Experience**: Adapt delivery tips to the user's experience level —",
            "   - For beginners: emphasize basic confidence techniques, pacing, and simple audience connection tips.",
            "   - For experienced speakers: suggest advanced techniques like humor timing, emotional storytelling, rhetorical questions, and body language enhancements.",
            "- **Core Message to Emphasize**: Ensure the speech is consistently centered around the user's main takeaway idea, reinforcing it in the opening, middle, and conclusion.",

            "Now read and analyze the content from each research URL provided.",
            "Use only insights found in these sources. Do not invent examples, delivery tips, titles, or links beyond what is supported by the URLs.",

            "Create a structured speech mentoring guide in clean Markdown format with the following sections:",
            "### 🎯 Suggested Title",
            "- Offer 1–2 strong title options that align with the theme, goal, and tone of the speech.",
            
            "### 🗝️ Key Points to Cover",
            "- Bullet-point a logical and engaging outline for the speech (opening hook, body points, conclusion), clearly tied to the speech goal.",
            "- Incorporate any important points/stories provided by the user where suitable.",
            
            "### 🗣️ Delivery Tips",
            "- Summarize speaking techniques tailored to the user's style and public speaking experience.",
            "- Cover tone, pacing, engagement strategies, humor tips if appropriate, audience interaction techniques, body language suggestions.",
            
            "### 🔗 Inspirational Resources",
            "- List 5–7 highly relevant speech examples, articles, or frameworks found during research.",
            "- Embed links using Markdown format: [Speech Title](https://link.example). Do not paste raw URLs.",

            "Ensure the final output is encouraging, actionable, and helps the user feel fully supported in preparing and delivering their speech."
        ],
        add_datetime_to_instructions=True
    )

    mentor_input = f"""
    User Speech Preparation Profile:
    {user_speech_profile}

    Research Results:
    {research_results}

    Use these details to draft a comprehensive Speech Preparation Guide.
    """

    response = speech_mentor_agent.run(mentor_input)
    speech_guide = response.content   

    return speech_guide 

def display_speech_guide(speech_guide: str) -> None:
    # Break speech guide into sections based on Markdown headers
    sections = speech_guide.split('### ')
    sections = [section.strip() for section in sections if section.strip()]

    # Dictionary to store separated sections
    content = {
        "Suggested Title": "",
        "Key Points to Cover": "",
        "Delivery Tips": "",
        "Inspirational Resources": ""
    }

    # Parse and store content in the dictionary
    for section in sections:
        if section.startswith("🎯 Suggested Title"):
            content["Suggested Title"] = section
        elif section.startswith("🗝️ Key Points to Cover"):
            content["Key Points to Cover"] = section
        elif section.startswith("🗣️ Delivery Tips"):
            content["Delivery Tips"] = section
        elif section.startswith("🔗 Inspirational Resources"):
            content["Inspirational Resources"] = section

    # Display in two columns
    col1, col2 = st.columns(2)

    with col1:
        if content["Suggested Title"]:
            st.markdown(f"### {content['Suggested Title']}", unsafe_allow_html=True)
        if content["Key Points to Cover"]:
            st.markdown(f"### {content['Key Points to Cover']}", unsafe_allow_html=True)

    with col2:
        if content["Delivery Tips"]:
            st.markdown(f"### {content['Delivery Tips']}", unsafe_allow_html=True)
        if content["Inspirational Resources"]:
            st.markdown(f"### {content['Inspirational Resources']}", unsafe_allow_html=True)


def main() -> None:
    # Page config
    st.set_page_config(page_title="Speech Mentor Bot", page_icon="🎤", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🎤 Speech Mentor Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Speech Mentor Bot — your personal guide for crafting memorable speeches. Get tailored suggestions for your speech title, key points to cover, delivery tips, and inspiration drawn from real-world examples.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_speech_profile = render_speech_inputs()
    
    st.markdown("---")

    # Main button to trigger Speech Guide generation
    if st.button("🎤 Generate Speech Preparation Guide"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Creating a Speech Preparation Guide for You..."):
                speech_guide = generate_speech_guide(user_speech_profile=user_speech_profile)
                st.session_state.speech_guide = speech_guide

    # Display the Speech Guide if available
    if "speech_guide" in st.session_state:
        st.markdown("## 📜 Speech Preparation Guide", unsafe_allow_html=True)
        display_speech_guide(st.session_state.speech_guide)
        #st.markdown(st.session_state.speech_guide, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Speech Preparation Guide",
            data=st.session_state.speech_guide,
            file_name="speech_preparation_guide.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()