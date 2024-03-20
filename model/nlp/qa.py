class QAPair:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"QAPair(question='{self.question}', answer='{self.answer}')"
