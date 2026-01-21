//http://127.0.0.1:8000/km52rbxn/

let letterButtons = document.getElementsByClassName("letter_block")
for(i = 0; i < letterButtons.length; i++){
    let button = letterButtons[i]
    button.addEventListener("click",()=>selectLetter(button))
}

let clear_button = document.getElementById("clear")
clear_button.addEventListener("click",()=>clear_board())

update_button_visibility()

function clear_board(){
    let current_word_element = document.getElementById("current_word")
    current_word_element.innerText = ""

    let letterButtons = document.getElementsByClassName("letter_block")

    for(iii = 0; iii < letterButtons.length; iii++){
        let button = letterButtons[iii]
        let button_classes = button.classList

        let index = get_tile_word_index(button_classes)

        if(index !== false){
            button_classes.remove("selected")
            let word_index_to_remove = "word_index_" + index
            button_classes.remove(word_index_to_remove)
        }
    }

    update_button_visibility()
    update_most_recent_selected()

}

function has_word_been_played(current_word){
    current_word = current_word.toLowerCase()

    let played_words = document.getElementsByClassName("played_word")
    let word_list = []

    for(p = 0; p < played_words.length; p++){
        let word = played_words[p].innerText
        word_list.push(word)
    }

    if(word_list.includes(current_word)){
        return true
    }

    else{
        return false
    }
}

function update_button_visibility(){
    let current_word = document.getElementById("current_word").innerText
    let clear_button = document.getElementById("clear")
    let enter_button = document.getElementById("enter_word")
    let already_button = document.getElementById("already_played")

    if(current_word.length == 0){
        clear_button.style.visibility = "hidden";
        enter_button.style.visibility = "hidden";
        already_button.style.visibility = "hidden";

    }
    else if(current_word.length < 4){
        clear_button.style.visibility = "visible";
        enter_button.style.visibility = "hidden";
        already_button.style.visibility = "hidden";
    }
    else{
        let played_already = has_word_been_played(current_word);

        if(played_already){
            clear_button.style.visibility = "visible";
            enter_button.style.visibility = "hidden";
            already_button.style.visibility = "visible";
        }
        else{
            clear_button.style.visibility = "visible";
            enter_button.style.visibility = "visible";
            already_button.style.visibility = "hidden";

            let button_url = current_word + "/"
            enter_button.parentElement.href = button_url
        }

    }
}

function update_most_recent_selected(){
    let letterButtons = document.getElementsByClassName("letter_block")

    for(j = 0; j < letterButtons.length; j ++){
        let block_of_interest = letterButtons[j]
        let block_of_interest_classes = block_of_interest.classList
        block_of_interest_classes.remove("most_recent_letter")
    }

    let block_to_promote = find_most_recent()

    if(block_to_promote){
        block_to_promote.classList.add("most_recent_letter")
    }
}

function find_most_recent(){
    let index_to_beat = -1
    let block_to_promote = false
    let letterButtons = document.getElementsByClassName("letter_block")

    for(j = 0; j < letterButtons.length; j ++){
        let block_of_interest = letterButtons[j]
        let block_of_interest_classes = block_of_interest.classList
       
        if(block_of_interest_classes.contains("selected")){
            let block_index = get_tile_word_index(block_of_interest_classes)
            if(block_index > index_to_beat){
                index_to_beat = block_index
                block_to_promote = block_of_interest
            }
        }
    }

    return block_to_promote

}

function get_tile_column(block){
    let starting_block_classes = block.classList

    for(jj = 0; jj < starting_block_classes.length; jj ++){
        let block_class = starting_block_classes[jj]
        if(block_class.startsWith("col_")){
            let word_col = block_class.replace("col_","")
            word_col = Number(word_col)
            return word_col
        }
    }
}

function get_tile_row(block){
    let parent_div_id = block.parentElement.id
    let word_row = parent_div_id.replace("letter_row_","")
    word_row = Number(word_row)
    return word_row
}

function get_tile_word_index(letter_classes){
    for(i = 0; i < letter_classes.length; i++){
        let letter_class = letter_classes[i]
        if(letter_class.startsWith("word_index_")){
            let word_index = letter_class.replace("word_index_","")
            word_index = Number(word_index)
            return word_index
        }
    }

    return false
}

function selectLetter(letter_button){
    let letter_classes = letter_button.classList
    let current_word_element = document.getElementById("current_word")
    let current_word = current_word_element.innerText

    if(letter_classes.contains("selected")){
    
        let indexToRemoveFrom = get_tile_word_index(letter_classes)
        current_word = current_word.slice(0,indexToRemoveFrom)
        current_word_element.innerText = current_word


        let letterButtons = document.getElementsByClassName("letter_block")

        for(ii = 0; ii < letterButtons.length; ii++){
            let button = letterButtons[ii]
            let button_classes = button.classList

            let index = get_tile_word_index(button_classes)

            if(index >= indexToRemoveFrom){
                button_classes.remove("selected")
                let word_index_to_remove = "word_index_" + index
                button_classes.remove(word_index_to_remove)
            }
        }
    }

    else{
        let start_block = find_most_recent()
        if(start_block){
            let start_row = get_tile_row(start_block)
            let new_row = get_tile_row(letter_button)
            let row_difference = Math.abs(start_row - new_row)

            if(row_difference > 1){
                return
            }

            let start_column = get_tile_column(start_block)
            let new_column = get_tile_column(letter_button)
            let col_difference = Math.abs(start_column - new_column)

            if(col_difference > 1){
                return
            }
        }

        letter_classes.add("selected")

        let word_index_class = "word_index_" + current_word.length
        letter_classes.add(word_index_class)

        let letter = letter_button.innerText
        current_word = current_word + letter.toLowerCase()
        current_word_element.innerText = current_word
    }

    update_button_visibility()
    update_most_recent_selected()
}