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
```

while:

```text
Candidate: MERN Stack
Job Requirement: AWS

→ Missing
```

This helps avoid false negatives caused by simple string matching.

### 🧠 Personalized Interview Question Generation
PrepAI generates role-specific questions using:
- Candidate profile
- Job profile
- Skill-match analysis
- Candidate projects and experience

Questions are categorized into:
- `resume_project`
- `jd_technical`
- `jd_gap`
- `fundamentals`

### 🎚️ Interview Modes

#### Easy → Medium
Starts with easier questions and gradually moves to medium difficulty.

```text
Q1–Q5 → Easy
Q6–Q10 → Medium
```

#### Medium → Hard
Starts at medium difficulty and progresses to harder questions.

```text
Q1–Q5 → Medium
Q6–Q10 → Hard
```

#### Adaptive
Question difficulty is dynamically determined from the candidate's previous performance.

```text
Score < 5  → Easy
5–7.9      → Medium
≥ 8        → Hard
```

The next question can also target concepts identified as weak in the previous response.

### 📊 LLM-as-a-Judge Evaluation
Each answer is evaluated using Gemini across:
- Correctness
- Technical Depth
- Clarity
- Overall Score

The evaluator also provides:
- Strengths
- Areas for improvement
- Missing concepts
- Detailed feedback

### 📈 Readiness Dashboard
After the interview, PrepAI calculates:
- Overall readiness score
- Correctness score
- Technical depth
- Clarity
- Performance by category
- Identified areas for improvement
- Strengths

### 📥 Downloadable Interview Report
Users can download a PDF report containing:
- Candidate information
- Target role
- Overall interview performance
- Category-wise scores
- Strengths
- Areas to improve
- Every interview question
- Candidate answers
- Question-level scores
- Detailed feedback
- Missing concepts

This allows candidates to revisit previous interviews and use the report as a study resource.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │   Resume PDF     │
                    └────────┬─────────┘
                             │
                             ▼
                     PDF Text Extraction
                             │
                             ▼
                    ┌──────────────────┐
                    │   Gemini LLM     │
                    │ Resume Extraction│
                    └────────┬─────────┘
                             │
                             ▼
                    Candidate Profile
                             │
                             ▼
                    ┌──────────────────┐
                    │   Skill Matcher  │
                    └────────┬─────────┘
                             ▲
                             │
                    ┌────────┴─────────┐
                    │   Job Profile    │
                    └────────▲─────────┘
                             │
                    Job Description
                             │
                             ▼
                    Gemini JD Extraction
                             │
                             ▼
                    Match Analysis
                             │
                             ▼
                 Personalized Questions
                             │
                             ▼
                    Interview Session
                             │
                             ▼
                       User Answer
                             │
                             ▼
                    ┌──────────────────┐
                    │   Gemini LLM     │
                    │   LLM-as-a-Judge │
                    └────────┬─────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
              Score      Feedback   Missing Concepts
                  │
                  ▼
              Adaptive Engine
                  │
                  ▼
             Next Question
                  │
                  ▼
                  ...
                  │
                  ▼
             Readiness Report
                  │
                  ▼
              PDF Download
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application logic |
| **Streamlit** | Interactive web interface |
| **Google Gemini API** | LLM-based extraction, generation and evaluation |
| **PyMuPDF** | PDF text extraction |
| **Pydantic** | Structured LLM outputs and data validation |
| **Pandas / Python** | Data processing and analysis |
| **ReportLab** | PDF report generation |
| **python-dotenv** | Environment variable management |

---

# 📂 Project Structure

```text
PrepAI/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── llm.py
│   ├── models.py
│   ├── matcher.py
│   ├── analytics.py
│   ├── pdf_report.py
│   └── vector_store.py
│
└── README.md
```

> `vector_store.py` is part of the planned RAG/embedding extension.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PrepAI.git
cd PrepAI
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit the `.env` file to GitHub.

---

# ▶️ Running the Application

Start Streamlit from the project root:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🧪 Example Workflow

### Step 1 — Upload Resume

Upload a PDF resume.

PrepAI extracts the text and creates a structured candidate profile.

```text
Candidate Profile

Skills:
Python
SQL
Machine Learning
RAG
...

