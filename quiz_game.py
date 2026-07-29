from quiz import Quiz


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self, quizzes, best_score=0):
        self.quizzes = quizzes        # Quiz 객체 리스트
        self.best_score = best_score  # 지금까지의 최고 점수

    def play(self):
        """등록된 모든 퀴즈를 순서대로 풀고 점수를 계산해서 반환"""
        if not self.quizzes:
            print("\n⚠ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.\n")
            return

        total = len(self.quizzes)
        correct_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for idx, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {idx}]")
            print(quiz.question)
            print()

            if quiz.quiz_type == "multiple":
                for i, choice in enumerate(quiz.choices, start=1):
                    print(f"{i}. {choice}")
                print()
                user_input = input("정답 입력: ")
            else:
                user_input = input("정답 입력 (주관식): ")

            if quiz.check_answer(user_input):
                print("✅ 정답입니다!\n")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer})\n")

        score = int(correct_count / total * 100)

        print("=" * 45)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

        print("=" * 45)

    def add_quiz(self):
        """새로운 퀴즈를 입력받아 목록에 추가"""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = input("문제를 입력하세요: ")

        is_multiple = input("객관식인가요? (y/n): ").strip().lower()

        if is_multiple == "y":
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

            new_quiz = Quiz(question, answer, choices, quiz_type="multiple")
        else:
            answer = input("정답을 입력하세요: ")
            new_quiz = Quiz(question, answer, quiz_type="short")

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
        """저장된 최고 점수를 출력"""
        print(f"\n🏆 최고 점수: {self.best_score}점\n")