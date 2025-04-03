
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pdfkit
from jinja2 import Template
import tempfile

# --- Helper Functions ---
def load_data(file):
    return pd.read_csv(file)

def process_data(df):
    pivot = df.pivot_table(index='Student', columns='Standard', values='Score')
    return pivot

def generate_feedback(row, threshold=70):
    feedback = []
    for standard, score in row.items():
        if pd.isna(score):
            continue
        if score < threshold:
            feedback.append(f"Needs review on {standard} (Score: {score}%)")
        else:
            feedback.append(f"Mastery on {standard} (Score: {score}%)")
    return feedback

def render_pdf(student, feedback):
    template = Template("""
    <h1>Feedback Report for {{ name }}</h1>
    <ul>
    {% for item in feedback %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
    """)
    html = template.render(name=student, feedback=feedback)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        pdfkit.from_string(html, f.name)
        return f.name

# --- Streamlit App ---
st.title("🎯 Student Mastery Tracker")
st.markdown("Upload your CSV file with student scores by standard.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("### Raw Data", df)

    pivot_df = process_data(df)
    st.write("### Student Performance Table", pivot_df)

    st.write("### Class Performance Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    student_choice = st.selectbox("Select a student to view detailed feedback:", pivot_df.index)

    if student_choice:
        student_scores = pivot_df.loc[student_choice]
        feedback = generate_feedback(student_scores)
        st.write("### Feedback:")
        for item in feedback:
            st.markdown(f"- {item}")

        if st.button("Export Feedback as PDF"):
            pdf_path = render_pdf(student_choice, feedback)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=f"{student_choice}_feedback.pdf")

    st.write("### Individual Student Growth")
    melted_df = df.pivot_table(index='Student', columns='Standard', values='Score').reset_index().melt(id_vars='Student')
    fig2, ax2 = plt.subplots()
    sns.barplot(x='variable', y='value', hue='Student', data=melted_df, ax=ax2)
    ax2.set_ylabel("Score")
    ax2.set_xlabel("Standard")
    ax2.set_title("Scores by Standard")
    st.pyplot(fig2)

    st.write("### Editable Notes Table (Experimental)")
    notes_df = pivot_df.copy()
    for student in notes_df.index:
        notes_df.loc[student, 'Notes'] = st.text_area(f"Notes for {student}", "")
    st.write(notes_df)