Projects:
Project A
Project B
...
```

### Step 2 — Provide Job Description

Paste the target job description.

PrepAI extracts the role requirements.

```text
Required Skills:
Python
SQL
Machine Learning
Docker

Preferred Skills:
AWS
LLMs
```

### Step 3 — Job Match

The system identifies matched and missing skills.

```text
Required Skill Coverage: 75%

Matched:
✓ Python
✓ SQL
✓ Machine Learning

Missing:
✗ Docker
```

### Step 4 — Select Interview Mode

Choose:

```text
Easy → Medium
Medium → Hard
Adaptive
```

### Step 5 — Take the Interview

Answer personalized questions generated from the resume, JD and match analysis.

### Step 6 — Receive Feedback

Each response receives:

```text
Overall Score
Correctness
Technical Depth
Clarity
Strengths
Improvements
Missing Concepts
```

### Step 7 — Review Readiness

The final dashboard summarizes the candidate's performance across different categories.

### Step 8 — Download Report

Download a PDF containing the complete interview history and feedback.

---

# 🧠 Adaptive Interview Logic

PrepAI uses a simple performance-based policy for adaptive interviews:

```text
                 Previous Answer
                       │
                       ▼
                LLM Evaluation
                       │
                       ▼
                    Score
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       < 5          5 – 7.9        ≥ 8
          │            │            │
          ▼            ▼            ▼
        Easy        Medium         Hard
```

In addition to score-based difficulty adjustment, the evaluator's:
- missing concepts
- improvement areas
- previous answer

are passed to the follow-up question generator.

This allows the system to probe weaknesses or increase depth when the candidate performs well.

---

# 🔍 Why a Hybrid Matching Approach?

Simple string matching can fail in cases such as:

```text
Resume: MERN Stack
JD: React.js
```

A direct comparison would incorrectly classify React.js as missing.

PrepAI therefore uses:

```text
Exact Matching
      +
Semantic Matching
```

The deterministic matching layer handles obvious matches, while Gemini is used for ambiguous skill relationships.

---

# 📊 LLM-as-a-Judge

The answer evaluation component follows an LLM-as-a-Judge pattern.

The model receives:

```text
Interview Question
+
Candidate Answer
```

and returns structured evaluation data:

```json
{
  "overall_score": 8,
  "correctness": 9,
  "technical_depth": 7,
  "clarity": 9,
  "strengths": [],
  "improvements": [],
  "missing_concepts": [],
  "feedback": "..."
}
```

The structured output is then used by Python to calculate aggregate interview metrics.

> **Note:** LLM-based evaluation is an approximation and should not be treated as an objective or definitive measure of interview performance.

---

# 🔮 Planned RAG / Embedding Extension

A planned extension is to introduce **embedding-based retrieval and RAG** for more targeted grounding of question generation.

The intended pipeline is:

```text
Resume / JD
     ↓
Chunking
     ↓
Embeddings
     ↓
FAISS Vector Index
     ↓
Semantic Retrieval
     ↓
Relevant Context
     ↓
Gemini
     ↓
Grounded Question
```

This would allow PrepAI to retrieve the most relevant resume/project sections instead of relying only on the complete structured profile.

Potential future improvements include:
- Embedding-based skill matching
- Resume/project semantic retrieval
- RAG-grounded question generation
- Larger candidate knowledge bases
- Progress tracking across multiple interviews
- Interview history persistence
- Cloud deployment

---

# ⚠️ Limitations

- Resume parsing accuracy depends on document structure and text extraction quality.
- LLM-generated questions may occasionally be imperfect or overly difficult.
- Semantic skill matching can produce incorrect relationships in ambiguous cases.
- LLM-as-a-Judge can be subjective and may not always evaluate answers consistently.
- The current application is intended as an interview preparation tool rather than a real recruitment decision system.

---

# 🎯 Project Goals

PrepAI aims to combine:

```text
NLP
+
LLMs
+
Structured Information Extraction
+
Semantic Matching
+
Adaptive Question Generation
+
LLM Evaluation
+
Data Analytics
```

to create a practical AI-powered interview preparation workflow.

---

# 👨‍💻 Author

**Your Name**


# 📜 License

This project is intended for educational and research purposes.
