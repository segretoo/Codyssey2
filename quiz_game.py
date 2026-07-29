from quiz import Quiz
import random


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self, quizzes, best_score=None):
        self.quizzes = quizzes        # Quiz 객체 리스트
        self.best_score = best_score  # 아직 안 풀었으면 None

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

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for idx, quiz in enumerate(selected_quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {idx}]")
            quiz.display()
            print()

            hint_used = False
            if quiz.has_hint():
                see_hint = input("힌트를 보시겠습니까? (y/n): ").strip().lower()
                if see_hint == "y":
                    print(f"💡 힌트: {quiz.hint}")
                    hint_used = True

            user_answer = self._get_answer_input()

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

    def _get_question_count(self, max_count):
        """풀고 싶은 문제 수를 입력받는다. (1 ~ 전체 개수 범위, 예외처리 포함)"""
        while True:
            raw = input(f"몇 문제를 푸시겠습니까? (1-{max_count}): ").strip()

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

    def _get_answer_input(self):
        """정답 번호(1~4) 입력을 검증하며 받는다.
        공백 제거, 숫자 변환 실패, 범위 밖, 빈 입력을 모두 처리."""
        while True:
            raw = input("정답 입력: ").strip()

            if raw == "":
                print("⚠ 입력이 비어 있습니다. 정답 번호를 입력하세요.")
                continue

            if not raw.isdigit():
                print("⚠ 숫자를 입력해야 합니다. 다시 입력하세요.")
                continue

            num = int(raw)
            if not (1 <= num <= 4):
                print("⚠ 1부터 4 사이의 번호를 입력하세요.")
                continue

            return num

    def add_quiz(self):
        """새로운 퀴즈를 입력받아 목록에 추가"""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ")
            choices.append(choice)

        while True:
            answer_input = input("정답 번호 (1-4): ").strip()
            if answer_input.isdigit() and 1 <= int(answer_input) <= 4:
                answer = int(answer_input)
                break
            print("⚠ 1부터 4 사이의 숫자를 입력하세요.")

        hint_input = input("힌트를 입력하세요 (없으면 Enter): ").strip()
        hint = hint_input if hint_input != "" else None

        new_quiz = Quiz(question, choices, answer, hint=hint)
        self.quizzes.append(new_quiz)
        print("\n✅ 퀴즈가 추가되었습니다!\n")

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
            print(f"\n🏆 최고 점수: {self.best_score}점\n")