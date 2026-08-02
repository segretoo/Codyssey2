from quiz import Quiz
import random
from datetime import datetime


class BackToMenu(Exception):
    """사용자가 'b'를 입력해 현재 작업을 취소하고 메뉴로 돌아갈 때 발생"""
    pass


class QuitProgram(Exception):
    """사용자가 'q'를 입력해 프로그램 종료를 요청할 때 발생"""
    pass


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self, quizzes, best_score=None, history=None):
        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history if history is not None else []

    def _read_line(self, prompt):
        """입력을 받되, b/q/? 를 공통으로 처리한다.
        - b: 이전(메뉴)으로 돌아가기
        - q: 프로그램 종료
        - ?: 도움말 표시 후 같은 질문 다시 하기"""
        while True:
            raw = input(prompt)
            lowered = raw.strip().lower()

            if lowered == "?":
                print("\nℹ 도움말: 입력창에서 b=이전 메뉴로 돌아가기, "
                      "q=프로그램 저장 후 종료 가 가능합니다.\n")
                continue

            if lowered == "b":
                raise BackToMenu()
            if lowered == "q":
                raise QuitProgram()

            return raw

    def _get_nonempty_text(self, prompt):
        """빈 문자열이 아닌 텍스트를 입력받는다."""
        while True:
            text = self._read_line(prompt).strip()
            if text == "":
                print("⚠ 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    def play(self):
        """등록된 퀴즈 중 사용자가 선택한 문제 수만큼 풀고 점수를 계산"""
        if not self.quizzes:
            print("\n⚠ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.\n")
            return

        total_available = len(self.quizzes)
        num_to_play = self._get_question_count(total_available)

        shuffled_quizzes = random.sample(self.quizzes, total_available)
        selected_quizzes = shuffled_quizzes[:num_to_play]

        total = len(selected_quizzes)
        correct_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제, b=중단 q=종료)\n")

        for idx, quiz in enumerate(selected_quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {idx}]")
            quiz.display()
            print()

            user_answer, hint_used = self._get_answer_input(quiz)

            if quiz.check_answer(user_answer):
                if hint_used:
                    print("✅ 정답입니다! (힌트 사용으로 0.5문제 처리)\n")
                    correct_count += 0.5
                else:
                    print("✅ 정답입니다!\n")
                    correct_count += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)\n")

        score = int(correct_count / total * 100)

        print("=" * 45)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

        print("=" * 45)

        record = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": total,
            "correct_count": correct_count,
            "score": score
        }
        self.history.append(record)

    def _get_question_count(self, max_count):
        """풀고 싶은 문제 수를 입력받는다."""
        while True:
            raw = self._read_line(
                f"몇 문제를 푸시겠습니까? (1-{max_count}) [b=뒤로 q=종료]: "
            ).strip()

            if raw == "":
                print("⚠ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue
            if not raw.isdigit():
                print("⚠ 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue
            num = int(raw)
            if not (1 <= num <= max_count):
                print(f"⚠ 1부터 {max_count} 사이의 숫자를 입력하세요.")
                continue
            return num

    def _get_answer_input(self, quiz):
        """정답 번호를 입력받는다. 힌트가 있으면 h로 확인 가능."""
        hint_used = False
        hint_note = " (h=힌트)" if quiz.has_hint() else ""

        while True:
            raw = self._read_line(f"정답 입력{hint_note}: ").strip()

            if raw == "":
                print("⚠ 입력이 비어 있습니다. 정답 번호를 입력하세요.")
                continue

            if quiz.has_hint() and raw.lower() == "h":
                if hint_used:
                    print("ℹ 이미 힌트를 확인하셨습니다. (0.5문제 처리 유지)")
                else:
                    print(f"💡 힌트: {quiz.hint}")
                    print("⚠ 힌트를 사용하면 이 문제는 0.5문제로 처리되어 점수가 줄어듭니다.")
                    hint_used = True
                continue

            if not raw.isdigit():
                print("⚠ 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue

            num = int(raw)
            if not (1 <= num <= 4):
                print("⚠ 1부터 4 사이의 번호를 입력하세요.")
                continue

            return num, hint_used

    def add_quiz(self):
        """새로운 퀴즈를 입력받아 목록에 추가"""
        print("\n📌 새로운 퀴즈를 추가합니다. (b=뒤로 q=종료 ?=도움말)\n")

        question = self._get_nonempty_text("문제를 입력하세요 [b=뒤로 q=종료 ?=도움말]: ")

        choices = []
        for i in range(1, 5):
            choice = self._get_nonempty_text(f"선택지 {i} [b=뒤로 q=종료 ?=도움말]: ")
            choices.append(choice)

        answer = self._get_choice_answer()

        hint_input = self._read_line("힌트를 입력하세요 (없으면 Enter) [b=뒤로 q=종료]: ").strip()
        hint = hint_input if hint_input != "" else None

        new_quiz = Quiz(question, choices, answer, hint=hint)
        self.quizzes.append(new_quiz)
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def _get_choice_answer(self, max_count=4):
        """정답 번호(1~4) 입력을 검증하며 받는다."""
        while True:
            raw = self._read_line(f"정답 번호 (1-{max_count}) [b=뒤로 q=종료]: ").strip()

            if raw == "":
                print("⚠ 입력이 비어 있습니다. 정답 번호를 입력하세요.")
                continue
            if not raw.isdigit():
                print("⚠ 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue
            num = int(raw)
            if not (1 <= num <= max_count):
                print(f"⚠ 1부터 {max_count} 사이의 번호를 입력하세요.")
                continue
            return num

    def list_quizzes(self):
        """등록된 모든 퀴즈의 문제 목록을 출력"""
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 45)

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        else:
            for idx, quiz in enumerate(self.quizzes, start=1):
                print(f"[{idx}] {quiz.question}")

        print("-" * 45)

    def show_best_score(self):
        """저장된 최고 점수를 출력. 아직 안 풀었으면 안내 메시지."""
        if self.best_score is None:
            print("\n🏆 아직 퀴즈를 푼 기록이 없습니다.\n")
        else:
            play_count = len(self.history)
            print(f"\n🏆 최고 점수: {self.best_score}점 (총 {play_count}회 플레이)\n")

    def delete_quiz(self):
        """등록된 퀴즈 중 하나를 선택해서 삭제 (재확인 포함)"""
        if not self.quizzes:
            print("\n⚠ 삭제할 퀴즈가 없습니다.\n")
            return

        self.list_quizzes()

        index = self._get_delete_index(len(self.quizzes))
        target = self.quizzes[index - 1]

        confirm = self._read_line(
            f"정말 삭제하시겠습니까? '{target.question}' (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("\n삭제가 취소되었습니다.\n")
            return

        removed = self.quizzes.pop(index - 1)
        print(f"\n🗑 삭제되었습니다: {removed.question}\n")

    def edit_quiz(self):
        """등록된 퀴즈 중 하나를 선택해서 전체 내용을 다시 입력받아 교체"""
        if not self.quizzes:
            print("\n⚠ 수정할 퀴즈가 없습니다.\n")
            return

        self.list_quizzes()

        index = self._get_delete_index(len(self.quizzes))
        target = self.quizzes[index - 1]

        print(f"\n✏ '{target.question}' 문제를 수정합니다. "
              f"(현재 값은 [ ] 안에 표시, 그대로 두려면 Enter)\n")

        question = self._read_line(
            f"문제 [{target.question}]: "
        ).strip()
        if question == "":
            question = target.question

        choices = []
        for i in range(1, 5):
            current = target.choices[i - 1]
            new_choice = self._read_line(f"선택지 {i} [{current}]: ").strip()
            choices.append(new_choice if new_choice != "" else current)

        answer_raw = self._read_line(
            f"정답 번호 (1-4) [{target.answer}]: "
        ).strip()
        answer = int(answer_raw) if answer_raw.isdigit() and 1 <= int(answer_raw) <= 4 else target.answer

        hint_prompt = f"힌트 [{target.hint if target.hint else '없음'}]: "
        hint_raw = self._read_line(hint_prompt).strip()
        hint = hint_raw if hint_raw != "" else target.hint

        self.quizzes[index - 1] = Quiz(question, choices, answer, hint=hint)
        print("\n✅ 퀴즈가 수정되었습니다!\n")

    def _get_delete_index(self, max_count):
        """삭제할 퀴즈 번호를 입력받는다."""
        while True:
            raw = self._read_line(
                f"삭제할 퀴즈 번호를 입력하세요 (1-{max_count}) [b=뒤로 q=종료]: "
            ).strip()

            if raw == "":
                print("⚠ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue
            if not raw.isdigit():
                print("⚠ 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue
            num = int(raw)
            if not (1 <= num <= max_count):
                print(f"⚠ 1부터 {max_count} 사이의 숫자를 입력하세요.")
                continue
            return num

    def show_history(self):
        """지금까지의 모든 게임 기록을 출력"""
        if not self.history:
            print("\n📜 아직 게임 기록이 없습니다.\n")
            return

        print(f"\n📜 게임 기록 (총 {len(self.history)}회)\n")
        print("-" * 45)
        for i, record in enumerate(self.history, start=1):
            print(f"[{i}] {record['datetime']} | "
                  f"{record['total_questions']}문제 중 {record['correct_count']}문제 정답 | "
                  f"{record['score']}점")
        print("-" * 45)