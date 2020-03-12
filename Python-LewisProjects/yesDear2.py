import pyttsx3
from tkinter import *
from tkinter import ttk
from random import randint


class Application(Frame):
    """A GUI Application """
    
    def __init__(self, master):
        """ Initialise the Frame """
        ttk.Frame.__init__(self, master)

        self.my_voice = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN - US_' + \
                        varVoice.get() + '_11.0'
        # self.my_voice = 'com.apple.speech.synthesis.voice.' + varVoice.get()
        self.voices = []
        self.voices = get_voices()

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create the window layout. """
        my_font = ('Lucinda Grande', 12)

        # Create Name Label
        self.label1 = \
            Label(self, font = my_font, text="This is the equivalent to the 'Yes, Dear' button!").grid(row=0, column=1)
        
        # Create Play Button
        self.play_button = \
            Button(self, font=my_font, text="Play", command=play_statement(self.my_voice)).grid(row=1, column=1)

        # Create Voice Label
        self.label2 = Label(self, font=my_font, text="Select a voice").grid(row=3, column=1)

        # Create combobox for voices
        self.cb_voice = ttk.Combobox(self, font=my_font, width=12, textvariable=varVoice)
        self.cb_voice.bind("<Return>", self.cb_voice_onEnter) # when the enter key is pressed an event happens
        self.cb_voice.bind('<<ComboboxSelected>>', self.cb_voice_onEnter)
        self.cb_voice['values'] = self.voices
        self.cb_voice.grid(row=4, column=1, sticky='w')

        # Create Quit button
        self.close_button = Button(self, text="Quit", command=quit_app).grid(row=6, column=1)

    def cb_voice_onEnter(self, event):
        # get the value of the text in the combo box, voice

        # self.my_voice = 'com.apple.speech.synthesis.voice.' + varVoice.get()
        self.my_voice = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN - US_' + \
                        varVoice.get() + '11.0'


def get_voices():
    voices = engine.getProperty('voices')
    voice_list = []
    for voice in voices:
        voice_list.append(voice.name)
        engine.runAndWait()
    return voice_list


def play_statement(voice):
    global limit, statements
    index = randint(0, limit-1)
    engine.setProperty('voice', voice)
    engine.say(statements[index])
    engine.runAndWait()


def get_statements():
    statements_list = []
    file = open('./yesDearStatements.txt', 'r')
    for line in file:
        statements_list.append(line)
    return statements_list


def quit_app():
    quit()


if __name__ == "__main__":
    
    engine = pyttsx3.init()
    statements = get_statements()
    limit = len(statements)
    
    root = Tk()
    root.title("YesDear")
    root.geometry("400x300")                            
    # varVoice = StringVar(root, value='daniel')
    varVoice = StringVar(root, value='DAVID')

    # creation of an instance
    app = Application(root)
    
    # mainloop
    root.mainloop()
