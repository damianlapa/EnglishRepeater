from tkinter import *
from database import create_main_table, add_new_word, assign_categories, words_to_repeat, category_action
from googletrans import Translator
from local_settings import first_language, second_language


class AppMenu:
    def __init__(self, env):
        self.env = env
        self.new_word_button = Button(text='Add new word', command=self.add_new_word)
        self.repeat_button = Button(text='Repeat', command=self.repeat_words)
        self.main_menu_button = Button(text='<', font='Helvetica 30 bold', command=self.return_to_main_menu)
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

    def repeat_words(self):
        def repeat():
            def answer(action):
                color = 'red' if action == '-' else 'green'
                category_action(words[self.counter][0], action)
                self.correct_answer = words[self.counter][2]
                self.correct_answer_label = Label(self.repeat_frame, text=self.correct_answer,
                                                  font='Helvetica 15', fg='{}'.format(color))
                self.correct_answer_label.grid(row=3, column=1, columnspan=2, sticky=W + E + N + S)
                correct_button.configure(state=DISABLED)
                wrong_button.configure(state=DISABLED)
                self.counter += 1 if self.counter != len(words) - 1 else 0
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
        # assign_categories()
        self.env.mainloop()


if __name__ == '__main__':
    environment = Tk()
    environment.title('English repeater')
    environment.geometry('300x300')
    app_start = AppMenu(environment)
