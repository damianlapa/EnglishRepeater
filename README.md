# ENGLISH REPEATER

Simple application based on Tkinter and postgres database which allows to learn new words using flashcards. 

#### Setup guide

* Install requirements from requirements.txt
* Create database using postgres
* Create file local_settings.py, where you will add data necessary to connect with database
* Each time when you will run an app, it will try to create main table *'words'*, where will be keeping all words you want to repeat
* That's all!

#### User guide

After run an app there will appear three buttons:

1) **Repeat**: a main functionality of the app. It will displays how many words are to repeat and we can run them by click tu **START** button.
2) **Add new word**: an option that allows us to add new words to our main table **words**. By default it displays two text areas titled *English* and *Polish*.
When you will type something in first text area it will automatically t**ranslate to another language and displays translation in another text area, which can be manually edited anyway. 
3) **<** button allows to return to main menu

##### How to change languages?
By default app works on english and polish languages but it can be easily changed. In your *local_settings.py* file you will 
have to change one of *first_language*, *second_language* or both of them.  
There is a list of available languages:  
[languages](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages)

#### How it works?

* When you will add a new word it will received it owns category(by default it'll be 0) and last correct answer feature 
which will equals to its create time
* While you run repeat module, you will be able to click or *+* or *x* buttons. They represents if you know this word or not.  
When you choose '+' option an app will update last correct answer feature and word's category feature by 1.  
Otherwise a last correct answer feature remains as it was but category feature drops dependently of its previous value.

##### Word categories

| Category | To repeat after: |
| ----------- | ----------- |
| 0 | immediately |
| 1 | 6 hours |
| 2 | 1 day |
| 3 | 3 days |
| 4 | 7 days |
| 5 | 15 days |
| 6 | 45 days |