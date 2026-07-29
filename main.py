from data_manager import load_state, save_state
from quiz_game import QuizGame


def print_menu():
    print("=" * 45)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 45)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 45)


def get_menu_choice():
    """1~5 사이의 숫자만 허용하고, 아니면 재입력 받기"""
    while True:
        choice = input("선택: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 5:
            return int(choice)
        print("⚠ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")


def main():
    quizzes, best_score = load_state()
    game = QuizGame(quizzes, best_score)

    print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)")

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            game.play()
        elif choice == 2:
            game.add_quiz()
        elif choice == 3:
            game.list_quizzes()
        elif choice == 4:
            game.show_best_score()
        elif choice == 5:
            save_state(game.quizzes, game.best_score)
            print("\n💾 저장 완료! 게임을 종료합니다. 안녕히 가세요 👋\n")
            break


if __name__ == "__main__":
    main()