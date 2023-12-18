# all the positions on the board
#    1 | 2 | 3
#   ---|---|---
#    4 | 5 | 6
#   ---|---|---
#    7 | 8 | 9

# all the positions and their 'vector' coordinates
#    (0,0) | (1,0) | (2,0)
#   -------|-------|-------
#    (0,1) | (1,1) | (2,1)
#   -------|-------|-------
#    (0,2) | (1,2) | (2,2)

# plan for other project (ignore)
#    _________________________________________
#  H | BC | BH | BR | BQ | BK | BR | BH | BC |
#    |----|----|----|----|----|----|----|----|
#  G | BP | BP | BP | BP | BP | BP | BP | BP |
#    |----|----|----|----|----|----|----|----|
#  F |    |    |    |    |    |    |    |    |
#    |----|----|----|----|----|----|----|----|
#  E |    |    |    |    |    |    |    |    |
#    |----|----|----|----|----|----|----|----|
#  D |    |    |    |    |    |    |    |    |
#    |----|----|----|----|----|----|----|----|
#  C |    |    |    |    |    |    |    |    |
#    |----|----|----|----|----|----|----|----|
#  B | WP | WP | WP | WP | WP | WP | WP | WP |
#    |----|----|----|----|----|----|----|----|
#  A | WR | WH | WB | WQ | WK | WB | WH | WR |
#    |---------------------------------------|
#      1    2    3    4    5    6    7    8


import random

def Start():
    # display which number associates to which position on the board
    print("this is the key")
    Display_Board({1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"})

    valid_input = False
    key = ""
    player_key = "X"
    computer_key = "O"
    # allow player to determine their preferred key
    while not valid_input:
        key: str = input("Type \'x\' or \'o\': ")
        if key == "x" or key == "X":
            player_key = "X"
            computer_key = "O"
            valid_input = True
        elif key == "o" or key == "O":
            player_key = "O"
            computer_key = "X"
            valid_input = True
    print("you are now playing as \'" + key + "\'")

    final_status = Main_Game(player_key, computer_key)

    # output final message depending on outcome of game
    if final_status == "player":
        print("You won, good job")
    elif final_status == "computer":
        print("The computer won, better luck next time")
    elif final_status == "tie":
        print("You both tied, not good enough")
    else:
        print("Ran out of turns, bad luck")


def Main_Game(player_key, computer_key) -> str:  # plays each of the turns for the player and computer
    # hold all the positions of the player and computer
    positions = {1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}
    turns = 0

    # plays each turn, computer goes first then player
    while turns < 9:
        positions = Computer_Turn(positions, player_key, computer_key)
        turns += 1

        print("\n")
        Display_Board(positions)  # show the move the board plays
        print("\n")

        game_status = Check_For_Winner(positions, player_key, computer_key)  # check for winner
        if game_status != "":
            return game_status

        if turns < 8:
            position = int(input("Enter the position: "))
            # make sure that the position the player wants to use is not taken
            while not Check_Valid_Position(positions, position):
                position = int(input("Enter the position: "))
            positions[position] = player_key
            turns += 1

            print("\n")
            Display_Board(positions)
            print("\n")

            game_status = Check_For_Winner(positions, player_key, computer_key)  # check for winner
            if game_status != "":
                return game_status

    return ""


def Check_For_Winner(positions, player_key, computer_key) -> str:
    player_win = False
    computer_win = False
    # a set of arrays that act like 'vectors', used to find the surrounding positions
    vector_set = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]

    player_positions = Take_Positions(positions, player_key)  # get all positions of player
    computer_positions = Take_Positions(positions, computer_key)  # get all positions of computer
    # converts the positions of player and computer into 'vector' positions
    player_vectors = Integer_To_Vector(player_positions)
    computer_vectors = Integer_To_Vector(computer_positions)

    # go through all the positions of the player and computer, then finds any sets of vectors that are collinear or in
    # a straight line
    for player_vector in player_vectors:
        for vector in vector_set:
            new_pos = Add_Vector(player_vector, vector)
            if new_pos in player_vectors:
                second_pos = Add_Vector(new_pos, vector)
                if second_pos in player_vectors:
                    player_win = True

    for computer_vector in computer_vectors:
        for vector in vector_set:
            new_pos = Add_Vector(computer_vector, vector)
            if new_pos in computer_vectors:
                second_pos = Add_Vector(new_pos, vector)
                if second_pos in computer_vectors:
                    computer_win = True

    if player_win and not computer_win:
        return "player"
    elif not player_win and computer_win:
        return "computer"
    elif player_win and computer_win:
        return "tie"

    return ""


def Computer_Turn(positions, player_key, computer_key) -> dict:  # computer turn
    print("Computer turn...\n")

    # get positions of player
    player_positions = Take_Positions(positions, player_key)

    if len(player_positions) < 1:  # if player has not played yet, use a random position
        i = 0
        while not Check_Valid_Position(positions, i):
            i = random.randint(1,9)
        if Check_Valid_Position(positions, i):
            positions[i] = computer_key

    else:
        computer_positions = Take_Positions(positions, computer_key)  # get computer positions

        # Take weightings of all potential positions for the computer to win
        computer_data = Take_Weightings(Integer_To_Vector(computer_positions), computer_key, positions)
        computer_weightings = computer_data[0]  # return all locations for the computer, may not be used
        computer_win = computer_data[1]  # will be true if the computer can win in this turn

        # if computer can win, will take the move else it will stop the player from winning
        if computer_win:
            surrounding_vectors = computer_weightings

        else:
            vector_positions = Integer_To_Vector(player_positions)

            weighting_data = Take_Weightings(vector_positions, player_key,
                                             positions)  # get potential positions for player
            surrounding_vectors = weighting_data[0]

        # take the position with the highest weighting and places a knot/cross there
        position_keys = list(surrounding_vectors.keys())
        if len(position_keys) > 0:
            highest_key = position_keys[0]
            for key in position_keys:
                if surrounding_vectors[key] > surrounding_vectors[highest_key]:
                    highest_key = key
            positions[highest_key] = computer_key

    return positions


def Take_Weightings(vector_positions, key, positions) -> list:  # brains of computer
    # an array of arrays that each act like 'vectors,' each of the vectors are meant to represent the relative position
    # of a surrounding vector from the original position
    vector_set = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]
    defence: bool = False  # flag for whether there is only one move left until a win
    surrounding_vectors: dict = {}  # dictionary of all the positions and their weightings (not in 'vector' form

    # cycle through all the positions inputted and create a dictionary of positions and their weightings, also determine
    # whether the game can be won in one move
    for vector in vector_positions:
        for direction in vector_set:
            weighting = 1  # set the weighting (reset for every position)
            # look at a position around the original position and determine if it is in the board
            surround_vector = Add_Vector(vector, direction)
            if 0 <= surround_vector[0] <= 2 and 0 <= surround_vector[1] <= 2:
                index = Vector_To_Integer([surround_vector])[0]
                # if the surrounding position is free, check to see if the next position collinear found by adding the
                # same vector again to the result the current two positions is taken, if so then the game can be won in
                # one turn
                if Check_Valid_Position(positions, index):

                    secondary_vector = Add_Vector(direction, surround_vector)
                    if 0 <= secondary_vector[0] <= 2 and 0 <= secondary_vector[1] <= 2:
                        pos_index = Vector_To_Integer([secondary_vector])[0]
                        if not Check_Valid_Position(positions, pos_index):
                            if positions[pos_index] == key:
                                defence = True
                    # add any position to the weighting list
                    surrounding_vectors = Add_To_Weighting_List(surrounding_vectors, index, weighting)

                # if the surrounding position is taken, check to see the next position is taken, if so then the game can
                # be won in one turn
                elif positions[index] == key:
                    side_vector_one = Add_Vector(vector, [-direction[0], -direction[1]])
                    side_vector_two = Add_Vector(surround_vector, direction)

                    if 0 <= side_vector_one[0] <= 2 and 0 <= side_vector_one[1] <= 2:
                        index1 = Vector_To_Integer([side_vector_one])[0]
                        if Check_Valid_Position(positions, index1):
                            surrounding_vectors = Add_To_Weighting_List(surrounding_vectors, index1, weighting + 1)
                            defence = True

                    if 0 <= side_vector_two[0] <= 2 and 0 <= side_vector_two[1] <= 2:
                        index2 = Vector_To_Integer([side_vector_two])[0]
                        if Check_Valid_Position(positions, index2):
                            surrounding_vectors = Add_To_Weighting_List(surrounding_vectors, index2, weighting + 1)
                            defence = True

    return [surrounding_vectors, defence]


