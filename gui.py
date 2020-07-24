from tkinter import *
from database import create_main_table, add_new_word, words_to_repeat, category_action, delete_record, get_all_records
from time import sleep
from googletrans import Translator
from local_settings import first_language, second_language


class AppMenu:
    def __init__(self, env):
        self.env = env
        self.new_word_button = Button(text='Add new word', command=self.add_new_word)
        self.repeat_button = Button(text='Repeat', command=self.repeat_words)
        self.main_menu_button = Button(text='<', font='Helvetica 30 bold', command=self.return_to_main_menu)
        self.edit_database_button = Button(text='Edit database', command=self.edit_database)
        self.all_records_frame = Frame(self.env)
        self.records_table = Frame(self.all_records_frame)
        self.word_en = None
        self.word_pl = None
        self.correct_answer = ''
        self.correct_answer_label = None
        self.repeat_start_button = None
        self.counter = 0
        self.new_word_frame = None
        self.repeat_frame = Frame(self.env)
        create_main_table()
        self.menu_display()
        self.run()

    def menu_display(self):
        self.repeat_button.pack()
        self.new_word_button.pack()
        self.main_menu_button.pack()
        self.edit_database_button.pack()

    def edit_database(self):
        def all_records():
            return get_all_records()

        def create_table():
            id_label = Label(self.all_records_frame, text='ID', borderwidth=2, relief="solid")
            id_label.grid(column=0, row=0, sticky=W + E)
            en_label = Label(self.all_records_frame, text='English', borderwidth=2, relief="solid")
            en_label.grid(column=1, row=0, sticky=W + E)
            pl_label = Label(self.all_records_frame, text='Polish', borderwidth=2, relief="solid")
            pl_label.grid(column=2, row=0, sticky=W + E)
            category = Label(self.all_records_frame, text='Category', borderwidth=2, relief="solid")
            category.grid(column=3, row=0, sticky=W + E)
            last_correct = Label(self.all_records_frame, text='Last Answer', borderwidth=2, relief="solid")
            last_correct.grid(column=4, row=0, sticky=W + E)
            delete = Label(self.all_records_frame, text='Delete', borderwidth=2, relief="solid")
            delete.grid(column=5, row=0, sticky=W + E)

        def display_records(num):
            row_num = 0
            for num in range(0, num):
                record = get_all_records()[num]
                for i in range(0, 6):
                    if i == 5:
                        delete_button = Button(self.all_records_frame, text='DELETE',
                                               command=lambda x=record[0]: delete_record(x))
                        delete_button.grid(row=row_num + 1, column=i)
                    else:
                        record_label = Label(self.all_records_frame, text='{}'.format(str(record[i])))
                        record_label.grid(row=row_num + 1, column=i)
                row_num += 1

            self.records_table.grid(column=0, row=1, columnspan=5, sticky=W + E)

        self.repeat_button.pack_forget()
        self.new_word_button.pack_forget()
        self.main_menu_button.pack_forget()
        self.edit_database_button.pack_forget()
        self.all_records_frame.pack()
        create_table()
        display_records(5)

    def repeat_words(self):
        def repeat():
            def answer(action):
                def end_repetition():
                    pass

                color = 'red' if action == '-' else 'green'
                category_action(words[self.counter][0], action)
                self.correct_answer = words[self.counter][2]
                self.correct_answer_label = Label(self.repeat_frame, text=self.correct_answer,
                                                  font='Helvetica 15', fg='{}'.format(color))
                self.correct_answer_label.grid(row=3, column=1, columnspan=2, sticky=W + E + N + S)
                correct_button.configure(state=DISABLED)
                wrong_button.configure(state=DISABLED)
                self.counter += 1 if self.counter != len(words) - 1 else 0
                if self.counter == len(words) - 1:
                    if len(words_to_repeat()) == 0:
                        self.repeat_frame.after(1000, self.return_to_main_menu)
                    else:
                        self.repeat_frame.pack_forget()
                        self.repeat_frame.destroy()
                        self.repeat_frame = Frame(self.env)
                        self.repeat_words()
                        return
                self.repeat_frame.after(1000, repeat)

            words_to_repeat_label.pack_forget()
            self.repeat_start_button.pack_forget()
            if self.correct_answer_label:
                self.correct_answer_label.destroy()
            self.word_en = Label(self.repeat_frame, text=words[self.counter][1], font='Helvetica 15')
            self.word_en.grid(row=1, column=1, columnspan=2, sticky=W + E + N + S)
            correct_button = Button(self.repeat_frame, text='+', font='Helvetica 30', fg='green',
                                    command=lambda: answer('+'))
            wrong_button = Button(self.repeat_frame, text='x', font='Helvetica 30', fg='red',
                                  command=lambda: answer('-'))
            correct_button.grid(row=2, column=1)
            wrong_button.grid(row=2, column=2)

        self.new_word_button.pack_forget()
        self.repeat_button.pack_forget()
        self.repeat_frame.pack()
        self.counter = 0
        words = words_to_repeat()

        words_to_repeat_label = Label(self.repeat_frame, text='You have {} words to repeat'.format(len(words)),
                                      font='Helvetica 15')
        words_to_repeat_label.pack()
        self.repeat_start_button = Button(self.repeat_frame, text='START', command=repeat)
        if len(words) == 0:
            self.repeat_start_button.configure(state=DISABLED)
        self.repeat_start_button.pack()

    def add_new_word(self):
        self.new_word_button.pack_forget()
        self.repeat_button.pack_forget()
        if not self.new_word_frame:
            def add_word():
                translator = Translator()
                translation = translator.translate(english.get(), dest=second_language[1], src=first_language[1])
                add_new_word(english.get(), translation.text)
                self.new_word_frame.destroy()
                self.new_word_frame = None
                self.menu_display()

            def dynamic_translation(event):

                translator = Translator()
                translation = translator.translate(english.get(), dest=second_language[1])
                polish.delete(0, END)
                polish.insert(0, translation.text)

            self.new_word_frame = Frame(self.env)
            english_label = Label(self.new_word_frame, text=first_language[0])
            english_label.pack()
            english = Entry(self.new_word_frame)
            english.pack()
            polish_label = Label(self.new_word_frame, text=second_language[0])
            polish_label.pack()
            polish = Entry(self.new_word_frame)
            polish.pack()
            add_button = Button(self.new_word_frame, text='ADD!', command=add_word)
            add_button.pack()
            self.new_word_frame.pack()
            english.bind('<KeyRelease>', dynamic_translation)
        else:
            pass

    def return_to_main_menu(self):
        if self.new_word_button:
            self.new_word_button.pack_forget()
        if self.repeat_button:
            self.repeat_button.pack_forget()
        if self.repeat_frame:
            self.repeat_frame.pack_forget()
            self.repeat_frame.destroy()
            self.repeat_frame = Frame(self.env)
        if self.repeat_start_button:
            self.repeat_start_button.pack_forget()
        if self.new_word_frame:
            self.new_word_frame.pack_forget()
            self.new_word_frame.destroy()
            self.new_word_frame = None
        self.menu_display()

    def run(self):
        self.env.mainloop()


if __name__ == '__main__':
    environment = Tk()
    environment.title('English repeater')
    environment.geometry('300x300')
    app_start = AppMenu(environment)
