# 🤖 PrepAI — LLM-Powered Adaptive Interview Readiness System

PrepAI is an **LLM-powered interview preparation platform** that analyzes a candidate's resume against a target job description, generates personalized interview questions, evaluates responses using an **LLM-as-a-Judge** approach, and adapts subsequent questions based on the candidate's performance.

The system is designed to help candidates identify their strengths, understand job-specific skill gaps, and practice role-focused technical interviews.

---

## 🚀 Features

### 📄 Resume Analysis
- Upload a resume in PDF format.
- Extract resume text using **PyMuPDF**.
- Use **Gemini LLM** to convert unstructured resume text into a structured candidate profile.
- Extract:
  - Education
  - Skills
  - Work Experience
  - Projects
  - Certifications
  - Achievements

### 💼 Job Description Analysis
- Paste a job description directly into the application.
- Extract structured role information using Gemini.
- Identify:
  - Required skills
  - Preferred skills
  - Responsibilities
  - Qualifications

### 🎯 Intelligent Skill Matching
The system compares candidate skills with job requirements using a hybrid approach:

1. **Exact matching** using Python set operations.
2. **Semantic matching** using Gemini for cases where skills are related but not identical.

For example:

```text
Candidate: MERN Stack
Job Requirement: React.js

→ Covered through MERN Stack
