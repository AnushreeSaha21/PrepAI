from collections import defaultdict


def calculate_readiness(evaluations, questions):

    if not evaluations:
        return None

    overall_scores = [
        evaluation.overall_score
        for evaluation in evaluations
    ]

    correctness_scores = [
        evaluation.correctness
        for evaluation in evaluations
    ]

    depth_scores = [
        evaluation.technical_depth
        for evaluation in evaluations
    ]

    clarity_scores = [
        evaluation.clarity
        for evaluation in evaluations
    ]

    result = {
        "overall": sum(overall_scores) / len(overall_scores),
        "correctness": (
            sum(correctness_scores)
            / len(correctness_scores)
        ),
        "technical_depth": (
            sum(depth_scores)
            / len(depth_scores)
        ),
        "clarity": (
            sum(clarity_scores)
            / len(clarity_scores)
        )
    }

    # ----------------------------------------------
    # Category-level scores
    # ----------------------------------------------

    category_scores = defaultdict(list)

    for question, evaluation in zip(
        questions,
        evaluations
    ):
        category_scores[
            question.category
        ].append(
            evaluation.overall_score
        )

    result["categories"] = {
        category: sum(scores) / len(scores)
        for category, scores
        in category_scores.items()
    }

    # ----------------------------------------------
    # Missing concepts
    # ----------------------------------------------

    missing_concepts = []

    for evaluation in evaluations:
        missing_concepts.extend(
            evaluation.missing_concepts
        )

    result["missing_concepts"] = missing_concepts

    return result



def identify_strengths(readiness):

    strengths = []

    if readiness["correctness"] >= 8:
        strengths.append(
            "Strong technical correctness"
        )

    if readiness["technical_depth"] >= 8:
        strengths.append(
            "Strong technical depth"
        )

    if readiness["clarity"] >= 8:
        strengths.append(
            "Clear and well-structured answers"
        )

    return strengths