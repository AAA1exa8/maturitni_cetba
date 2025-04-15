import genanki
from shared import BookQandA

def create_deck(q_and_as: list[BookQandA], name: str, file: str):
    my_model = genanki.Model(
        1607392319,
        'Basic model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ]
    )

    my_deck = genanki.Deck(
        2059400110,
        name
    )

    for book in q_and_as:
        for question, answer in book.q_and_as:
            formatted_question = f"""<div style="font-size: 1.5em; font-weight: bold;">{book.book_title}</div>
<div><em>{book.author}</em></div>
<br>
{question}"""

            my_note = genanki.Note(
                model=my_model,
                fields=[formatted_question, answer]
            )
            my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file(file)

