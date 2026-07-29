class Quiz:
    """퀴즈 문제 1개를 표현하는 클래스 (객관식 전용, 정답은 1~4 번호)"""

    def __init__(self, question, choices, answer):
        self.question = question   # 문제 내용
        self.choices = choices     # 보기 4개 리스트
        self.answer = answer       # 정답 번호 (1~4 중 하나)

    def display(self):
        """문제와 보기를 출력"""
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        """사용자가 입력한 정답 번호가 맞는지 확인"""
        return int(user_answer) == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        """JSON에서 불러온 딕셔너리를 Quiz 객체로 변환"""
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )