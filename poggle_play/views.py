#w7erx56f/
#hfsopm5z/
#kslcyj4g/

import requests
from django.shortcuts import render
import random
from .models import Board, Word, Word_Board
import json
from django.shortcuts import redirect

def create_random_code_for_link():
    opt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
           't', 'u', 'v', 'w', 'x','y', 'z', '1', '2','3','4','5','6','7','8','9','0']

    link = ''

    for i in range(8):
        random_integer = random.randint(0, 35)
        random_char = opt[random_integer]
        link = link + random_char

    return link

def new_board():
    dice_set = [["R", "I","F", "O", "B", "X"],
        ["I", "F", "E", "H", "E", "Y"],
        ["D", "E", "N", "O", "W", "S"],
        ["U", "T", "O", "K", "N", "D"],
        ["H", "M", "S", "R", "A", "O"],
        ["L", "U", "P", "E", "T", "S"],
        ["A", "C", "I", "T", "O", "A"],
        ["Y", "L", "G", "K", "U", "E"],
        ["Qu", "B", "M", "J", "O", "A"],
        ["E", "H", "I", "S", "P", "N"],
        ["V", "E", "T", "I", "G", "N"],
        ["B", "A", "L", "I", "Y", "T"],
        ["E", "Z", "A", "V", "N", "D"],
        ["R", "A", "L", "E", "S", "C"],
        ["U", "W", "I", "L", "R", "G"],
        ["P", "A", "C", "E", "M", "D"]]
    
    letters = []

    for die in dice_set:
        letter = random.choice(die)
        letters.append(letter)

    random.shuffle(letters)

    board = {}
    #make into dictionary
    for i in range(0,16):
        board[i] = letters[i]
    
    #make into json
    json_board = json.dumps(board)


    boardInst = Board(arrangement = json_board)

    unique = False
    while unique == False:
        link = create_random_code_for_link()
        findMultiple = Board.objects.filter(link = link)
        if len(findMultiple) == 0:
            boardInst.link = link
            unique = True
            boardInst.save()
    
    return boardInst
    #create new board object and return   

def is_scrabble_valid(word):
    print(word)
    url = "https://scrabble.merriam.com/finder/" + word
    res = requests.get(url)

    info = str(res.content)

    if "play_yes" in info:
       return True
    else:
        return False

def show_board(request, boardString=False):
    player_name = request.COOKIES.get('player_name', None)
    
    currentBoard = None

    if boardString:
        try:
            currentBoard = Board.objects.get(link=boardString)
        except:
            currentBoard = new_board()
            return redirect('show_board', boardString = currentBoard.link)
    
    else:
        currentBoard = new_board()
        return redirect('show_board', boardString = currentBoard.link)

    letters = currentBoard.arrangement
    boardDictionary = json.loads(letters)

    board_as_list = []

    #transform dictionary to list of lists
    for i in range(0,4):
        row = []
        for ii in range(0,4):
            index = i*(4) + ii
            index = str(index)
            row.append(boardDictionary[index])
        board_as_list.append(row)

    board_pk = ''
    board_pk = Board.objects.get(link = boardString)

    word_list = []
    
    try:
        word_list = Word_Board.objects.filter(board = board_pk)
    except:
        word_list = []
    
    final_word_list_valid = []
    final_word_list_invalid = []

    for w in word_list:
        if w.word.valid is None:
            word_valid = is_scrabble_valid(w.word.word_string)
            w.word.valid = word_valid
            w.word.save()
        
        if w.word.valid:
            final_word_list_valid.append(w.word.word_string)
        else:
            final_word_list_invalid.append(w.word.word_string)
    
    final_word_list_valid.sort()
    final_word_list_invalid.sort()

    return render(request, 'poggle_play/show_board.html', {'board': board_as_list, 'word_list': final_word_list_valid, 'invalid_word_list': final_word_list_invalid, 'player_name': player_name})

def enter_word(request, boardString, wordString=False):
    if wordString == False:
        return show_board(request, boardString=False)
    
    if len(wordString) <= 3:
        return show_board(request, boardString=False)

    wordString = wordString.lower()
    word_obj = ''

    try:
        word_obj = Word.objects.get(word_string = wordString)
        if word_obj.valid is None:
            word_valid = is_scrabble_valid(wordString)
            word_obj.valid = word_valid
            word_obj.save()

    except:
        word_valid = is_scrabble_valid(wordString)
        word_obj = Word.objects.create(word_string = wordString, valid = word_valid)
    
    board_pk = ''
    board_pk = Board.objects.get(link = boardString)

    #try:
    #except:
        #show_board(request, boardString)

    try:
        Word_Board.objects.get(board = board_pk, word = word_obj)
        return redirect('show_board', boardString = boardString)
    except:
        Word_Board.objects.create(board = board_pk, word = word_obj)

    return redirect('show_board', boardString = boardString)
