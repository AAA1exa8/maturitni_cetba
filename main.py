import argparse
import csv
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from scraper import get_urls_for_book, get_md_for_book
from shared import BookQandA
from ai import get_questions_for_book
from anki import create_deck

def get_q_and_as_for_book(breakdown_name: str, author: str, story: bool) -> BookQandA:
    urls = get_urls_for_book(breakdown_name)
    if urls:
        mds = []
        selected = inquirer.checkbox(
            message="Choose breakdowns to exclude",
            choices=list(urls.keys())
        ).execute()
        for to_remove in selected:
            del urls[to_remove]
        for breakdown_name, url in urls.items():
            md = get_md_for_book(url)
            mds.append(md)
        q_and_as = get_questions_for_book(mds, breakdown_name, author, story)
        return q_and_as
    else:
        print(f"No URLs found for book: {breakdown_name}")
        raise ValueError(f"No URLs found for book: {breakdown_name}")

        

def main():
    parser = argparse.ArgumentParser(
        prog="Maturita Grinder",
        description="Creates anki cards for Czech Maturita exam.")
    parser.add_argument("-s", "--story", action="store_true", help="Include story in the questions")
    parser.add_argument("-i", "--split", action="store_true", help="Create deck for each book")
    parser.add_argument("-f", "--file", type=str, help="File to save the questions to", required=True)
    load_dotenv()
    args = parser.parse_args()
    
    books = []
    with open(args.file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            books.append((row[0], row[1]))
    q_and_ass: list[BookQandA] = []
    for book, author in books:
        q_and_as = get_q_and_as_for_book(book, author, args.story)
        q_and_ass.append(q_and_as)
    if args.split:
        for q_and_as in q_and_ass:
            create_deck([q_and_as], q_and_as.book_title, q_and_as.book_title.lower().replace(" ", "_")+".apkg")
    else:
        create_deck(q_and_ass, "Maturita Grind", "maturita_grind.apkg")



if __name__ == "__main__":
    main()


