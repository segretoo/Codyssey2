import json
import os
import shutil
from quiz import Quiz

DATA_PATH = "state.json"
BACKUP_PATH = "state.json.bak"

# 파일이 없거나 손상됐을 때 사용할 기본 퀴즈 데이터
DEFAULT_QUIZZES = [
    Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1,
         hint="네덜란드 출신 프로그래머입니다."),
    Quiz("HTML에서 하이퍼링크를 만드는 태그는?", ["<link>", "<href>", "<a>", "<url>"], 3,
         hint="영어로 anchor(닻)의 줄임말입니다."),
    Quiz("Git에서 변경 이력을 저장하는 명령어는?", ["git save", "git commit", "git record", "git log"], 2),
    Quiz("웹사이트의 디자인(스타일)을 담당하는 언어는?", ["HTML", "JSON", "CSS", "SQL"], 3),
    Quiz("다음 중 파이썬의 기본 자료형이 아닌 것은?", ["int", "list", "dict", "array"], 4),
]


def load_state():
    """state.json을 불러와서 (quiz 리스트, best_score, history)를 반환.
    - 파일이 없으면: 기본 퀴즈 데이터 사용
    - 파일이 손상됐으면: 백업 파일로 복구를 먼저 시도
    - 백업도 없거나 손상됐으면: 기본 퀴즈 데이터로 최종 복구"""
    if not os.path.exists(DATA_PATH):
        return list(DEFAULT_QUIZZES), None, []

    try:
        return _load_from_path(DATA_PATH)

    except (json.JSONDecodeError, KeyError, TypeError):
        print("⚠ 저장된 데이터 파일이 손상되었습니다. 백업 파일로 복구를 시도합니다.")

        if os.path.exists(BACKUP_PATH):
            try:
                quizzes, best_score, history = _load_from_path(BACKUP_PATH)
                print("✅ 백업 파일에서 정상적으로 복구했습니다.")
                return quizzes, best_score, history
            except (json.JSONDecodeError, KeyError, TypeError):
                print("⚠ 백업 파일도 손상되어 기본 퀴즈 데이터로 복구합니다.")
        else:
            print("⚠ 백업 파일이 없어 기본 퀴즈 데이터로 복구합니다.")

        return list(DEFAULT_QUIZZES), None, []


def _load_from_path(path):
    """지정한 경로의 JSON 파일을 읽어 (quiz 리스트, best_score, history)로 변환.
    실패하면 예외를 그대로 호출한 쪽으로 전달한다."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
    best_score = data.get("best_score")
    history = data.get("history", [])

    if not quizzes:
        quizzes = list(DEFAULT_QUIZZES)

    return quizzes, best_score, history


def save_state(quizzes, best_score, history):
    """현재 퀴즈 목록, 최고점수, 게임 기록을 state.json에 저장.
    저장 직전에는 기존 파일을 백업(state.json.bak)으로 먼저 남긴다.
    쓰기 중 오류가 발생해도 프로그램이 죽지 않도록 처리."""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score,
        "history": history
    }

    try:
        if os.path.exists(DATA_PATH):
            shutil.copyfile(DATA_PATH, BACKUP_PATH)

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        print("⚠ 데이터를 저장하는 중 오류가 발생했습니다.")