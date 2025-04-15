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
        ])
    my_deck = genanki.Deck(
        2059400110,
        name
    )
    qa_list = []
    for qas in q_and_as:
        for qa in qas.q_and_as:
            qa_list.append(qa)
    for question, answer in qa_list:
        my_note = genanki.Note(
            model=my_model,
            fields=[question, answer]
        )
        my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file(file)

