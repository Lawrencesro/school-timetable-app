
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Auto Timetable Generator", layout="wide")
st.title("📅 School Timetable Generator")

# Input section
st.header("Step 1: Enter Teacher Assignments")
with st.form("teacher_input_form"):
    teacher = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    class_name = st.text_input("Class")
    periods = st.number_input("Periods per week", min_value=1, step=1)
    submitted = st.form_submit_button("Add Entry")

# Session state to store entries
if "entries" not in st.session_state:
    st.session_state.entries = []

if submitted and teacher and subject and class_name:
    st.session_state.entries.append((teacher, subject, class_name, periods))
    st.success(f"Added {subject} ({class_name}) by {teacher} for {periods} periods.")

# Display current entries
if st.session_state.entries:
    st.subheader("📋 Current Entries")
    df = pd.DataFrame(st.session_state.entries, columns=["Teacher", "Subject", "Class", "Periods/Week"])
    st.dataframe(df, use_container_width=True)

# Timetable generation
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS_PER_DAY = [9, 9, 9, 9, 9, 5]

def generate_timetable(entries):
    timetable = {day: ["" for _ in range(PERIODS_PER_DAY[i])] for i, day in enumerate(DAYS)}
    slots = []
    for i, day in enumerate(DAYS):
        for p in range(PERIODS_PER_DAY[i]):
            slots.append((day, p))
    random.shuffle(slots)

    for teacher, subject, class_name, count in entries:
        assigned = 0
        for slot in slots:
            if assigned >= count:
                break
            if timetable[slot[0]][slot[1]] == "":
                timetable[slot[0]][slot[1]] = f"{subject} ({class_name}) - {teacher}"
                assigned += 1
    return timetable

# Generate timetable button
if st.button("🧠 Generate Timetable"):
    st.session_state.generated = generate_timetable(st.session_state.entries)

# Show timetable
if "generated" in st.session_state:
    st.subheader("📆 Weekly Timetable")
    for day in DAYS:
        st.markdown(f"### {day}")
        cols = st.columns(PERIODS_PER_DAY[DAYS.index(day)])
        for i, col in enumerate(cols):
            val = st.session_state.generated[day][i]
            col.markdown(f"**P{i+1}**<br>{val if val else '-'}", unsafe_allow_html=True)

# Reset button
if st.button("🔄 Reset All"):
    st.session_state.entries = []
    if "generated" in st.session_state:
        del st.session_state.generated
    st.experimental_rerun()
