import streamlit as st

from src.pdf_parser import extract_text_from_pdf
from src.llm import (
    extract_candidate_profile,
    extract_job_profile,
    generate_interview_questions,
    evaluate_answer,
    generate_follow_up_question
)
from src.analytics import (
    calculate_readiness,
    identify_strengths
)
from src.pdf_report import generate_interview_report
from src.matcher import match_candidate_to_job


st.set_page_config(
    page_title="PrepAI",
    page_icon="🤖",
    layout="wide"
)
MAX_QUESTIONS = 10
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

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "interview_mode" not in st.session_state:
    st.session_state.interview_mode = "Adaptive"

if "is_adaptive_question" not in st.session_state:
    st.session_state.is_adaptive_question = False

if "active_section" not in st.session_state:
    st.session_state.active_section = "📄 Profile"

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

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

interview_mode = st.radio(
    "Interview Mode",
    [
        "Easy → Medium",
        "Medium → Hard",
        "Adaptive"
    ],
    horizontal=True
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
                match_result,
                interview_mode
            )

        st.session_state.candidate_profile = candidate_profile
        st.session_state.job_profile = job_profile
        st.session_state.match_result = match_result
        st.session_state.questions = question_set.questions
        st.session_state.current_question = 0
        st.session_state.evaluations = []
        st.session_state.interview_mode = interview_mode
        st.session_state.is_adaptive_question = False
        st.session_state.last_evaluation = None
        st.session_state.last_answer = None
        st.session_state.active_section = "🎤 Interview"
        st.session_state.interview_history = []

        st.success(
            f"Generated {len(question_set.questions)} personalized questions!"
        )
        
        # --------------------------------------------------
        # DISPLAY PROFILE
        # --------------------------------------------------
if st.session_state.candidate_profile is not None:

    candidate_profile = st.session_state.candidate_profile
    job_profile = st.session_state.job_profile
    match_result = st.session_state.match_result

    

    active_section = st.segmented_control(
        "Navigation",
        [
            "📄 Profile",
            "🎯 Job Match",
            "🎤 Interview",
            "📊 Results"
        ],
        key="active_section",
        label_visibility="collapsed"
    )
    if active_section == "📄 Profile":

            st.header("Candidate Profile")

            st.subheader("Name")
            st.write(candidate_profile.name)

            st.subheader("Education")

            for education in candidate_profile.education:
                st.write(f"- {education}")

            st.subheader("Skills")

            if candidate_profile.skills:
                st.write(", ".join(candidate_profile.skills))
            else:
                st.write("No skills extracted.")

            st.subheader("Experience")

            if candidate_profile.experience:

                for experience in candidate_profile.experience:

                    st.markdown(
                        f"""
                        **{experience.role} — {experience.company}**

                        {experience.description}
                        """
                    )

            else:
                st.write("No experience extracted.")

            st.subheader("Projects")

            if candidate_profile.projects:

                for project in candidate_profile.projects:

                    st.markdown(
                        f"""
                        **{project.name}**

                        **Technologies:** {", ".join(project.technologies)}

                        {project.description}
                        """
                    )

            else:
                st.write("No projects extracted.")

            st.subheader("Certifications")

            if candidate_profile.certifications:

                for certification in candidate_profile.certifications:
                    st.write(f"- {certification}")

            else:
                st.write("No certifications extracted.")

            st.subheader("Achievements")

            if candidate_profile.achievements:

                for achievement in candidate_profile.achievements:
                    st.write(f"- {achievement}")

            else:
                st.write("No achievements extracted.")



                st.divider()

    elif active_section == "🎯 Job Match":

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

                if match_result["matched_required"]:

                    for skill in match_result["matched_required"]:
                        st.write(f"✓ {skill}")

                else:
                    st.write("No required skills matched.")

            with col2:

                st.subheader("⚠️ Missing Required Skills")

                if match_result["missing_required"]:

                    for skill in match_result["missing_required"]:
                        st.write(f"• {skill}")

                else:
                    st.write("No missing required skills.")

            st.subheader("⭐ Matched Preferred Skills")

            if match_result["matched_preferred"]:

                for skill in match_result["matched_preferred"]:
                    st.write(f"✓ {skill}")

            else:
                st.write("None.")

            st.subheader("📚 Missing Preferred Skills")

            if match_result["missing_preferred"]:

                for skill in match_result["missing_preferred"]:
                    st.write(f"• {skill}")

            else:
                st.write("None.")


