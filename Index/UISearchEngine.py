from Tkinter import *
import webbrowser

class homepage:
    def __init__(self, master):
        self.master = master
        self.timer = 0
        self.query_true = None

        # self.frame = Frame(master)

        # self.frame.pack(fill=BOTH, expand=1)

        self.welcome = Label(master, text = "Welcome to Group 111's Search Engine")
        self.welcome.grid(row=0,column=1, sticky = N+S+W+E)
        # self.welcome.pack()

        self.image = PhotoImage(file=".\gif.gif") #GIF Len = 40 frames
        self.pic = Label(image=self.image)
        self.pic.grid(row=1, column=1, sticky = N+S+W+E)


        # self.pic.image = self.image
        # self.pic.pack(fill=BOTH, expand=1)

        self.query = Text(master, height = 1, width = 40)
        self.query.grid(row=2,column=1,sticky = N+S+W+E)
        self.query.insert(END,"Search here...")

        self.search_button = Button(text = "Search Now Bitch", command = self.click_search)
        self.search_button.grid(row=3, column=1, sticky = N+S+W+E)

        self.resultsLabel = Label(self.master)



    def click_search(self):
        input = self.query.get("1.0", END)
        input = input.split()
        if len(input) >= 2 :
            self.input  = input[0]+ " " +input[1]
        elif len(input) == 1:
            self.input = input[0]
        else:
            self.input = ""
        self.query_true = True
        self.update()



    def update(self):

        if self.query_true == True:
            self.resultsLabel.selection_clear()
            self.resultsLabel = Label(self.master, text="Results for " + self.input + ":")
            r=0
            
            for text in (r"http://www.google.com",r"http://www.google.com",r"http://www.google.com"):
                self.resultsLabel= Label(self.master,text=text,foreground="#0000ff")
                self.resultsLabel.bind("<1>",lambda event,text=text: self.click_link(event,text))
                self.resultsLabel.grid(row=4+r,column=1,sticky = W)
                r=r+1        

        self.master.update()


    def click_link(self, event, text):
        print(text)
        webbrowser.open_new(text)
        
        
if __name__ == "__main__":
    root = Tk()
    root.title("Group 111's Search Engine")
    hp = homepage(root)
    root.after(0,hp.update(),40)
    root.mainloop()