def Take_Positions(positions, key) -> list:  # return a list with all the positions which have either a knot or cress
    entity_positions = []
    for position in positions:
        if positions[position] == key:
            entity_positions.append(position)

    return entity_positions


def Add_To_Weighting_List(surrounding_vectors, index, weighting) -> dict:
    # add a postion to the weighting dictionary, if the position already exists then add to its weighting
    present = False
    for vectors in surrounding_vectors:
        if vectors == index:
            surrounding_vectors[index] += weighting
            present = True
    if not present:
        surrounding_vectors[index] = weighting

    return surrounding_vectors


def Add_Vector(Vector1, Vector2) -> list:   # 'add' the lists as if they were vectors
    return [Vector1[0] + Vector2[0], Vector1[1] + Vector2[1]]


def Integer_To_Vector(positions) -> list:   # convert the number positions to the vector counterpart
    vectors = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    final_vectors = []
    for place in positions:
        final_vectors.append(vectors[place])

    return final_vectors


def Vector_To_Integer(vectors) -> list:  # convert a list of vectors into their integer position counter part
    integers = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    keys = integers.keys()
    final_values = []
    for vector in vectors:
        for place in keys:
            if vector == integers[place]:
                final_values.append(place)

    return final_values


def Display_Board(positions):  # display the board by priting it out
    index = 1
    while index <= 6:
        print(positions[index] + " | " + positions[index + 1] + " | " + positions[index + 2])
        print("--|---|--")
        index += 3
    print(positions[7] + " | " + positions[8] + " | " + positions[9])


def Check_Valid_Position(positions, position) -> bool:  # check if position is not taken
    for locations in positions:
        if locations == position:
            if positions[locations] == " ":
                return True
            else:
                return False

    return False


Start()
