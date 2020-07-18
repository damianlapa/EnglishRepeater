from tkinter import *
from database import create_main_table, add_new_word, assign_categories
from googletrans import Translator


class AppMenu:
    def __init__(self, env):
        self.env = env
        self.new_word_button = Button(text='Add new word', command=self.add_new_word)
        self.repeat_button = Button(text='Repeat', command=self.repeat_words)
        self.new_word_frame = None
        self.repeat_frame = Frame(self.env)
        self.menu_display()
        self.run()

    def menu_display(self):
        self.repeat_button.pack()
        self.new_word_button.pack()

    def repeat_words(self):
        self.new_word_button.pack_forget()
        self.repeat_frame.pack()

    def add_new_word(self):
        self.new_word_button.pack_forget()
        self.repeat_button.pack_forget()
        if not self.new_word_frame:
            def add_word():
                translator = Translator()
                translation = translator.translate(english.get(), dest='pl', src='en')
                print(translation)
                print(translation.text)
                add_new_word(english.get(), translation.text)
                self.new_word_frame.destroy()
                self.new_word_frame = None
                self.menu_display()

            def dynamic_translation(event):

                translator = Translator()
                translation = translator.translate(english.get(), dest='pl')
                print(event, english.get(), translation.text)
                polish.delete(0, END)
                polish.insert(0, translation.text)

            self.new_word_frame = Frame(self.env)
            english_label = Label(self.new_word_frame, text='English')
            english_label.pack()
            english = Entry(self.new_word_frame)
            english.pack()
            polish_label = Label(self.new_word_frame, text='Polish')
            polish_label.pack()
            polish = Entry(self.new_word_frame)
            polish.pack()
            add_button = Button(self.new_word_frame, text='ADD!', command=add_word)
            add_button.pack()
            self.new_word_frame.pack()
            english.bind('<KeyRelease>', dynamic_translation)
        else:
            pass

    def run(self):
        assign_categories()
        self.env.mainloop()


if __name__ == '__main__':
    environment = Tk()
    environment.title('English repeater')
    environment.geometry('300x300')
    app_start = AppMenu(environment)
