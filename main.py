from data_manager import load_state, save_state
from quiz_game import QuizGame, BackToMenu, QuitProgram


def print_menu():
    print("=" * 45)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 45)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 퀴즈 삭제")
    print("6. 퀴즈 수정")
    print("7. 게임 기록")
    print("8. 종료")
    print("=" * 45)


def get_menu_choice():
    """1~8 사이의 숫자만 허용. q 입력 시 바로 종료(8)로 처리."""
    while True:
        choice = input("선택: ").strip()

        if choice.lower() == "q":
            return 8

        if choice.lower() == "b":
            print("⚠ 이미 메인 메뉴입니다.\n")
            continue

        if choice == "":
            print("⚠ 입력이 비어 있습니다. 1-8 사이의 숫자를 입력하세요.\n")
            continue

        if not choice.isdigit():
            print("⚠ 잘못된 입력입니다. 1-8 사이의 숫자를 입력하세요.\n")
            continue

        num = int(choice)
        if not (1 <= num <= 8):
            print("⚠ 잘못된 입력입니다. 1-8 사이의 숫자를 입력하세요.\n")
            continue

        return num


def main():
    quizzes, best_score, history = load_state()
    game = QuizGame(quizzes, best_score, history)

    print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)")
    print("ℹ 입력 중 언제든 b=이전으로, q=종료 가 가능합니다.")

    try:
        while True:
            print_menu()
            choice = get_menu_choice()

            try:
                if choice == 1:
                    game.play()
                elif choice == 2:
                    game.add_quiz()
                elif choice == 3:
                    game.list_quizzes()
                elif choice == 4:
                    game.show_best_score()
                elif choice == 5:
                    game.delete_quiz()
                elif choice == 6:
                    game.edit_quiz()
                elif choice == 7:
                    game.show_history()
                elif choice == 8:
                    save_state(game.quizzes, game.best_score, game.history)
                    print("\n💾 저장 완료! 게임을 종료합니다. 안녕히 가세요 👋\n")
                    break
            except BackToMenu:
                print("\n↩ 메뉴로 돌아갑니다.\n")
            except QuitProgram:
                save_state(game.quizzes, game.best_score, game.history)
                print("\n💾 저장 완료! 게임을 종료합니다. 안녕히 가세요 👋\n")
                break

            if choice != 8:
                save_state(game.quizzes, game.best_score, game.history)

    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠ 강제 종료가 감지되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        save_state(game.quizzes, game.best_score, game.history)
        print("💾 저장 완료. 안녕히 가세요 👋\n")


if __name__ == "__main__":
    main()