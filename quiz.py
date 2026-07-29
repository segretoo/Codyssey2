class Quiz:
    """퀴즈 문제 1개를 표현하는 클래스"""

    def __init__(self, question, answer, choices=None, quiz_type="multiple"):
        self.question = question      # 문제 내용
        self.answer = answer          # 정답 (객관식: 번호, 주관식: 문자열)
        self.choices = choices        # 보기 리스트 (주관식이면 None)
        self.quiz_type = quiz_type    # "multiple"(객관식) 또는 "short"(주관식)

    def check_answer(self, user_input):
        """사용자가 입력한 답이 정답인지 확인"""
        if self.quiz_type == "multiple":
            return str(user_input).strip() == str(self.answer)
        else:  # 주관식은 대소문자, 공백 차이는 정답으로 인정
            return str(user_input).strip().lower() == str(self.answer).strip().lower()

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환"""
        return {
            "question": self.question,
            "answer": self.answer,
            "choices": self.choices,
            "type": self.quiz_type
        }

    @staticmethod
    def from_dict(data):
        """JSON에서 불러온 딕셔너리를 Quiz 객체로 변환"""
        return Quiz(
            question=data["question"],
            answer=data["answer"],
            choices=data.get("choices"),
            quiz_type=data.get("type", "multiple")
        )