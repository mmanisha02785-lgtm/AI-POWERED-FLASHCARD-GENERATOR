import streamlit as st
import ollama
import json
import re
from pypdf import PdfReader

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Flashcard Generator",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AI-Powered Flashcard Generator")
st.write("Generate study flashcards using your notes, topics, or PDF files.")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "current_card" not in st.session_state:
    st.session_state.current_card = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False


# -------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------

def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF."""

    try:
        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        st.error(f"PDF reading error: {e}")
        return ""


# -------------------------------------------------
# GENERATE FLASHCARDS USING OLLAMA
# -------------------------------------------------

def generate_flashcards(topic, notes, number_of_cards, difficulty):

    prompt = f"""
You are an AI flashcard generator.

Create exactly {number_of_cards} useful study flashcards.

Difficulty level: {difficulty}

Study topic:
{topic}

Study material:
{notes[:12000]}

IMPORTANT RULES:

1. Return ONLY a valid JSON array.
2. Do NOT write explanations before or after the JSON.
3. Do NOT use Markdown.
4. Do NOT use ```json.
5. Every flashcard must contain exactly two fields:
   "question"
   "answer"

Example:

[
  {{
    "question": "What is Python?",
    "answer": "Python is a high-level programming language."
  }},
  {{
    "question": "What is a variable?",
    "answer": "A variable stores a value in a program."
  }}
]
"""

    try:

        response = ollama.chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"].strip()

        # Remove Markdown code blocks if Ollama adds them
        content = re.sub(r"```json", "", content, flags=re.IGNORECASE)
        content = re.sub(r"```", "", content)

        content = content.strip()

        # Find JSON array
        start = content.find("[")
        end = content.rfind("]")

        if start == -1 or end == -1:

            st.error("AI did not return valid JSON.")

            with st.expander("See AI response"):
                st.write(content)

            return []

        json_text = content[start:end + 1]

        # Convert JSON string into Python list
        flashcards = json.loads(json_text)

        # Check that response is a list
        if not isinstance(flashcards, list):

            st.error("AI returned an invalid flashcard format.")

            return []

        valid_cards = []

        for card in flashcards:

            if isinstance(card, dict):

                question = card.get("question")
                answer = card.get("answer")

                if question and answer:

                    valid_cards.append(
                        {
                            "question": str(question).strip(),
                            "answer": str(answer).strip()
                        }
                    )

        if not valid_cards:

            st.error("No valid flashcards were generated.")

            return []

        return valid_cards

    except json.JSONDecodeError:

        st.error("AI returned invalid JSON.")

        return []

    except Exception as e:

        st.error(f"Ollama error: {e}")

        return []


# -------------------------------------------------
# SIDEBAR SETTINGS
# -------------------------------------------------

st.sidebar.header("⚙️ Flashcard Settings")

number_of_cards = st.sidebar.slider(
    "Number of flashcards",
    min_value=3,
    max_value=20,
    value=5
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)


# -------------------------------------------------
# INPUT METHOD
# -------------------------------------------------

st.subheader("📚 Choose Study Material")

input_method = st.radio(
    "Input method:",
    [
        "Enter Topic",
        "Paste Notes",
        "Upload PDF"
    ]
)


topic = ""
notes = ""


# -------------------------------------------------
# ENTER TOPIC
# -------------------------------------------------

if input_method == "Enter Topic":

    topic = st.text_input(
        "Enter your topic",
        placeholder="Example: Python Basics"
    )

    if topic:
        notes = topic


# -------------------------------------------------
# PASTE NOTES
# -------------------------------------------------

elif input_method == "Paste Notes":

    notes = st.text_area(
        "Paste your study notes",
        height=250,
        placeholder="Paste your notes here..."
    )

    topic = "Study Notes"


# -------------------------------------------------
# UPLOAD PDF
# -------------------------------------------------

elif input_method == "Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("PDF uploaded successfully.")

        notes = extract_pdf_text(uploaded_file)

        topic = uploaded_file.name

        if notes:

            st.info(
                f"Extracted approximately {len(notes)} characters from the PDF."
            )

            with st.expander("Preview extracted text"):

                st.write(notes[:3000])


# -------------------------------------------------
# GENERATE BUTTON
# -------------------------------------------------

st.divider()

if st.button(
    "✨ Generate Flashcards",
    use_container_width=True
):

    if not notes.strip():

        st.warning(
            "Please enter a topic, paste notes, or upload a PDF."
        )

    else:

        with st.spinner("🤖 AI is generating flashcards..."):

            cards = generate_flashcards(
                topic,
                notes,
                number_of_cards,
                difficulty
            )

        if cards:

            st.session_state.flashcards = cards
            st.session_state.current_card = 0
            st.session_state.show_answer = False

            st.success(
                f"✅ {len(cards)} flashcards generated successfully!"
            )


# -------------------------------------------------
# DISPLAY FLASHCARDS
# -------------------------------------------------

if st.session_state.flashcards:

    cards = st.session_state.flashcards

    current = st.session_state.current_card

    total = len(cards)

    card = cards[current]

    st.divider()

    st.subheader(
        f"📖 Flashcard {current + 1} of {total}"
    )

    # Progress bar
    st.progress(
        (current + 1) / total
    )

    # Question
    st.markdown("### ❓ Question")

    st.info(card["question"])

    # Answer
    if st.session_state.show_answer:

        st.markdown("### ✅ Answer")

        st.success(card["answer"])

        if st.button("🙈 Hide Answer"):

            st.session_state.show_answer = False

            st.rerun()

    else:

        if st.button("👀 Show Answer"):

            st.session_state.show_answer = True

            st.rerun()


    # -------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True
        ):

            if current > 0:

                st.session_state.current_card -= 1
                st.session_state.show_answer = False

                st.rerun()

    with col2:

        if st.button(
            "Next ➡️",
            use_container_width=True
        ):

            if current < total - 1:

                st.session_state.current_card += 1
                st.session_state.show_answer = False

                st.rerun()


    # -------------------------------------------------
    # CLEAR FLASHCARDS
    # -------------------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear Flashcards",
        use_container_width=True
    ):

        st.session_state.flashcards = []
        st.session_state.current_card = 0
        st.session_state.show_answer = False

        st.rerun()


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "🧠 AI-Powered Flashcard Generator | "
    "Python + Streamlit + Ollama + PyPDF"
)