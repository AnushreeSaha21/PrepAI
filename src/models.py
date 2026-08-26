from pydantic import BaseModel, Field


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class Project(BaseModel):
    name: str = ""
    technologies: list[str] = Field(default_factory=list)
    description: str = ""


class CandidateProfile(BaseModel):
    name: str = ""
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)


class JobProfile(BaseModel):
    role: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    qualifications: list[str] = Field(default_factory=list)


class SkillRelationship(BaseModel):
    candidate_skill: str
    job_skill: str
    relationship: str
    confidence: float
    reason: str


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str
    source: str


class QuestionSet(BaseModel):
    questions: list[InterviewQuestion] = Field(
        default_factory=list
    )


class AnswerEvaluation(BaseModel):
    overall_score: float
    correctness: float
    technical_depth: float
    clarity: float
    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    missing_concepts: list[str] = Field(default_factory=list)
    feedback: str = ""