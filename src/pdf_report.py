from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def _safe_text(text) -> str:
    """
    Convert values to text and avoid problematic
    characters for the PDF.
    """
    if text is None:
        return ""

    return str(text).replace("→", "->").replace("•", "-")


def generate_interview_report(
    candidate,
    job,
    readiness,
    interview_history,
):
    """
    Generate a downloadable PDF containing:

    - Candidate information
    - Target role
    - Overall readiness
    - Dimension scores
    - Category scores
    - Strengths
    - Areas to improve
    - Every interview question
    - Candidate answer
    - Evaluation and feedback

    Returns:
        bytes: PDF content
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="PrepAI Interview Readiness Report",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=26,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=18,
        spaceBefore=12,
        spaceAfter=8,
    )

    question_style = ParagraphStyle(
        "Question",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        spaceAfter=4,
    )

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "PrepAI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Interview Readiness Report",
            subtitle_style,
        )
    )

    # --------------------------------------------------
    # CANDIDATE / ROLE INFORMATION
    # --------------------------------------------------

    candidate_name = _safe_text(candidate.name)
    job_role = _safe_text(job.role)

    info_data = [
        ["Candidate", candidate_name],
        ["Target Role", job_role],
        [
            "Questions Answered",
            str(len(interview_history)),
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[42 * mm, 120 * mm],
    )

    info_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(info_table)
    story.append(Spacer(1, 10))

    # --------------------------------------------------
    # OVERALL RESULTS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Overall Performance",
            heading_style,
        )
    )

    overall_data = [
        ["Metric", "Score"],
        [
            "Overall Readiness",
            f"{readiness['overall']:.1f} / 10",
        ],
        [
            "Correctness",
            f"{readiness['correctness']:.1f} / 10",
        ],
        [
            "Technical Depth",
            f"{readiness['technical_depth']:.1f} / 10",
        ],
        [
            "Clarity",
            f"{readiness['clarity']:.1f} / 10",
        ],
    ]

    overall_table = Table(
        overall_data,
        colWidths=[100 * mm, 55 * mm],
    )

    overall_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(overall_table)

    # --------------------------------------------------
    # CATEGORY PERFORMANCE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Performance by Category",
            heading_style,
        )
    )

    category_names = {
        "resume_project": "Resume / Projects",
        "jd_technical": "JD Technical",
        "jd_gap": "JD Skill Gaps",
        "fundamentals": "Fundamentals",
    }

    category_data = [
        ["Category", "Score"]
    ]

    for category, score in readiness["categories"].items():

        display_name = category_names.get(
            category,
            category.replace("_", " ").title(),
        )

        category_data.append([
            display_name,
            f"{score:.1f} / 10",
        ])

    category_table = Table(
        category_data,
        colWidths=[100 * mm, 55 * mm],
    )

    category_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(category_table)

    # --------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------

    strengths = []

    if readiness["correctness"] >= 8:
        strengths.append("Strong technical correctness")

    if readiness["technical_depth"] >= 8:
        strengths.append("Strong technical depth")

    if readiness["clarity"] >= 8:
        strengths.append("Clear and well-structured answers")

    story.append(
        Paragraph(
            "Strengths",
            heading_style,
        )
    )

    if strengths:

        for strength in strengths:
            story.append(
                Paragraph(
                    f"- {_safe_text(strength)}",
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No major strengths identified yet.",
                body_style,
            )
        )

    # --------------------------------------------------
    # AREAS TO IMPROVE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Areas to Improve",
            heading_style,
        )
    )

    unique_concepts = list(
        dict.fromkeys(
            readiness.get(
                "missing_concepts",
                [],
            )
        )
    )

    if unique_concepts:

        for concept in unique_concepts:

            story.append(
                Paragraph(
                    f"- {_safe_text(concept)}",
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No major missing concepts identified.",
                body_style,
            )
        )

    # --------------------------------------------------
    # QUESTION-BY-QUESTION RESULTS
    # --------------------------------------------------

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Interview Transcript and Feedback",
            heading_style,
        )
    )

    for index, record in enumerate(
        interview_history,
        start=1,
    ):

        question = record["question"]
        answer = record["answer"]
        evaluation = record["evaluation"]

        story.append(
            Paragraph(
                f"Question {index}",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Question:</b> "
                f"{_safe_text(question.question)}",
                question_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Category:</b> "
                f"{_safe_text(question.category)}",
                small_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Difficulty:</b> "
                f"{_safe_text(question.difficulty)}",
                small_style,
            )
        )

        story.append(Spacer(1, 4))

        story.append(
            Paragraph(
                f"<b>Your Answer:</b><br/>"
                f"{_safe_text(answer)}",
                body_style,
            )
        )

        score_data = [
            ["Evaluation", "Score"],
            [
                "Overall",
                f"{evaluation.overall_score:.1f} / 10",
            ],
            [
                "Correctness",
                f"{evaluation.correctness:.1f} / 10",
            ],
            [
                "Technical Depth",
                f"{evaluation.technical_depth:.1f} / 10",
            ],
            [
                "Clarity",
                f"{evaluation.clarity:.1f} / 10",
            ],
        ]

        score_table = Table(
            score_data,
            colWidths=[100 * mm, 55 * mm],
        )

        score_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )

        story.append(score_table)
        story.append(Spacer(1, 8))

        if evaluation.strengths:

            story.append(
                Paragraph(
                    "<b>Strengths:</b>",
                    body_style,
                )
            )

            for item in evaluation.strengths:
                story.append(
                    Paragraph(
                        f"- {_safe_text(item)}",
                        small_style,
                    )
                )

        if evaluation.improvements:

            story.append(
                Paragraph(
                    "<b>Areas to Improve:</b>",
                    body_style,
                )
            )

            for item in evaluation.improvements:
                story.append(
                    Paragraph(
                        f"- {_safe_text(item)}",
                        small_style,
                    )
                )

        if evaluation.missing_concepts:

            story.append(
                Paragraph(
                    "<b>Missing Concepts:</b>",
                    body_style,
                )
            )

            for item in evaluation.missing_concepts:
                story.append(
                    Paragraph(
                        f"- {_safe_text(item)}",
                        small_style,
                    )
                )

        story.append(
            Paragraph(
                f"<b>Feedback:</b> "
                f"{_safe_text(evaluation.feedback)}",
                body_style,
            )
        )

        story.append(Spacer(1, 12))

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()