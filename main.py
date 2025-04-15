import argparse
import csv
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from scraper import get_urls_for_book, get_md_for_book
from shared import BookQandA, MDs
from ai import get_questions_for_book
from anki import create_deck

def get_filtered_mds_for_book(book_name: str, author: str) -> MDs:
    urls = get_urls_for_book(book_name)
    if urls:
        mds = []
        selected = inquirer.checkbox(
            message="Choose breakdowns to exclude",
            choices=list(urls.keys())
        ).execute()
        for to_remove in selected:
            del urls[to_remove]
        print("Fetching Breakdowns")
        for breakdown_name, url in urls.items():
            md = get_md_for_book(url)
            mds.append(md)
        return MDs(book_name, author, mds)
    else:
        print(f"No URLs found for book: {book_name}")
        raise ValueError(f"No URLs found for book: {book_name}")

        

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
    book_mds: list[MDs] = []
    for book, author in books:
        mds = get_filtered_mds_for_book(book, author)
        book_mds.append(mds)
    q_and_ass: list[BookQandA] = []
    for mds in book_mds:
        print(f"Getting questions for {mds.book_title}")
        q_and_as = get_questions_for_book(mds.mds, mds.book_title, mds.author, args.story)
        q_and_ass.append(q_and_as)
        print(f"Got {len(q_and_as.q_and_as)} for {q_and_as.book_title}")
    if args.split:
        for q_and_as in q_and_ass:
            print(f"creating deck for {q_and_as.book_title}")
            create_deck([q_and_as], q_and_as.book_title, q_and_as.book_title.lower().replace(" ", "_")+".apkg")
    else:
        print("Creating deck")
        create_deck(q_and_ass, "Maturita Grind", "maturita_grind.apkg")



if __name__ == "__main__":
    main()


