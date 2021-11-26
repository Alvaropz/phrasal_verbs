import db
import random

# Inserting data in the database.
def insert():
    # Data format insertion example: '', [], [], ''
    phrasal_verb = input('Type a phrasal verb (get off): ').strip().lower()
    pv_retrieved = pv_exists(phrasal_verb)
    if not pv_retrieved:
        continue_bool = "y"
        explanations_list = []
        while continue_bool != "n":
            if continue_bool == "y":
                explanations_list.append(input('Type an explanation (If you get off something that you are on, you move your body from it, usually onto the ground): ').strip().capitalize())
            continue_bool = continue_insert("explanations")

        continue_bool = "y"
        english_examples_list = []
        while continue_bool != "n":
            if continue_bool == "y":
                english_examples_list.append(input('Type an English example (He got off his bicyle): ').strip().capitalize())
            continue_bool = continue_insert("examples")
        
        spanish_equivalent = input('Type the Spanish equivalent (Bajarse): ').strip().capitalize()
        db.inserting_data(phrasal_verb, explanations_list, english_examples_list, spanish_equivalent)
    else:
        print("'{}' already exists in the database.".format(pv_retrieved))


def continue_insert(step):
    active = input('Do you want to add more {}? Type "Y" for continuing, "N" to stop: '.format(step)).strip().lower()
    if active != "y" and active != "n":
        print('That is not a valid option.')
    return active

def pv_exists(phrasal_verb):
    fetchedData = db.pv_exists_query(phrasal_verb)
    return fetchedData

# Retrieve data from the database.
def retrieve(*update):
    fetchedData = db.all_data_query()
    pv_retrieved = []
    for row in fetchedData:
        pv_retrieved.append(dict(row))
        if update:
            print("{}. {}".format(row['id'], row['phrasal_verb']))
    return pv_retrieved

# Update de data in the database.
def update():
    retrieved_data = retrieve(True)
    id_chosen = input("Type the 'id' number you want to use to update the data: ")
    if id_chosen.isdigit():
        for row in retrieved_data:
            if row['id'] == int(id_chosen):
                data = row
                break
        print("Now you are modifying '{}'".format(data['phrasal_verb'].upper()))
        modify_data = modify_this_data('phrasal verb')
        if modify_data:
            data['phrasal_verb'] = input('Type your phrasal verb modification: ').strip().lower()
        modify_data = modify_this_data('explanations')
        if modify_data:
            data['explanations'] = modify_explanations_examples(data['explanations'], 'explanation')
        modify_data = modify_this_data('English exammples')
        if modify_data:
            data['english_examples'] = modify_explanations_examples(data['english_examples'], 'example')
        modify_data = modify_this_data('Spanish equivalent')
        if modify_data:
            data['spanish_equivalent'] = input('Type your Spanish equivalent modification: ').strip().capitalize()
    else:
        print('Please, type a valid number.')
    db.update_query(data['id'], data['phrasal_verb'], data['explanations'], data['english_examples'], data['spanish_equivalent'])

def modify_this_data(step):
    modify_data = ''
    while modify_data != 'y' or modify_data != 'n':
        if modify_data == 'y':
            return True
        elif modify_data == 'n':
            return False
        modify_data = input("Do you want to modify '{}'? 'Y' if you want, 'N' if you don't want to: ".format(step)).strip().lower()


def modify_explanations_examples(data_list, type):
    # Allows to modify the explanations/examples lists by asking if the user wants to modify an existing explanation/exmple and/or adding a new one
    i = 0
    while i < len(data_list):
        change = ''
        while change != 'y' or change != 'n':
            if change != 'y':
                change = input("Do you want to modify/remove '{}'? Type 'Y' for modifying/removing this {}, 'N' to skip: ".format(data_list[i], type)).strip().lower()
            if change == 'y':
                modify_remove = input('Do you want or "remove" or "modify" this data? Type "Remove" or "Modify": ').strip().lower()
                if modify_remove == "remove":
                    del data_list[i]
                    i -= 1
                    break
                if modify_remove == "modify":
                    data_list[i] = input('Type your {} modification: '.format(type)).strip().capitalize()
                    break
                else:
                    print("That is not a valid action.")
            elif change == 'n':
                break
        i += 1
    add_more = ''
    while add_more != 'y' or add_more != 'n':
        add_more = input("Do you want add another {0}? Type 'Y' to add another {0}. 'N' to stop adding {0}s: ".format(type)).strip().lower()
        if add_more == 'y':
            data_list.append(input('Type your new {}: '.format(type)).strip().capitalize())
        elif add_more == 'n':
            break
    return data_list

# Knowledge test function
def guess_pv(points, attemps):
    pv_complete_list = retrieve()
    if len(pv_complete_list) < 3:
        print('There is not enough data in the database.')
        return points, attemps

    # Select three random phrasal verbs from all available
    options_list = random.sample(pv_complete_list, 3)

    # Select one phrasal verb target to guess
    index = random.choice(range(len(options_list)))
    choice = options_list[index]
    pv_target = choice['phrasal_verb']
    explanation_index = random.choice(range(len(choice['explanations'])))
    explanation_target = choice['explanations'][explanation_index]

    # Randomly set phrasal verbs to three options answers
    first = random.choice(options_list)
    options_list.remove(first)
    second = random.choice(options_list)
    options_list.remove(second)
    third = random.choice(options_list)
    options_list.remove(third)

    # Allows type an answer. Then it checks if it's right
    print('What phrasal verb does the explanation "{}" belong to?'.format(explanation_target))
    print("1. {}\n2. {}\n3. {}".format(first['phrasal_verb'], second['phrasal_verb'], third['phrasal_verb']))
    answer = input('Type the phrasal verb as you see it in options: ').strip().lower()
    if pv_target == answer:
        spanish_equ = choice['spanish_equivalent']
        random_english_example = choice['english_examples'][explanation_index]
        print("Correct! The Spanish equivalent is '{}' and an example in English might be '{}'".format(spanish_equ, random_english_example))
        points += 1
    else:
        print('Wrong answer!')
    return points, attemps + 1

def game():
    points = 0
    attemps = 0
    keep_playing = "y"
    while keep_playing != "n":
        if keep_playing == "y":
            points, attemps = guess_pv(points, attemps)
        keep_playing = input('Type "Y" for keeping playing, "N" to stop. If you type something else, you will be ask again: ').lower()

    # Gives feeback to the player about their results.
    percentage = 0
    if attemps != 0:
        percentage = round((points/attemps)*100, 2)
    formated_right_attempts = str(points) + "/" + str(attemps)
    if percentage == 100:
        print('Well done! You got 100% score! With a {} of right answers/attemps.'.format(formated_right_attempts))
    elif percentage >= 80:
        print('Good job! You were close! You got {} score. With a {} of right answers/attemps.'.format(str(percentage) + '%', formated_right_attempts))
    elif percentage >= 50:
        print('Not bad! You have to keep practicing a bit! You got {} score. With a {} of right answers/attemps.'.format(str(percentage) + '%', formated_right_attempts))
    else:
        print('Oh no! You got {} score. That\'s fewer than 50% of total score, but don\'t worry, you just to practice a bit more! With a {} of right answers/attemps.'.format(str(percentage) + '%', formated_right_attempts))

db.stop_connection()