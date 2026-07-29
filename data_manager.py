import json
import os
from quiz import Quiz

DATA_PATH = "state.json"

# 파일이 없거나 손상됐을 때 사용할 기본 퀴즈 데이터
DEFAULT_QUIZZES = [
    Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
    Quiz("HTML에서 하이퍼링크를 만드는 태그는?", ["<link>", "<href>", "<a>", "<url>"], 3),
    Quiz("Git에서 변경 이력을 저장하는 명령어는?", ["git save", "git commit", "git record", "git log"], 2),
    Quiz("웹사이트의 디자인(스타일)을 담당하는 언어는?", ["HTML", "JSON", "CSS", "SQL"], 3),
    Quiz("다음 중 파이썬의 기본 자료형이 아닌 것은?", ["int", "list", "dict", "array"], 4),
]


def load_state():
    """state.json을 불러와서 (quiz 리스트, best_score)를 반환.
    - 파일이 없으면: 기본 퀴즈 데이터 사용
    - 파일이 손상됐으면: 안내 메시지 출력 후 기본 퀴즈 데이터로 복구"""
    if not os.path.exists(DATA_PATH):
        return list(DEFAULT_QUIZZES), None

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
        best_score = data.get("best_score")

        if not quizzes:
            quizzes = list(DEFAULT_QUIZZES)

        return quizzes, best_score

    except (json.JSONDecodeError, KeyError, TypeError):
        print("⚠ 저장된 데이터 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
        return list(DEFAULT_QUIZZES), None


def save_state(quizzes, best_score):
    """현재 퀴즈 목록과 최고점수를 state.json에 저장.
    쓰기 중 오류가 발생해도 프로그램이 죽지 않도록 처리."""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score
    }

    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        print("⚠ 데이터를 저장하는 중 오류가 발생했습니다.")