import json
import os
from quiz import Quiz

DATA_PATH = "state.json"


def load_state():
    """state.json을 불러와서 (quiz 리스트, best_score)를 반환.
    파일이 없으면 기본값(빈 퀴즈 목록, 0점)을 반환."""
    if not os.path.exists(DATA_PATH):
        return [], 0

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
    best_score = data.get("best_score", 0)
    return quizzes, best_score


def save_state(quizzes, best_score):
    """현재 퀴즈 목록과 최고점수를 state.json에 저장."""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score
    }

    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)