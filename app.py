import streamlit as st

from src.pdf_parser import extract_text_from_pdf
from src.llm import (
    extract_candidate_profile,
    extract_job_profile,
    generate_interview_questions,
    evaluate_answer
)

from src.matcher import match_candidate_to_job


st.set_page_config(
    page_title="PrepAI",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "candidate_profile" not in st.session_state:
    st.session_state.candidate_profile = None

if "job_profile" not in st.session_state:
    st.session_state.job_profile = None

if "match_result" not in st.session_state:
    st.session_state.match_result = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

if "last_evaluation" not in st.session_state:
    st.session_state.last_evaluation = None

st.title("🤖 PrepAI")
st.subheader("LLM-Powered Adaptive Interview Readiness System")

st.write(
    "Upload your resume and provide a job description "
    "to begin your interview preparation."
)


# --------------------------------------------------
# INPUTS
# --------------------------------------------------

resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

jd = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the job description here..."
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("Analyze Resume", type="primary"):

    if resume is None:
        st.warning("Please upload your resume first.")

    elif not jd.strip():
        st.warning("Please provide a job description.")

    else:

        with st.spinner("Extracting resume information..."):

            resume_text = extract_text_from_pdf(resume)

        st.success("Resume text extracted successfully!")

        with st.spinner("Analyzing resume with Gemini..."):

            candidate_profile = extract_candidate_profile(
                resume_text
            )

        st.success("Candidate profile generated!")

        with st.spinner("Analyzing job description with Gemini..."):

            job_profile = extract_job_profile(jd)

        st.success("Job profile generated!")

        match_result = match_candidate_to_job(
            candidate_profile,
            job_profile
        )

        st.divider()

        with st.spinner("Generating personalized interview questions..."):

            question_set = generate_interview_questions(
                candidate_profile,
                job_profile,
                match_result
            )

        st.session_state.candidate_profile = candidate_profile
        st.session_state.job_profile = job_profile
        st.session_state.match_result = match_result
        st.session_state.questions = question_set.questions
        st.session_state.current_question = 0
        st.session_state.evaluations = []
        

        st.success(
            f"Generated {len(question_set.questions)} personalized questions!"
        )

        # --------------------------------------------------
        # DISPLAY PROFILE
        # --------------------------------------------------

        st.header("Candidate Profile")

        st.subheader("Name")
        st.write(candidate_profile.name)

        st.subheader("Education")

        for education in candidate_profile.education:
            st.write(f"- {education}")

        st.subheader("Skills")

        st.write(
            ", ".join(candidate_profile.skills)
        )

        st.subheader("Experience")

        for experience in candidate_profile.experience:

            st.markdown(
                f"""
                **{experience.role} — {experience.company}**

                {experience.description}
                """
            )

        st.subheader("Projects")

        for project in candidate_profile.projects:

            st.markdown(
                f"""
                **{project.name}**

                Technologies: {", ".join(project.technologies)}

                {project.description}
                """
            )

        st.subheader("Certifications")

        for certification in candidate_profile.certifications:
            st.write(f"- {certification}")

        st.subheader("Achievements")

        for achievement in candidate_profile.achievements:
            st.write(f"- {achievement}")



        st.divider()

        st.header("Job Profile")

        st.subheader("Role")
        st.write(job_profile.role)

        st.subheader("Required Skills")

        for skill in job_profile.required_skills:
            st.write(f"- {skill}")

        st.subheader("Preferred Skills")

        for skill in job_profile.preferred_skills:
            st.write(f"- {skill}")

        st.subheader("Responsibilities")

        for responsibility in job_profile.responsibilities:
            st.write(f"- {responsibility}")

        st.subheader("Qualifications")

        for qualification in job_profile.qualifications:
            st.write(f"- {qualification}")


        st.divider()

        st.header("🎯 Job Match Analysis")

        st.metric(
            "Required Skill Coverage",
            f"{match_result['required_match_score']}%"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Required Skills")

            for skill in match_result["matched_required"]:
                st.write(f"✓ {skill}")

        with col2:

            st.subheader("⚠️ Missing Required Skills")

            for skill in match_result["missing_required"]:
                st.write(f"• {skill}")


        st.subheader("⭐ Matched Preferred Skills")

        for skill in match_result["matched_preferred"]:
            st.write(f"✓ {skill}")


        st.subheader("📚 Missing Preferred Skills")

        for skill in match_result["missing_preferred"]:
            st.write(f"• {skill}")


# --------------------------------------------------
# INTERVIEW
# --------------------------------------------------

if st.session_state.questions:

    st.divider()

    st.header("🎤 Interview Session")

    current_index = st.session_state.current_question
    questions = st.session_state.questions
    total_questions = len(questions)

    # --------------------------------------------------
    # INTERVIEW COMPLETED
    # --------------------------------------------------

    if current_index >= total_questions:

        st.success("🎉 Interview completed!")

    else:

        current_question = questions[current_index]

        st.caption(
            f"Question {current_index + 1} "
            f"of {total_questions}"
        )

        st.subheader(current_question.question)

        st.write(
                    f"Category: `{current_question.category}`"
        )

        st.write(
                    f"Difficulty: `{current_question.difficulty}`"
        )

        # ----------------------------------------------
        # ANSWER INPUT
        # ----------------------------------------------

        answer = st.text_area(
                    "Your Answer",
                    height=200,
                    key=f"answer_{current_index}"
        )

        # ----------------------------------------------
        # SUBMIT ANSWER
        # ----------------------------------------------

        if st.button(
                    "Submit Answer",
                    type="primary"
        ):

            if not answer.strip():

                st.warning(
                            "Please write an answer first."
                )

            else:

                with st.spinner(
                            "Evaluating your answer..."
                ):

                    evaluation = evaluate_answer(
                                current_question,
                                answer
                    )

                st.session_state.last_evaluation = evaluation

                st.session_state.evaluations.append(
                            evaluation
                )

                st.rerun()

        # ----------------------------------------------
        # DISPLAY EVALUATION
        # ----------------------------------------------

        if st.session_state.last_evaluation is not None:

            evaluation = (
                        st.session_state.last_evaluation
            )

            st.divider()

            st.subheader("📊 Your Evaluation")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                        "Overall",
                        f"{evaluation.overall_score}/10"
            )

            col2.metric(
                        "Correctness",
                        f"{evaluation.correctness}/10"
            )

            col3.metric(
                        "Technical Depth",
                        f"{evaluation.technical_depth}/10"
            )

            col4.metric(
                        "Clarity",
                        f"{evaluation.clarity}/10"
            )

            st.subheader("✅ Strengths")

            for item in evaluation.strengths:
                st.write(f"• {item}")

            st.subheader("⚠️ Areas to Improve")

            for item in evaluation.improvements:
                st.write(f"• {item}")

            st.subheader("📚 Missing Concepts")

            for item in evaluation.missing_concepts:
                st.write(f"• {item}")

            st.subheader("💬 Feedback")

            st.write(evaluation.feedback)

            # ------------------------------------------
            # NEXT QUESTION
            # ------------------------------------------

            if st.button(
                        "Next Question",
                        type="primary"
            ):

                st.session_state.current_question += 1

                st.session_state.last_evaluation = None

                st.rerun()