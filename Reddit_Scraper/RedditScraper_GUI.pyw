import re
import os
import sys
import praw
import string
import idlelib
import __main__
import traceback
import subprocess
import pandas as pd
import datetime as dt
import tkinter.filedialog
import tkinter as Tkinter
tkFileDialog = tkinter.filedialog

#Abbreviate
m = __main__

class redditscraper():

    def __init__(self):
        self.gui_window = self._Create_GUI_Window()
        self.credentials = self.__Get_Credentials_File__()
        self.Access = 0
        
    def __Get_Credentials_File__(self, credentials_file = 'Credentials.txt'):

        txt_file_path = credentials_file

        #Create window for the TXT File Selection
        root = Tkinter.Tk()
        root.withdraw()
        
        if not os.path.isfile(credentials_file):
            
            # Where Am I File & Path
            file_path = sys._getframe().f_code.co_filename

            # This Directory
            Dir = os.path.dirname(file_path)

            #Abbreviate
            Select_File = tkFileDialog.askopenfilename

            T = "Select File Path to Credentials.txt"
            F = (("TXT files","*.txt"),("all files","*.*"))
            TF = Select_File(initialdir = Dir, title = T, filetypes = F)
        
            credentials_file = TF

            if 'Credentials.txt' != os.path.basename(credentials_file) or not credentials_file:

                m.CButton.place(x=25,y=531)
                m.CButton.update
            
                msg = "Invalid or Missing Credentials.\n\nPlease update or locate "
                msg += "the Credentials.txt file before using this this API.\n"
                m.textbox.delete(1.0, Tkinter.END)
                m.textbox.insert(1.0, msg )
                m.textbox.configure(fg='red')
                m.textbox.update()

                return
                
        CF = open(credentials_file, 'r')
        CF_Data = CF.read()
        CF.close()

        credentials_dictionary = {}
        
        for Line in CF_Data.splitlines():
            if not Line.strip():
                continue

            Key, Value = Line.split('=')

            credentials_dictionary[Key.strip()] = Value.strip()

        self.credentials = credentials_dictionary

        # Test credentials
        Test = self.Get_Reddit_Comments('Politics', 1)

        if self.Access:
            
            m.CButton.place_forget()

            m.textbox.delete(1.0, Tkinter.END)
            m.textbox.configure(fg='black')
            m.textbox.update()

        else:

            m.CButton.place(x=25,y=531)
            m.CButton.update
            
            msg = "Invalid or Missing Credentials.\n\nPlease update or locate "
            msg += "the Credentials.txt file before using this this API.\n\n"
            msg += Test
            
            m.textbox.delete(1.0, Tkinter.END)
            m.textbox.insert(1.0, msg )
            m.textbox.configure(fg='red')
            m.textbox.update()

            return

        return credentials_dictionary

    def __get_date__(self, created):
        return dt.datetime.fromtimestamp(created)

    def Get_Reddit_Comments(self, Sub_Reddit_Topic, Limit):

        self.Access = 0

        YOUR_APP_NAME                = self.credentials['YOUR_APP_NAME']
        PERSONAL_USE_SCRIPT_14_CHARS = self.credentials['PERSONAL_USE_SCRIPT_14_CHARS']
        SECRET_KEY_27_CHARS          = self.credentials['SECRET_KEY_27_CHARS']
        YOUR_REDDIT_USER_NAME        = self.credentials['YOUR_REDDIT_USER_NAME']
        YOUR_REDDIT_LOGIN_PASSWORD   = self.credentials['YOUR_REDDIT_LOGIN_PASSWORD']

        try:

            # Getting a Reddit instance
            Reddit = praw.Reddit(client_id=PERSONAL_USE_SCRIPT_14_CHARS,
                            client_secret=SECRET_KEY_27_CHARS,
                            user_agent=YOUR_APP_NAME, 
                            username=YOUR_REDDIT_USER_NAME, 
                            password=YOUR_REDDIT_LOGIN_PASSWORD)

            # Getting a Sub Reddit instance
            subreddit = Reddit.subreddit(Sub_Reddit_Topic)

            # Let’s just grab the most up-voted topics all-time with:
            # be aware that Reddit’s request limit* is 1000
            top_subreddit = subreddit.top(limit=Limit)

            topics_dict = { "title":[], 
                        "score":[], 
                        "id":[], "url":[], 
                        "comms_num": [], 
                        "created": [], 
                        "body":[]}

            for submission in top_subreddit:
                topics_dict["title"].append(submission.title)
                topics_dict["score"].append(submission.score)
                topics_dict["id"].append(submission.id)
                topics_dict["url"].append(submission.url)
                topics_dict["comms_num"].append(submission.num_comments)
                topics_dict["created"].append(submission.created)
                topics_dict["body"].append(submission.selftext)
        
            topics_data = pd.DataFrame(topics_dict)
        
            _timestamp = topics_data["created"].apply(self.__get_date__)
        
            topics_data = topics_data.assign(timestamp = _timestamp)
        
            # topics_data.to_csv('Sub_Reddit_Topics.csv', index=False)

            self.Access = 1

            return topics_data
        
        except Exception as e:

            print(e)

            error = 'invalid_grant error processing request'

            if error in "".join(traceback.format_exception(*sys.exc_info())):
                return error

            if "401" in str(e):

                return '\nWeb Access Error. received 401 HTTP response.\n'

            if "400" in str(e) or "403" in str(e)or "404" in str(e):

                 return str(e)
    
    def _GET_TOPIC(self, e=""):

        self.Access = 0

        Topic = m.TBox.get().strip()
        Limit = m.LBox.get().strip()

        if not Limit or not Limit.isdigit() :

            m.LBox.delete(0, Tkinter.END)
            m.LBox.insert(0, "5")
            m.LBox.configure(fg='black')
            m.LBox.update()
            Limit = 5

        Limit = int(Limit)

        if "Type Sub Reddit Topic Here" in Topic or not Topic:

            if not Topic:
                
                msg = "No Sub Reddit Topic Found in the Entry Box Below"
                m.textbox.delete(1.0, Tkinter.END)
                m.textbox.insert(Tkinter.END, msg)
                
            return

        #Get Subreddit Pre-Check
        Test_Request = self.Get_Reddit_Comments(Topic, 1)
        
        if not self.Access:
            
            msg = '\nWeb Access Error.\n'
            msg += 'Please check your Sub_Reddit_Topic. --> '+ Topic +'\n'
            msg += 'Server could not understand request due to invalid syntax.'
            msg += repr(Test_Request)
            
            m.textbox.delete(1.0, Tkinter.END)
            m.textbox.insert(1.0, msg )
            m.textbox.configure(fg='red')
            m.textbox.update()
            return

        m.textbox.configure(fg='black')
        m.textbox.delete(1.0, Tkinter.END)

        msg ="\n\nGetting Reddit_Comments. Please Wait . . . \n\n"

        m.textbox.insert(Tkinter.END, msg)
        m.textbox.update()
         
        Comments = self.Get_Reddit_Comments(Topic, Limit)

        m.textbox.delete(1.0, Tkinter.END)

        for title in range(0,Limit):
           m.textbox.insert(Tkinter.END, str(title + 1) + ':  ' )
           m.textbox.insert(Tkinter.END, Comments['title'][title][:75] + ' . . . . . ')
           m.textbox.insert(Tkinter.END, '\n')
           m.textbox.update()

    def _Get_Credentials(self):

        self.__Get_Credentials_File__("")

    def _Plot_Graphs(self):

        msg = 'Update code for the   < _Plot_Graphs  >  Method'

        m.textbox.delete(1.0, Tkinter.END)
        m.textbox.insert(1.0, msg )
        m.textbox.update()

    def _check_tbox_focus(self):

        Topic = m.TBox.get().strip()
        Limit = m.LBox.get().strip()
        
        if "LIMIT" not in Limit and "Type Sub Reddit Topic Here"  not in Topic:
            
            return

        if  'canvas.!entry2>' in repr(m.window.focus_get()):

            if "LIMIT" in m.LBox.get().strip():

                m.LBox.delete(0, Tkinter.END)
                m.LBox.configure(fg='black')

        elif  'canvas.!entry>' in repr(m.window.focus_get()):

            if "Type Sub Reddit Topic Here" in m.TBox.get().strip():

                m.TBox.delete(0, Tkinter.END)
                m.TBox.configure(fg='black')

        elif  'canvas.!button>' in repr(m.window.focus_get()):

            if "Type Sub Reddit Topic Here" in m.TBox.get().strip():

                m.TBox.configure(fg='grey')

            if "LIMIT" in m.LBox.get().strip():

                m.LBox.configure(fg='grey')
                
        m.window.after(500, self._check_tbox_focus)

    def _ButtonPress(self, e=""):

        m.TButton.focus_set()
        m.TButton.update()

    def _ButtonRelease(self, e=""):

        m.TButton.focus_set()
        m.TButton.update()

    def _Create_GUI_Window(self):
    
        # Create and hide the root window
        root = Tkinter.Tk()
        root.wm_title("REDDIT_SCRAPER")
        root.withdraw()

        window = Tkinter.Toplevel()

        window.configure(background = 'black')
        window.attributes('-topmost', False)
        window.state('zoomed')
        window.resizable(1,1)
    
        window.state('normal')

        width = 800
        height = 600
    
        window.maxsize(width, height)
        window.minsize(width, height)

        canvas = Tkinter.Canvas(window, highlightthickness=0)
        canvas.configure(background = 'white')
        canvas.pack(fill=Tkinter.BOTH, expand=1)
        canvas.update()

        # Create a Grdient Background
        for row in range(0,height)[::-1]:
            r = int(row / (height - 1)*0)
            g = int(row / (height - 1)*0)
            b = int(row / (height - 1)*125)

            canvas.create_line(0,row,width,row, fill = "#%02x%02x%02x" % (r, g, b) )

        canvas2 = Tkinter.Canvas(window, highlightthickness=0)
        canvas2.configure(background = 'white')
        canvas2.place(x=25, y=50)
        canvas2.update()

        textbox = Tkinter.Text(canvas2, relief=Tkinter.RAISED)
        textbox.insert(Tkinter.END, "Type a Sub Reddit Topic in the Entry Box Below.\n")
        textbox.configure(font=("Arial",12))

        textbox.place(x=20, y=50)
        textbox['width'] = 80
        textbox['height'] = 26
        textbox['bg'] =   'white'#'#008800'
        textbox['bd'] = 2
        textbox.update()
    
        scrollbar = Tkinter.Scrollbar(canvas2, orient=Tkinter.VERTICAL, command = textbox.yview )
        textbox['yscroll'] = scrollbar.set
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y) #, expand=1)
        textbox.pack(fill=Tkinter.BOTH, expand=Tkinter.Y)

        m.textbox = textbox

        TBox = Tkinter.Entry(canvas, bg='white', width=27)
        __main__.TBox = TBox
        TBox.place(x=79,y=532)
        TBox.configure(font=("Arial",13), fg='light grey')
        TBox.delete(0, Tkinter.END)
        TBox.insert(Tkinter.END, "  Type Sub Reddit Topic Here")

        m.TBox = TBox

        LBox = Tkinter.Entry(canvas, bg='white', width=5)
        __main__.LBox = LBox
        LBox.place(x=25,y=532)
        LBox.configure(font=("Arial",13), fg='light grey')
        LBox.delete(0, Tkinter.END)
        LBox.insert(0, "LIMIT")
        
        m.LBox = LBox

        text = 'GET  SUBREDDIT  TOPIC'
        command = self._GET_TOPIC

        TButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.TButton = TButton
        TButton.place(x=332,y=531)
        
        TButton.bind('<ButtonPress-1>',self._ButtonPress)
        TButton.bind('<ButtonRelease-1>',self._ButtonRelease)

        text = 'PLOT MATPLOTLIB GRAPHS'
        command = self._Plot_Graphs

        PButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PButton = PButton
        PButton.place(x=550,y=531)

        text = 'GET REDDIT CREDENTIALS'
        command = self._Get_Credentials

        CButton = Tkinter.Button(canvas, width=105, text=text, command=command)
        __main__.CButton = CButton
        CButton.place(x=25,y=531)
        
        window.update()
        m.window = window
        self._check_tbox_focus()
    
#----------------------------------------------------------------

if __name__ == '__main__':

    app = redditscraper()
    window.mainloop()




      
