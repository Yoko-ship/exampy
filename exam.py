from google import genai
from dotenv import load_dotenv
import os
from tkinter import *
from tkinter import Text
import asyncio
load_dotenv()

class Tkinter:
    def __init__(self,size,title):
        self.root = Tk()
        self.root.geometry(size)
        self.title = title
        self.font = ("Arial",15)
        self.__labels()

    def _confirm_button(self):
        self.entry_variant =  self.variant.get()
        self.entry_prompt =   self.prompt.get()
        self.prompt.set("")
        asyncio.run(self.__response_gemini())



    async def __response_gemini(self):
        self.gemini = Gemini()
        try:
            self.model = self.gemini.client.models.generate_content(model="gemini-2.0-flash-exp",contents=self.entry_prompt)
            self.generated_content = self.model.text.replace("*","")
            with open("exam.txt","a",encoding="UTF-8") as file:
                if self.entry_variant == 0:
                    file.write(f"Вопрос: {self.entry_prompt} \n Ответ:{self.generated_content} \n")
                    self.success.set("Ответ успешно записан")
                else:
                    file.write(f"Вариант:{self.entry_variant} \n Вопрос:{self.entry_prompt} \n Ответ:{self.generated_content} \n")
                    self.success.set("Ответ успешно записан")

        
        except ValueError:
            self.error.set("Пожалуста заполните поле 'Запрос' ")
    
        else:
            self.variant.set(0)
            self.error.set("")

    async def __show_listbox(self):
        self.text.pack(anchor="w")
        self.text.config(state=NORMAL)
        self.text.delete("1.0",END)
        try:
            self.text.insert(END,self.generated_content,"\n")
            self.text.config(state=DISABLED)
        except AttributeError:
            self.error.set("Вы ещё не ввели запрос")

    def __labels(self):
        Label(self.root,text="Вариант",font=self.font).pack(anchor="n")
        self.variant = IntVar() or 0
        Entry(self.root,textvariable=self.variant,font=self.font).pack(ipady=5)
        Label(self.root,text="Запрос",font=self.font).pack(anchor="n")
        self.prompt = StringVar()
        Entry(self.root,textvariable=self.prompt,width=100,font=self.font).pack(ipady=10)
        Button(self.root,text="Подтвердить",command=self._confirm_button,foreground="white",background="green",font=self.font).pack(anchor="n")
        self.success = StringVar(self.root,"")
        Label(self.root,textvariable=self.success,foreground="green",font=self.font).pack(anchor="n")
        self.error = StringVar(self.root,"")
        Label(self.root,textvariable=self.error,foreground="red",font=self.font).pack(anchor="n")
        Button(self.root,text="Показать ответ",foreground="white",background="green",font=self.font,command=lambda:asyncio.run(self.__show_listbox())).pack(anchor="n")
        Button(self.root,text="Скрыть",foreground="white",background="red",font=self.font,command=lambda:self.text.pack_forget()).pack(anchor="n")
        self.text = Text(self.root,height=50,font=self.font,wrap=WORD)


        self.root.mainloop()

class Gemini:
    def __init__(self):
        self.__api_key = os.getenv("API_KEY")
        self.client = genai.Client(
            api_key=self.__api_key
        )



tkinter = Tkinter("800x700","exam")


