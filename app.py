import streamlit as st
import time

# Custom Bold CSS Styling
st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; }
    h1 { color: #F59E0B !important; font-weight: 800 !important; }
    .stButton>button { 
        background-color: #3B82F6 !important; 
        color: white !important; 
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
    }
    .stButton>button:hover { background-color: #2563EB !important; }
    .box { 
        background-color: #1E293B; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #F59E0B;
        margin-bottom: 20px;
    }
    .chat-bubble {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .bot-bubble { background-color: #1E293B; border-left: 4px solid #3B82F6; }
    </style>
""", unsafe_allow_html=True)

# 1. BROADENED KNOWLEDGE BASE (4 Core CBSE AI Chapters)
QUIZ_BANK = {
    "Introduction to AI / Project Cycle": [
        {
            "question": "What is the purpose of Data Exploration in the AI Project Cycle?",
            "keywords": {"visualize", "understand", "trends", "patterns", "data", "graph", "analyze", "charts"},
            "model_answer": "To visually analyze and explore gathered data to uncover hidden patterns, trends, and structures before modelling."
        },
        {
            "question": "Name the 5 stages of the AI Project Cycle in correct order.",
            "keywords": {"scoping", "acquisition", "exploration", "modelling", "evaluation"},
            "model_answer": "Problem Scoping, Data Acquisition, Data Exploration, Modelling, and Evaluation."
        }
    ],
    "Natural Language Processing (NLP)": [
        {
            "question": "What is the primary objective of the NLP domain in Artificial Intelligence?",
            "keywords": {"understand", "human", "language", "text", "speech", "process", "natural"},
            "model_answer": "To enable computers to understand, interpret, and manipulate human languages like text or speech."
        },
        {
            "question": "Explain what 'Tokenization' means in an NLP pipeline.",
            "keywords": {"breaking", "split", "text", "sentences", "words", "tokens", "smaller"},
            "model_answer": "Tokenization is the process of breaking down a large text corpus into smaller parts called tokens, such as words."
        }
    ],
    "Computer Vision (CV)": [
        {
            "question": "What is Computer Vision and give one real-world application of it.",
            "keywords": {"see", "interpret", "visual", "images", "videos", "facial", "recognition", "cars", "medical"},
            "model_answer": "Computer Vision enables computers to see and interpret visual data from digital images or videos. Applications include autonomous cars and facial recognition."
        },
        {
            "question": "How do computers process color images under the hood?",
            "keywords": {"pixels", "rgb", "red", "green", "blue", "channels", "matrix", "numbers"},
            "model_answer": "Computers see color images as numeric grids or matrices of pixels split across three core color channels: Red, Green, and Blue (RGB)."
        }
    ],
    "Data Science & AI Evaluation": [
        {
            "question": "Define what a 'Confusion Matrix' is in AI evaluation.",
            "keywords": {"table", "performance", "classification", "actual", "predicted", "accuracy"},
            "model_answer": "A Confusion Matrix is an evaluation table used to describe the performance of a classification model by comparing actual values with predicted values."
        },
        {
            "question": "What is the difference between Overfitting and Underfitting?",
            "keywords": {"overfitting", "training", "testing", "fails", "generalize", "poor", "high"},
            "model_answer": "Overfitting happens when a model performs exceptionally well on training data but poorly on unseen test data. Underfitting happens when the model is too simple to learn the basic patterns at all."
        }
    ]
}

DOUBT_RESOLVER = {
    "nlp": "Natural Language Processing (NLP) helps computers understand human text/speech. Key steps: Tokenization, Stemming, Lemmatization, Bag of Words.",
    "project cycle": "AI Project Cycle: 1. Problem Scoping, 2. Data Acquisition, 3. Data Exploration, 4. Modelling, 5. Evaluation.",
    "tokenization": "Tokenization breaks a long paragraph or sentence down into individual units called tokens. E.g., 'Learn AI' -> ['Learn', 'AI'].",
    "computer vision": "Computer Vision (CV) lets computers interpret visual inputs like digital photos or videos (e.g., self-driving cars).",
    "data science": "Data Science focuses on working with massive datasets, cleaning them, and extracting smart patterns using statistical algorithms.",
    "evaluation": "Evaluation is the final stage where we calculate metrics like Accuracy, Precision, Recall, and F1 Score to see how reliable our AI model is."
}

# 2. NLP SIMILARITY ENGINE
def evaluate_answer(user_ans, correct_keywords):
    cleaned = "".join([char.lower() for char in user_ans if char.isalnum() or char.isspace()])
    user_tokens = set(cleaned.split())
    matched_keywords = user_tokens.intersection(correct_keywords)
    return len(matched_keywords) / len(correct_keywords) if correct_keywords else 0.0

# 3. INTERFACE & STATE MANAGEMENT
st.title("⚡ AI Quiz & Revision Companion")

if "mode" not in st.session_state:
    st.session_state.mode = "menu"
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.selected_topic = ""

# --- MAIN MENU MODE ---
if st.session_state.mode == "menu":
    st.markdown("<div class='box'>👋 <b>Hello Student!</b> How can I help you revise today? Select an option below:</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Take a Revision Quiz"):
            st.session_state.mode = "quiz_setup"
            st.rerun()
    with col2:
        if st.button("❓ Ask a Doubt"):
            st.session_state.mode = "doubt"
            st.rerun()

# --- QUIZ SETUP MODE ---
elif st.session_state.mode == "quiz_setup":
    st.subheader("Select your Revision Topic:")
    topic = st.selectbox("Choose a chapter from the AI Syllabus:", list(QUIZ_BANK.keys()))
    
    if st.button("Start Quiz 🚀"):
        # BUG FIX: Explicitly clear out old session states before starting a fresh quiz!
        for key in list(st.session_state.keys()):
            if key.startswith("evaluated_") or key.startswith("score_ratio_"):
                del st.session_state[key]
                
        st.session_state.selected_topic = topic
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.mode = "quiz"
        st.rerun()
        
    if st.button("⬅️ Back to Menu"):
        st.session_state.mode = "menu"
        st.rerun()

# --- ACTIVE QUIZ MODE ---
elif st.session_state.mode == "quiz":
    questions = QUIZ_BANK[st.session_state.selected_topic]
    q_idx = st.session_state.current_q
    
    st.markdown(f"<div class='box'><b>Topic:</b> {st.session_state.selected_topic} | <b>Progress:</b> Q {q_idx + 1}/{len(questions)} | <b>Score:</b> {st.session_state.score}</div>", unsafe_allow_html=True)
    
    st.subheader(f"Q: {questions[q_idx]['question']}")
    
    student_response = st.text_area("Type your evaluation answer:", key=f"quiz_ans_{q_idx}")
    
    if f"evaluated_{q_idx}" not in st.session_state:
        st.session_state[f"evaluated_{q_idx}"] = False
        st.session_state[f"score_ratio_{q_idx}"] = 0.0

    # Step A: Submit Answer Process
    if not st.session_state[f"evaluated_{q_idx}"]:
        if st.button("Submit Answer"):
            if student_response.strip() != "":
                score_ratio = evaluate_answer(student_response, questions[q_idx]["keywords"])
                st.session_state[f"score_ratio_{q_idx}"] = score_ratio
                
                if score_ratio >= 0.4:
                    st.session_state.score += 10
                elif score_ratio >= 0.15:
                    st.session_state.score += 5
                
                st.session_state[f"evaluated_{q_idx}"] = True
                st.rerun()
            else:
                st.warning("Please type an answer before submitting!")

    # Step B: Static Result Frame & Manual Gateway Button
    if st.session_state[f"evaluated_{q_idx}"]:
        score_ratio = st.session_state[f"score_ratio_{q_idx}"]
        
        if score_ratio >= 0.4:
            st.success(f"🎉 Correct! (NLP Match: {score_ratio*100:.1f}%)")
        elif score_ratio >= 0.15:
            st.info(f"⚠️ Partially Correct. (NLP Match: {score_ratio*100:.1f}%)")
        else:
            st.error("❌ Incorrect concept mapping.")
            
        st.markdown(f"**Model Answer Reference:**\n*{questions[q_idx]['model_answer']}*")
        
        st.markdown("---")
        if st.button("Next Question ➡️"):
            if q_idx < len(questions) - 1:
                st.session_state.current_q += 1
            else:
                st.balloons()
                st.success(f"🏁 Completed! Total Score: {st.session_state.score} points.")
                time.sleep(2.0)
                st.session_state.mode = "menu"
            st.rerun()

# --- DOUBT RESOLVER MODE ---
elif st.session_state.mode == "doubt":
    st.subheader("🤖 AI Doubt Assistant")
    st.markdown("Type a keyword or concept you want to understand (e.g., *NLP, Computer Vision, Project Cycle, Data Science, Evaluation*):")
    
    user_query = st.text_input("Your Doubt:", placeholder="What do you want to learn about?")
    
    if user_query:
        matched = False
        query_clean = user_query.lower()
        
        for key, explanation in DOUBT_RESOLVER.items():
            if key in query_clean:
                st.markdown(f"<div class='chat-bubble bot-bubble'><b>Bot Explains:</b> {explanation}</div>", unsafe_allow_html=True)
                matched = True
                break
                
        if not matched:
            st.markdown("<div class='chat-bubble bot-bubble'><b>Bot:</b> I'm currently trained on specific syllabus topics. Try asking about <i>NLP, Evaluation, Computer Vision, Data Science</i> or the <i>Project Cycle</i>!</div>", unsafe_allow_html=True)
            
    if st.button("⬅️ Return to Main Menu"):
        st.session_state.mode = "menu"
        st.rerun()