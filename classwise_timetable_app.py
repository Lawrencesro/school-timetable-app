import streamlit as st
import pandas as pd
import random
from collections import defaultdict

st.set_page_config(page_title="Class-wise Timetable Generator", layout="wide")
st.title("📚 Class-wise School Timetable Generator")

# Define constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS_PER_DAY = [9, 9, 9, 9, 9, 5]  # Periods per day

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
    st.session_state.entries.append((teacher.strip(), subject.strip(), class_name.strip(), int(periods)))
    st.success(f"Added: {subject} ({class_name}) by {teacher} for {periods} periods/week.")

# Display current entries
if st.session_state.entries:
    st.subheader("🧾 Current Assignments")
    df = pd.DataFrame(st.session_state.entries, columns=["Teacher", "Subject", "Class", "Periods/Week"])
    st.dataframe(df, use_container_width=True)

# Timetable generation function
def generate_classwise_timetables(entries):
    class_timetables = {}
    teacher_schedule = defaultdict(lambda: {day: [False] * PERIODS_PER_DAY[i] for i, day in enumerate(DAYS)})
    
    # Group entries by class
    class_subjects = defaultdict(list)
    for teacher, subject, class_name, count in entries:
        class_subjects[class_name].append((teacher, subject, count))

    for class_name, subjects in class_subjects.items():
        timetable = {day: [""] * PERIODS_PER_DAY[i] for i, day in enumerate(DAYS)}
        slots = [(day, p) for i, day in enumerate(DAYS) for p in range(PERIODS_PER_DAY[i])]
        random.shuffle(slots)

        for teacher, subject, count in subjects:
            assigned = 0
            for day, period in slots:
                if assigned >= count:
                    break
                if timetable[day][period] == "" and not teacher_schedule[teacher][day][period]:
                    timetable[day][period] = f"{subject} - {teacher}"
                    teacher_schedule[teacher][day][period] = True
                    assigned += 1
        class_timetables[class_name] = timetable

    return class_timetables

# Generate timetables
if st.button("📅 Generate Class-wise Timetables"):
    st.session_state.classwise = generate_classwise_timetables(st.session_state.entries)

# Display timetables
if "classwise" in st.session_state:
    st.subheader("📘 Class-wise Timetables")
    for class_name, timetable in st.session_state.classwise.items():
        st.markdown(f"### 🏫 Class: {class_name}")
        df = pd.DataFrame.from_dict(timetable, orient="index")
        df.columns = [f"P{i+1}" for i in range(df.shape[1])]
        st.dataframe(df, use_container_width=True)

# Reset button
if st.button("🔄 Reset All"):
    st.session_state.entries = []
    if "classwise" in st.session_state:
        del st.session_state.classwise
    st.experimental_rerun()
