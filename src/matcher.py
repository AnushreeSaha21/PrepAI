from src.models import CandidateProfile, JobProfile
from src.llm import evaluate_skill_relationships


def normalize_skill(skill: str) -> str:
    return skill.lower().strip()


def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobProfile
):

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate.skills
    }

    required_skills = {
        normalize_skill(skill)
        for skill in job.required_skills
    }

    preferred_skills = {
        normalize_skill(skill)
        for skill in job.preferred_skills
    }

    # -----------------------------------------------
    # Exact matches
    # -----------------------------------------------

    exact_required = (
        candidate_skills & required_skills
    )

    exact_preferred = (
        candidate_skills & preferred_skills
    )

    unmatched_required = (
        required_skills - exact_required
    )

    unmatched_preferred = (
        preferred_skills - exact_preferred
    )

    # -----------------------------------------------
    # Semantic matching
    # -----------------------------------------------

    semantic_matches = []

    if unmatched_required:

        result = evaluate_skill_relationships(
            candidate.skills,
            list(unmatched_required)
        )

        semantic_matches.extend(
            result.relationships
        )

    if unmatched_preferred:

        result = evaluate_skill_relationships(
            candidate.skills,
            list(unmatched_preferred)
        )

        semantic_matches.extend(
            result.relationships
        )

    # -----------------------------------------------
    # Build final classification
    # -----------------------------------------------

    matched_required = set(exact_required)
    missing_required = set()

    matched_preferred = set(exact_preferred)
    missing_preferred = set()

    for relationship in semantic_matches:

        job_skill = normalize_skill(
            relationship.job_skill
        )

        if relationship.relationship in [
            "direct",
            "covered"
        ]:

            if job_skill in required_skills:
                matched_required.add(job_skill)

            if job_skill in preferred_skills:
                matched_preferred.add(job_skill)

        else:

            if job_skill in required_skills:
                missing_required.add(job_skill)

            if job_skill in preferred_skills:
                missing_preferred.add(job_skill)

    # -----------------------------------------------
    # Calculate score
    # -----------------------------------------------

    if required_skills:

        required_match_score = (
            len(matched_required)
            / len(required_skills)
        ) * 100

    else:

        required_match_score = 100.0

    return {
        "matched_required": sorted(
            matched_required
        ),

        "missing_required": sorted(
            missing_required
        ),

        "matched_preferred": sorted(
            matched_preferred
        ),

        "missing_preferred": sorted(
            missing_preferred
        ),

        "required_match_score": round(
            required_match_score,
            1
        ),

        "semantic_matches": semantic_matches
    }

if __name__ == "__main__":

    candidate = CandidateProfile(
        name="Test Candidate",
        skills=[
            "MERN Stack",
            "Python",
            "SQL"
        ]
    )

    job = JobProfile(
        role="Full Stack Developer",
        required_skills=[
            "React.js",
            "Node.js",
            "Python",
            "Docker"
        ],
        preferred_skills=[
            "AWS"
        ]
    )

    result = match_candidate_to_job(
        candidate,
        job
    )

    print("\n=== MATCHING RESULT ===\n")

    print("Matched Required:")
    print(result["matched_required"])

    print("\nMissing Required:")
    print(result["missing_required"])

    print("\nMatched Preferred:")
    print(result["matched_preferred"])

    print("\nMissing Preferred:")
    print(result["missing_preferred"])

    print("\nSemantic Matches:")

    for match in result["semantic_matches"]:
        print(
            f"\n{match.candidate_skill} → "
            f"{match.job_skill}"
        )
        print(f"Relationship: {match.relationship}")
        print(f"Confidence: {match.confidence}")
        print(f"Reason: {match.reason}")