# --------------------------------------------------
# INTERVIEW
# --------------------------------------------------

    elif active_section == "🎤 Interview":

        if st.session_state.questions:

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

                if st.session_state.is_adaptive_question:

                    st.info(
                        "This question was generated based on "
                        "your previous interview response."
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
                        st.session_state.last_answer = answer
                        st.session_state.evaluations.append(
                                    evaluation
                        )
                        st.session_state.interview_history.append({
                            "question": current_question,
                            "answer": answer,
                            "evaluation": evaluation
                        })

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

                        next_index = (
                            st.session_state.current_question + 1
                        )

                        # ----------------------------------------------
                        # Interview finished
                        # ----------------------------------------------

                        if next_index >= MAX_QUESTIONS:

                            st.session_state.current_question = MAX_QUESTIONS
                            st.session_state.last_evaluation = None
                            st.session_state.last_answer = None

                            st.rerun()

                        else:
                            # --------------------------------------------------
                            # ADAPTIVE MODE
                            # --------------------------------------------------

                            if st.session_state.interview_mode == "Adaptive":

                                score = evaluation.overall_score

                                if score < 5:
                                    next_difficulty = "easy"

                                elif score < 8:
                                    next_difficulty = "medium"

                                else:
                                    next_difficulty = "hard"

                                with st.spinner(
                                    f"Generating {next_difficulty} follow-up..."
                                ):

                                    next_question = generate_follow_up_question(
                                        question=current_question,
                                        answer=st.session_state.last_answer,
                                        evaluation=evaluation,
                                        candidate=st.session_state.candidate_profile,
                                        job=st.session_state.job_profile,
                                        next_difficulty=next_difficulty
                                    )

                                st.session_state.questions[next_index] = (
                                    next_question
                                )

                                st.session_state.is_adaptive_question = True

                            # --------------------------------------------------
                            # FIXED DIFFICULTY MODES
                            # --------------------------------------------------
                            else:
                                st.session_state.is_adaptive_question = False

                            st.session_state.current_question = next_index

                            st.session_state.last_evaluation = None
                            st.session_state.last_answer = None

                            st.rerun()

    elif active_section == "📊 Results":


        st.header("📊 Interview Readiness")

        evaluations = st.session_state.evaluations
        questions = st.session_state.questions
        category_names = {
            "resume_project": "Resume / Projects",
            "jd_technical": "JD Technical",
            "jd_gap": "JD Skill Gaps",
            "fundamentals": "Fundamentals"
        }

        # ----------------------------------------------
        # Check whether interview is complete
        # ----------------------------------------------

        if len(evaluations) == 0:

            st.info(
                "Complete at least one interview question "
                "to see your readiness analysis."
            )

        else:

            readiness = calculate_readiness(
                evaluations,
                questions
            )

            # ------------------------------------------
            # Overall readiness
            # ------------------------------------------

            st.subheader("Overall Readiness")

            overall = readiness["overall"]

            st.metric(
                "Readiness Score",
                f"{overall:.1f} / 10"
            )

            st.progress(
                min(overall / 10, 1.0)
            )

            # ------------------------------------------
            # Core dimensions
            # ------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Correctness",
                f"{readiness['correctness']:.1f}/10"
            )

            col2.metric(
                "Technical Depth",
                f"{readiness['technical_depth']:.1f}/10"
            )

            col3.metric(
                "Clarity",
                f"{readiness['clarity']:.1f}/10"
            )

            col4.metric(
                "Questions Answered",
                len(evaluations)
            )

            st.divider()

            # ------------------------------------------
            # Category scores
            # ------------------------------------------

            st.subheader("Performance by Category")

            for category, score in readiness["categories"].items():

                display_name = category_names.get(
                    category,
                    category.replace("_", " ").title()
                )

                st.write(
                    f"**{display_name}** — "
                    f"{score:.1f}/10"
                )

                st.progress(
                    min(score / 10, 1.0)
                )

            # ------------------------------------------
            # Missing concepts
            # ------------------------------------------

            st.subheader("📚 Areas to Improve")

            if readiness["missing_concepts"]:

                # Remove duplicates while
                # preserving order

                unique_concepts = list(
                    dict.fromkeys(
                        readiness["missing_concepts"]
                    )
                )

                for concept in unique_concepts:
                    st.write(f"• {concept}")

            else:

                st.write(
                    "No major missing concepts identified."
                )


            strengths = identify_strengths(readiness)

            st.subheader("💪 Strengths")

            if strengths:

                for strength in strengths:
                    st.write(f"✓ {strength}")

            else:

                st.write(
                    "Keep practicing to build stronger response patterns."
                )

            if overall >= 8:

                st.success(
                    "Strong readiness — focus on polishing "
                    "advanced concepts and project depth."
                )

            elif overall >= 6:

                st.warning(
                    "Moderate readiness — strengthen the "
                    "areas highlighted above."
                )

            else:

                st.error(
                    "More preparation recommended — focus "
                    "on fundamentals and identified gaps."
                )


            st.divider()

            st.subheader("📥 Download Interview Report")

            if st.session_state.interview_history:

                pdf_bytes = generate_interview_report(
                    candidate=candidate_profile,
                    job=job_profile,
                    readiness=readiness,
                    interview_history=st.session_state.interview_history,
                )

                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="PrepAI_Interview_Report.pdf",
                    mime="application/pdf",
                )

            else:

                st.info(
                    "Complete at least one interview question "
                    "to generate a report."
                )