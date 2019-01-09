from tkinter import *
from tkinter import ttk
import string
import random
import similarity

def submitForm(*args):
    try:
        masukan_helper = chatInput.get()
        text.config(state=NORMAL)
        text.insert(INSERT,"Anda   : "+masukan_helper+"\n")

        fp = similarity.FinalProject.default()
        
        masukan = {
			'raw_input' : masukan_helper,
			'processed' : re.sub('['+string.punctuation+']', "", re.sub(r"[0-9]", "", masukan_helper.casefold()))
        }

        top = fp.predict(masukan, 2)
        selected = random.choice(top)
        
        text.insert(INSERT,"Penjual: "+selected.get('response')+"\n")
        text.config(state=DISABLED)   
        chatInput.delete(0, END)
    except ValueError:
        pass

if __name__ == "__main__":
    utama = Tk()
    utama.title('Chat')

    frametext = ttk.Frame(utama, padding="10 10 10 5", borderwidth=2, relief='sunken')
    frametext.grid(column=0, row=0, sticky=(N, W, E, S))

    frameinput = ttk.Frame(utama, padding="10 5 10 10", borderwidth=2, relief='sunken')
    frameinput.grid(column=0, row=1, sticky=(N, W, E, S))

    utama.columnconfigure(0, weight=1)
    utama.rowconfigure(0, weight=1)

    text = Text(frametext, width=50, height=30, state=DISABLED, wrap=WORD)
    text.grid(column=0, row=0, columnspan=3, sticky=W)

    chatText = StringVar()
    chatInput = ttk.Entry(frameinput, width=53, textvariable=chatText)
    chatInput.grid(column=0, row=1, columnspan=2, sticky=W)

    sendButton = ttk.Button(frameinput, text="Send", command=submitForm).grid(column=2, row=1, sticky=E)

    utama.bind('<Return>', submitForm)

    utama.mainloop()