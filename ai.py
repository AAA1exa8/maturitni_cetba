from openai import OpenAI
import json

from shared import BookQandA

client: None | OpenAI = None

def get_questions_for_book(mds: list[str], name: str, author: str, story: bool = False) -> BookQandA:
    global client
    if client is None:
        client = OpenAI()
    schema_example = {
        "questions_and_answers": [
            {
              "question": "Question 1",
              "answer": "Answer 1"
            }
        ]
    }
    story_string = "\nVynechej otázky na děj.\n" if not story else ""
    question_singular = f"Vygeneruj z následujícího rozboru otázky které zjišťují znalosti každé části rozboru. {story_string}"
    question_multiple = f"Vygeneruj z následujících rozborů otázky které zjišťují znalosti každé části rozboru. {story_string}"
    question = """
    Otázky by měli pokrývat celý rozbor.
    Vždy vygeneruj otázku a odpověď vzatou z rozboru.
    V odpovědi budou pouze otázky a odpovědi.
    Odpovědi by kde je to možné měli dosahovat až pěti vět.
    V případě že rozbory mají stejné informace neopakuj otázky
    Mezi otázkami by měli být otázky:
    Na hlavní postavy, na autora, na literálně historický kontext, na jazyk, na hlavní myšlenky, stylistika a na další věci obsažené v rozboru.
    V případě že k nějákému rozboru není otázka, tak ji vynechej.
    Pokud je to možné vygeneruj alespoň 10 nebo více otázek."""
    if len(mds) == 1:
        question = question_singular + question
        question += mds[0]
    else:
        question = question_multiple + question
        question += "\n\n".join(mds)

    chat_completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "provide a output in valid JSON format. The data schema should look like this: " + json.dumps(schema_example) + "\n\n"
            } 
            ,
            {
                "role": "user",
                "content": question
            }
        ]
        
    )
    response = chat_completion.choices[0].message.content
    try:
        response = json.loads(response)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Response:", response)
        raise ValueError("Invalid JSON response")
    if "questions_and_answers" not in response:
        print("Invalid response format:", response)
        raise ValueError("Invalid response format")
    questions = response["questions_and_answers"]
    if not isinstance(questions, list):
        print("Invalid response format:", response)
        raise ValueError("Invalid response format")
    if len(questions) == 0:
        print("No questions found in response:", response)
        raise ValueError("No questions found in response")
    questions_and_answers = []
    for question in questions:
        if "question" not in question or "answer" not in question:
            print("Invalid question format:", question)
            raise ValueError("Invalid question format")
        questions_and_answers.append((question["question"], question["answer"]))
    return BookQandA(name, author, questions_and_answers)
    

