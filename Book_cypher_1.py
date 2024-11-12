
import json
import os.path
import random
import re

HOW_MANY_BOOK = 3
LINE = 128
#LINE = 12
PAGE = 64
#PAGE = 2
pages = {}
page_number = 0
line_window = {}
line_number = 0
char_window = []

def clean_line(line):
    return line.strip().replace('-', '') + ' ' # adding a space instead of a new line

def add_page():
    global line_number, line_window, pages, page_number
    page_number += 1
    pages[page_number] = dict(line_window)
    line_window.clear()
    line_number = 0


def process_page(line, line_num):
     global line_window, pages, page_number
     line_window[line_num] = line
     if len(line_window) == PAGE:
         add_page()


def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def add_line():
    global char_window, line_number
    #print(char_window)
    line_number += 1
    process_page(''.join(char_window),line_number)
    char_window.clear()
    #print(char_window)

def read_book(file_path):
    global char_window
    with open(file_path, 'r', encoding='utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)
    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()

def generate_code_book():
    global pages
    code_book = {}
    for page,  lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char,[]).append(f'{page}-{num}-{pos}')
    return code_book

def save(file_path, book):
    with open(file_path,'w') as fp:
        #json.dump(book,fp, indent = 4)
        json.dump(book,fp)

def process_books(*paths):
    for path in paths:
        read_book(path)


def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path,'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save(file_path, pages)
            return pages
        else:
            code_book = generate_code_book()
            save(file_path,code_book)
            return code_book

def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0,len(code_book[char])-1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_code_book, ciphertext):
    # 840-61-122-547-23-68-501-63-69-505-39-94-931-64-27-527-15-72-164-34-74-43-2-63-853-45-28-612-9-108-883-42-50-424-1-121-597-23-42-698-6-97-303-3-37-645-30-22-204-12-88-796-18-99-173-50-3-572-12-116-496-11-23-699-3-104-597-10-108
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+',ciphertext):
        page, line, pos = cc.split('-')
        plaintext.append(
        rev_code_book[page][line][int(pos)]
        )
    return ''.join(plaintext)
def main_menu():
    print("""1). Encrypt
    2). Decrypt
    3). Quit""")
    return int(input("make a selection[1,2,3]: "))


def main():
    #code_book = load('code_books/poem.json')
    key_books = ('Books/Dr._jekyl_and_Mr._Hyde.txt','Books/All_of_Shakespeare.txt','Books/War_and_Peace.txt')
    code_book_path = 'code_books/real_deal.json'
    rev_code_book_path = 'code_books/real_deal_r.json'

    code_book = load(code_book_path,*key_books)
    rev_code_book = load(rev_code_book_path, *key_books, reverse = True)

    #ciphertext = "840-61-122-547-23-68-501-63-69-505-39-94-931-64-27-527-15-72-164-34-74-43-2-63-853-45-28-612-9-108-883-42-50-424-1-121-597-23-42-698-6-97-303-3-37-645-30-22-204-12-88-796-18-99-173-50-3-572-12-116-496-11-23-699-3-104-597-10-108"
        #input("give me your cipher text:")
    #print(encrypt(code_book, 'get rich or die trying.'))
    #print(decrypt(rev_code_book,ciphertext))
    while True:
        try:
            choice = main_menu()
            match choice:
                case 1:
                    message = input("Please enter your message here: ")
                    print(encrypt(code_book,message))
                    continue
                case 2:
                    message = input("Please enter your ciphertext here: ")
                    print(decrypt(rev_code_book,message))
                    continue
                case 3:
                    break
        except ValueError:
            print("Improper input")

if __name__ == '__main__':
    main()
"""
                if char in code_book:
                    code_book[char].append(f'{page}-{num}-{pos}')
                else:
                    code_book[char]= [f'{page}-{num}-{pos}'}]
"""