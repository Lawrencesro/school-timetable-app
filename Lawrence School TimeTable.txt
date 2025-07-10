import streamlit as st
import pandas as pd
import random
from collections import defaultdict

st.set_page_config(page_title="📚 Class-wise Timetable from Excel", layout="wide")
st.title("📥 Upload Excel → 📘 Get Class-wise Timetables")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS_PER_DAY = [9, 9, 9, 9, 9, 5]

# Upload Excel
uploaded_file = st.file_uploader("📤 Upload Excel with Teacher Assignments", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Assignments")
        df.columns = [col.strip() for col in df.columns]
        st.success("✅ Excel uploaded and read successfully.")
        st.write(df)

        # Validate structure
        required_cols = {"Teacher Name", "Subject", "Class", "Periods/Week"}
        if not required_cols.issubset(set(df.columns)):
            st.error("❌ Missing required columns.")
        else:
            entries = []
            for row in df.itertuples(index=False):
                entries.append((str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip(), int(row[3])))

            # Generate Timetables
            def generate_classwise_timetables(entries):
                class_timetables = {}
                teacher_schedule = defaultdict(lambda: {day: [False] * PERIODS_PER_DAY[i] for i, day in enumerate(DAYS)})
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

            if st.button("📅 Generate Class-wise Timetables"):
                results = generate_classwise_timetables(entries)
                for class_name, timetable in results.items():
                    st.markdown(f"### 🏫 Timetable for Class {class_name}")
                    df_tt = pd.DataFrame.from_dict(timetable, orient="index")
                    df_tt.columns = [f"P{i+1}" for i in range(df_tt.shape[1])]
                    st.dataframe(df_tt, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading Excel: {e}")
else:
    st.info("📄 Please upload an Excel file with columns: Teacher Name, Subject, Class, Periods/Week (Sheet name: Assignments)")
