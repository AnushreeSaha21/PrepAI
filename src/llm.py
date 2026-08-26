import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

from src.models import (
    CandidateProfile,
    JobProfile,
    SkillRelationship,
    InterviewQuestion,
    QuestionSet,
    Project,
    AnswerEvaluation
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


class SkillMatchingResult(BaseModel):
    relationships: list[SkillRelationship] = Field(
        default_factory=list
    )

def extract_candidate_profile(resume_text: str) -> CandidateProfile:

    prompt = f"""
You are an expert resume information extraction system.

Extract the candidate's information from the resume below.

Important rules:
- Do not invent information.
- If a field is not present, leave it empty.
- Preserve the meaning of the original resume.
- Extract technical skills separately.
- Extract each project separately.
- Extract each work experience separately.
- Keep descriptions concise but informative.

RESUME:
----------------
{resume_text}
----------------
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CandidateProfile,
        },
    )

    return CandidateProfile.model_validate_json(response.text)


def extract_job_profile(jd_text: str) -> JobProfile:

    prompt = f"""
You are an expert job description information extraction system.

Extract the important information from the job description below.

Rules:
- Do not invent requirements that are not present.
- Separate required skills from preferred/nice-to-have skills.
- Extract the major responsibilities of the role.
- Extract educational and experience qualifications.
- Keep the extracted information concise.
- Return only information supported by the job description.

JOB DESCRIPTION:
----------------
{jd_text}
----------------
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JobProfile,
        },
    )

    return JobProfile.model_validate_json(response.text)



def evaluate_skill_relationship(
    candidate_skill: str,
    job_skill: str
) -> SkillRelationship:

    prompt = f"""
You are evaluating whether a candidate's skill satisfies
a job requirement.

Candidate skill:
{candidate_skill}

Job requirement:
{job_skill}

Classify the relationship using exactly one of:

- direct: The candidate explicitly has the same skill.
- covered: The candidate has a broader skill, technology,
  framework, stack, or experience that clearly includes
  the job requirement.
- related: The skills are related, but the candidate's skill
  does not clearly demonstrate the required skill.
- missing: The candidate's skill does not satisfy or meaningfully
  relate to the job requirement.

Important:
- Do not assume skills that are not reasonably implied.
- Do not treat merely similar-looking names as equivalent.
- Java and JavaScript are different.
- MERN includes React.js and Node.js.
- Give a confidence score between 0 and 1.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SkillRelationship,
        },
    )

    return SkillRelationship.model_validate_json(response.text)


def evaluate_skill_relationships(
    candidate_skills: list[str],
    job_skills: list[str]
) -> SkillMatchingResult:

    prompt = f"""
You are an expert technical recruiter.

Compare the candidate's skills against the job requirements.

Candidate skills:
{candidate_skills}

Job requirements:
{job_skills}

For each job requirement, determine whether it is:

direct:
The candidate explicitly has the same skill.

covered:
The candidate has a broader technology, framework,
stack, or experience that clearly includes the requirement.

related:
The candidate has a related skill, but it does not
clearly demonstrate the required skill.

missing:
The candidate does not have a skill that satisfies
the requirement.

Important examples:
- MERN Stack covers React.js.
- MERN Stack covers Node.js.
- Python does not cover Java.
- Java does not cover JavaScript.
- Machine Learning does not automatically mean
  experience with every ML framework.

Return one relationship for every job requirement.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SkillMatchingResult,
        },
    )

    return SkillMatchingResult.model_validate_json(
        response.text
    )


def generate_interview_questions(
    candidate: CandidateProfile,
    job: JobProfile,
    match_result: dict
) -> QuestionSet:

    prompt = f"""
You are an expert technical interviewer.

Your task is to generate a personalized interview question set
for a candidate applying to a specific job.

CANDIDATE PROFILE:
{candidate.model_dump_json(indent=2)}

JOB PROFILE:
{job.model_dump_json(indent=2)}

MATCH ANALYSIS:
{match_result}

Generate exactly 10 questions.

Distribute them across these categories:

1. resume_project
   Questions specifically about projects or experience
   mentioned in the candidate's resume.

2. jd_technical
   Questions testing skills explicitly required by the
   job description.

3. jd_gap
   Questions targeting important required skills that are
   missing or weak in the candidate profile.

4. fundamentals
   General technical fundamentals relevant to the role.

Guidelines:
- Questions must be specific to this candidate and role.
- Do not invent projects, technologies, or experience.
- Resume-based questions must be grounded in the candidate profile.
- JD-gap questions should focus on genuine gaps from the match analysis.
- Avoid duplicate questions.
- Mix easy, medium, and hard questions.
- Prefer questions that require explanation or reasoning rather
  than simple definitions.

Return exactly 10 questions.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": QuestionSet,
        },
    )

    return QuestionSet.model_validate_json(
        response.text
    )


def evaluate_answer(
    question: InterviewQuestion,
    answer: str
) -> AnswerEvaluation:

    prompt = f"""
You are an expert technical interviewer evaluating
a candidate's interview answer.

QUESTION:
{question.question}

CATEGORY:
{question.category}

DIFFICULTY:
{question.difficulty}

CANDIDATE ANSWER:
{answer}

Evaluate the answer using these dimensions:

1. correctness
   Is the answer factually and conceptually correct?

2. technical_depth
   Does the candidate demonstrate sufficient understanding
   rather than giving a superficial answer?

3. clarity
   Is the answer understandable, structured and concise?

Scoring:
0-2 = very poor
3-4 = weak
5-6 = partially satisfactory
7-8 = good
9-10 = excellent

Important:
- Do not penalize the candidate for using different wording
  from an expected answer.
- Give credit for valid alternative explanations.
- Do not invent errors that are not present.
- Clearly identify missing important concepts.
- Keep feedback constructive.

Return a structured evaluation.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": AnswerEvaluation,
        },
    )

    return AnswerEvaluation.model_validate_json(
        response.text
    )

if __name__ == "__main__":

    question = InterviewQuestion(
        question=(
            "Explain the difference between RAG "
            "and fine-tuning."
        ),
        category="fundamentals",
        difficulty="medium",
        source="LLM fundamentals"
    )

    answer = """
    RAG retrieves relevant external information and gives it
    to the language model as context. Fine tuning changes the
    model weights by training the model on additional examples.
    RAG is useful when the external knowledge changes frequently,
    while fine tuning is more useful for adapting model behavior.
    """

    evaluation = evaluate_answer(
        question,
        answer
    )

    print(
        evaluation.model_dump_json(
            indent=2
        )
    )