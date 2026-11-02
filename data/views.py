
import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render


JSON_FILE = settings.BASE_DIR / "JSON" / "data.json"


def load_quiz_data():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def categories(request):
    data = load_quiz_data()

    return render(
        request,
        "categories.html",
        {
            "quiz_title": data["quiz_title"],
            "categories": data["categories"],
        },
    )


from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

# Existing load_quiz_data() function ko use karna.

@require_http_methods(["GET", "POST"])
def start_quiz(request, category_id):
    data = load_quiz_data()

    category = next(
        (item for item in data["categories"]
         if item["id"] == category_id),
        None
    )

    if category is None:
        from django.http import Http404
        raise Http404("Quiz category not found")

    questions = category["questions"]
    score = None

    if request.method == "POST":
        score = 0
        answers = []

        for question in questions:
            selected = request.POST.get(
                f"question_{question['id']}"
            )

            is_correct = selected == question["correct_answer"]

            if is_correct:
                score += question.get("points", 10)

            answers.append({
                "question": question["question"],
                "selected": selected,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
            })

        return render(request, "quiz_result.html", {
            "category": category,
            "score": score,
            "answers": answers,
        })

    return render(request, "quiz.html", {
        "category": category,
        "questions": questions,
    })
