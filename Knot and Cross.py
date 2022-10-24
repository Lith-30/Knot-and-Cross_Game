#    1 | 2 | 3
#   ---|---|---
#    4 | 5 | 6
#   ---|---|---
#    7 | 8 | 9

#    (0,0) | (1,0) | (2,0)
#   -------|-------|-------
#    (0,1) | (1,1) | (2,1)
#   -------|-------|-------
#    (0,2) | (1,2) | (2,2)

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


def Start():
    print("this is the key")
    Display_Board({1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"})

    valid_input = False
    key = ""
    player_key = "X"
    computer_key = "O"
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

    if final_status == "player":
        print("You won, good job")
    elif final_status == "computer":
        print("The computer won, better luck next time")
    elif final_status == "tie":
        print("You both tied, not good enough")
    else:
        print("Ran out of turns, bad luck")


def Main_Game(player_key, computer_key) -> str:
    positions = {1: " ", 2: " ", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}
    turns = 0
    while turns < 9:
        positions = Computer_Turn(positions, player_key, computer_key)
        turns += 1

        print("\n")
        Display_Board(positions)
        print("\n")

        game_status = Check_For_Winner(positions, player_key, computer_key)
        if game_status != "":
            return game_status

        if turns < 8:
            position = int(input("Enter the position: "))
            while not Check_Valid_Position(positions, position):
                position = int(input("Enter the position: "))
            positions[position] = player_key
            turns += 1

            print("\n")
            Display_Board(positions)
            print("\n")

            game_status = Check_For_Winner(positions, player_key, computer_key)
            if game_status != "":
                return game_status

    return ""


def Check_For_Winner(positions, player_key, computer_key) -> str:
    player_win = False
    computer_win = False
    vector_set = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]

    player_positions = Take_Positions(positions, player_key)
    computer_positions = Take_Positions(positions, computer_key)
    player_vectors = Integer_To_Vector(player_positions)
    computer_vectors = Integer_To_Vector(computer_positions)

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


def Computer_Turn(positions, player_key, computer_key) -> dict:
    print("Computer turn...\n")

    player_positions = Take_Positions(positions, player_key)

    if len(player_positions) < 1:
        i = 0
        while not Check_Valid_Position(positions, i):
            i += 1
        if Check_Valid_Position(positions, i):
            positions[i] = computer_key

    else:
        computer_positions = Take_Positions(positions, computer_key)
        computer_data = Take_Weightings(Integer_To_Vector(computer_positions), computer_key, positions)
        computer_weightings = computer_data[0]
        computer_win = computer_data[1]

        if computer_win:
            surrounding_vectors = computer_weightings

        else:
            vector_positions = Integer_To_Vector(player_positions)

            weighting_data = Take_Weightings(vector_positions, player_key, positions)
            surrounding_vectors = weighting_data[0]


        position_keys = list(surrounding_vectors.keys())
        if len(position_keys) > 0:
            highest_key = position_keys[0]
            for key in position_keys:
                if surrounding_vectors[key] > surrounding_vectors[highest_key]:
                    highest_key = key
            positions[highest_key] = computer_key

    return positions


def Take_Weightings(vector_positions, key, positions) -> list:
    vector_set = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, -1], [1, 1], [-1, 1], [-1, -1]]
    defence: bool = False
    surrounding_vectors: dict = {}

    for vector in vector_positions:
        for direction in vector_set:
            weighting = 1
            surround_vector = Add_Vector(vector, direction)
            if 0 <= surround_vector[0] <= 2 and 0 <= surround_vector[1] <= 2:
                index = Vector_To_Integer([surround_vector])[0]
                if Check_Valid_Position(positions, index):

                    secondary_vector = Add_Vector(direction, surround_vector)
                    if 0 <= secondary_vector[0] <= 2 and 0 <= secondary_vector[1] <= 2:
                        pos_index = Vector_To_Integer([secondary_vector])[0]
                        if not Check_Valid_Position(positions, pos_index):
                            if positions[pos_index] == key:
                                defence = True

                    surrounding_vectors = Add_To_Weighting_List(surrounding_vectors, index, weighting)

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


def Take_Positions(positions, key) -> list:
    entity_positions = []
    for position in positions:
        if positions[position] == key:
            entity_positions.append(position)

    return entity_positions


def Add_To_Weighting_List(surrounding_vectors, index, weighting) -> dict:
    present = False
    for vectors in surrounding_vectors:
        if vectors == index:
            surrounding_vectors[index] += weighting
            present = True
    if not present:
        surrounding_vectors[index] = weighting

    return surrounding_vectors


def Add_Vector(Vector1, Vector2) -> list:
    return [Vector1[0] + Vector2[0], Vector1[1] + Vector2[1]]


def Integer_To_Vector(positions) -> list:
    vectors = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    final_vectors = []
    for place in positions:
        final_vectors.append(vectors[place])

    return final_vectors


def Vector_To_Integer(vectors) -> list:
    integers = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    keys = integers.keys()
    final_values = []
    for vector in vectors:
        for place in keys:
            if vector == integers[place]:
                final_values.append(place)

    return final_values


def Display_Board(positions):
    index = 1
    while index <= 6:
        print(positions[index] + " | " + positions[index + 1] + " | " + positions[index + 2])
        print("--|---|--")
        index += 3
    print(positions[7] + " | " + positions[8] + " | " + positions[9])


def Check_Valid_Position(positions, position) -> bool:
    for locations in positions:
        if locations == position:
            if positions[locations] == " ":
                return True
            else:
                return False

    return False


Start()
