class BookQandA:
    def __init__(self, book_title: str, author: str, q_and_as: list[tuple[str, str]]):
        self.book_title = book_title
        self.author = author
        self.q_and_as = q_and_as
