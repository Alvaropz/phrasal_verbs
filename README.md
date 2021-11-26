# Phrasal Verbs

## Table of Contents:

* [General Info](#general-info)
* [Technologies](#techonologies)
* [Setup](#setup)

## General Info:

This project allows a (Spanish speaker) user to improve their knowledge in phrasal verbs retrieved from a databse in Postgres. This project is divided in two files:

* **db.py**: This file first checks if the database exists in Postgres, if so, it connects with the database, if not, it creates a new one with the table 'phrasal_verb' included. Then it connnects this file with the database. About their functions, there are serie of them that allows to insert, retrieve and update the database. The function *pv_exists_query()* is a helper function for the *insert()*, and allows to check if the phrasal verb already exists in the database.

* **phrasal_verbs.py**: This file allows the user to interact with the database. 
  *  The main function is *game()*, which actually allows the user to study the phrasal verbs. This function keeps track of how many right answers and attempts has tried. Also gives to the user feedback about their results.
  *  *insert()* and *pv_exists()*: Allows to insert new phrasal verbs in the database. The columns associated are *phrasal_verbs*, *explanations* and *English examples* (which are arrays) and, *Spanish equivalent*, which allows the player to know what it's the Spanish equivalent if they are not sure about the answer when playing. Thie function handles the situation where a phrasal verb might already exist in the database.
  *  *retrieve()*: Allows to retrieve all rows in the database. This handles a situation where a user is actually updating one or more phrasal verbs, or adding new ones. This is done this way to show the user the ids and their corresponding phrasal verbs.
  *  *update(), modify_this_data() and modify_explanations_examples()*: 
    *  The function *update()* is a bit tricky as it nees many additional checks to work. That's why *modify_this_data() and modify_explanations_examples()* were created as helper functions. 
    *  As *update()* cannot know what column you want to modify, it goes through all of them. So the user can select if they want to modify one or more rows. *modify_this_data()* is a helper function where they program ask the user if the current data (e.g.: "Phrasalverb") has to be modfied, if so, it allows to modify the user that data. 
    *  The function *modify_explanations_examples()* allows to modify, remove or add new explanations and/or examples to their corresponding arrays. First it asks what task wants the user to perform by iterating through the list. When it finishes iterating through the list, the user can add more explanations/examples.

  *  *guess_pv()*: This functions is pretty simple. It retrieves all data from the database, then it randomly selects three options, then it selects a phrasal verb target to guess. If the answer is right, the user gets a point.

## Technologies:

Project is created with:
* Visual Studio Code
* Git
* GitHub
* psycopg2 library
* Python for Visual Studio Code

## Setup:

* Git: [Git - Installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Visual Studio Code: [Visual Studio Code](https://code.visualstudio.com)
