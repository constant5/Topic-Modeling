
import os
import sys
import math
import tkinter as Tkinter
import tkinter.filedialog
import traceback
import __main__
import pandas as pd
from Reddit_Scraper.RedditScraper import redditscraper
from LDA.LDA_Infer import lda_infer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import scipy.stats as ss
import time
import praw

tkFileDialog = tkinter.filedialog

#Abbreviate
m = __main__

# Create and hide the root window
root = Tkinter.Tk()
root.wm_title("REDDIT_SCRAPER")
root.withdraw()

class gui_interface():

    def __init__(self):
        
        self.Access = 0
        self.gui_window = self._Create_GUI_Window()
        self.credentials = self.__Get_Credentials_File__()
        self.scraper = redditscraper(self.credentials)

        self.LDA = lda_infer(os.path.join('LDA','models','hash_vect.pk'),
                             os.path.join('LDA','models','lda_model_8.pk'))

    def get_topic_predict(self, texts):
        clean_text, pred = self.LDA.infer(texts)
        # print(pred)
        pred =  [np.where(r==r.max())[0][0] for r in pred]
        return clean_text, pred
    
    def __Get_Credentials_File__(self, credentials_file = 'Credentials.txt'):

        credentials_file = os.path.join('Credentials.txt')

        Valid_Keys = 0
        Access = 0

        time.sleep(3)

        m.textbox.delete(1.0, Tkinter.END)  
        
        while not os.path.isfile(credentials_file) or not Valid_Keys or not Access:

            if not os.path.isfile(credentials_file):
               
               time.sleep(3)
            
               msg = "\nInvalid or Missing Credentials File in the local "
               msg += "directory.\n\nPlease locate or update ( ...\\\\"
               msg += "Credentials.txt ) file before using this API.\n"

               m.textbox.insert(Tkinter.END, msg )
               m.textbox.configure(fg='red')
               m.textbox.update()

               time.sleep(3)

               # Where Am I File & Path
               file_path = sys._getframe().f_code.co_filename

               # This Directory
               Dir = os.path.dirname(file_path)

               #Abbreviate
               Select_File = tkFileDialog.askopenfilename

               T = "Select File Path to Credentials.txt"
               F = (("TXT files","*.txt"),("all files","*.*"))
               cFile = Select_File(initialdir = Dir, title = T, filetypes = F)
        
               credentials_file = cFile

               if 'Credentials.txt' != os.path.basename(cFile) or not cFile:

                  credentials_file = ""

                  msg = "\nINVALID Credentials File Name.\n"
                  msg += cFile
                  
                  m.textbox.configure(fg='red')
                  m.textbox.insert(Tkinter.END, msg )
                  m.textbox.update()
                  
                  continue
            print(credentials_file)
            CF = open(credentials_file, 'r')
            CF_Data = CF.read()
            CF.close()
              
            Valid_Keys = min('YOUR_APP_NAME' in CF_Data,
            'PERSONAL_USE_SCRIPT_14_CHARS' in CF_Data,           
            'SECRET_KEY_27_CHARS' in CF_Data,
            'YOUR_REDDIT_USER_NAME' in CF_Data,
            'YOUR_REDDIT_LOGIN_PASSWORD' in CF_Data)
             
            if not Valid_Keys:
               
               credentials_file = ""
               
               msg = "\nINVALID Credentials File FORMAT.\n"
               
               m.textbox.configure(fg='red')
               m.textbox.insert(Tkinter.END, msg )
               m.textbox.update()
                  
               continue
               
            if not Access:
               
               m.textbox.delete(1.0, Tkinter.END)
        
               Msg = "Checking for a valid Credentials File. Please Wait . . .\n"
               
               m.textbox.insert(Tkinter.END, Msg )
               m.textbox.configure(fg='black')
               m.textbox.update()
               
               CF = open(credentials_file, 'r')
               CF_Data = CF.read()
               CF.close()

               credentials_dictionary = {}
        
               for Line in CF_Data.splitlines():
                  if not Line.strip():
                     continue

                  Key, Value = Line.split('=')

                  credentials_dictionary[Key.strip()] = Value.strip()

               cred = credentials_dictionary
               
               if os.path.isfile('Verified_Credentials.txt'):
                  
                  VCF = open(credentials_file, 'r')
                  VCF_Data = VCF.read()
                  VCF.close()

                  if VCF_Data == CF_Data:
                      
                      m.GCButton.place_forget()
                      m.PTSButton.place(x=550,y=561)
                      m.textbox.delete(1.0, Tkinter.END)
                      m.textbox.configure(fg='black')
                      m.textbox.update()
                      return credentials_dictionary
               
               # Test credentials
               try:

                  YOUR_APP_NAME                = cred['YOUR_APP_NAME']
                  PERSONAL_USE_SCRIPT_14_CHARS = cred['PERSONAL_USE_SCRIPT_14_CHARS']
                  SECRET_KEY_27_CHARS          = cred['SECRET_KEY_27_CHARS']
                  YOUR_REDDIT_USER_NAME        = cred['YOUR_REDDIT_USER_NAME']
                  YOUR_REDDIT_LOGIN_PASSWORD   = cred['YOUR_REDDIT_LOGIN_PASSWORD']

                  Reddit = praw.Reddit(client_id=PERSONAL_USE_SCRIPT_14_CHARS,
                                 client_secret=SECRET_KEY_27_CHARS,
                                 user_agent=YOUR_APP_NAME, 
                                 username=YOUR_REDDIT_USER_NAME, 
                                 password=YOUR_REDDIT_LOGIN_PASSWORD)

                  list(Reddit.subreddit('food').top(limit=1))

                  Access = 1

               except:
                  #print( "".join(traceback.format_exception(*sys.exc_info())) )
                  pass
                
               if Access:
            
                  CF = open(credentials_file, 'r')
                  CF_Data = CF.read()
                  CF.close()
                  
                  VCF = open('Verified_Credentials.txt', 'w')
                  VCF.write(CF_Data)
                  VCF.close()
                  
                  m.GCButton.place_forget()
                  m.PTSButton.place(x=550,y=561)
                  m.textbox.delete(1.0, Tkinter.END)
                  m.textbox.configure(fg='black')
                  m.textbox.update()
               
               else:

                  credentials_file = ""

                  continue

               return credentials_dictionary

    def _GET_TOPIC(self, e=""):

        self.Access = 0

        self.Topic = m.TBox.get().strip()
        self.Limit = m.LBox.get().strip()

        if not self.Limit or not self.Limit.isdigit() :

            m.LBox.delete(0, Tkinter.END)
            m.LBox.insert(0, "5")
            m.LBox.configure(fg='black')
            m.LBox.update()
            self.Limit = 5

        self.Limit = int(self.Limit)

        if "Type Sub Reddit Topic Here" in self.Topic or not self.Topic:
                
            msg = "No Sub Reddit Topic Found in the Entry Box Below"
            m.textbox.delete(1.0, Tkinter.END)
            m.textbox.insert(Tkinter.END, msg)
                
            return

        m.textbox.configure(fg='black')
        m.textbox.delete(1.0, Tkinter.END)

        msg ="\n\nGetting Reddit_Comments. Please Wait . . . \n\n"

        m.textbox.insert(Tkinter.END, msg)
        m.textbox.update()

        #Get Subreddit Pre-Check
        # Test_Request = self.scraper.Get_Reddit_Comments(Topic, 1)
        Test_Request = self.scraper.Get_Reddit_Comments(self.Topic, 1, 'top', after='3d')
        
        if not isinstance(Test_Request, pd.DataFrame):
            
            msg = '\nWeb Access Error.\n'
            msg += 'Please check your Sub_Reddit_Topic. --> '+ self.Topic +'\n'
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
         
        self.Comments = self.scraper.Get_Reddit_Comments(self.Topic, 
                                    Limit=self.Limit, 
                                    how='asc',
                                    after='5y')
        
        # print(Comments)

        m.textbox.delete(1.0, Tkinter.END)
        count = 1
        for title in self.Comments['body']:
            title = title.replace('\n', ' ')
            try:
                _, pred = self.get_topic_predict([title])
                m.textbox.insert(Tkinter.END, str(count) + ':  ' )
                m.textbox.insert(Tkinter.END, title[:75] + ' . . . . . ')
                m.textbox.insert(Tkinter.END, str(pred) + ' . ')
                m.textbox.insert(Tkinter.END, '\n')
                m.textbox.update()
                count += 1
            except:
                m.textbox.insert(Tkinter.END, str(count) + ':  ' )
                m.textbox.insert(Tkinter.END, title[:75] + ' . . . . . ')
                m.textbox.insert(Tkinter.END, '[n/a]' + ' . ')
                m.textbox.insert(Tkinter.END, '\n')
                m.textbox.update()
                count += 1
                pass
            

    def _Get_Credentials(self):

        return self.__Get_Credentials_File__()

    def _Plot_Dist(self):

        _, pred = self.get_topic_predict(list(self.Comments['body']))
        t = range(len(pred))
        sns.set_style('dark')
        d = sns.displot(data=pred, bins=8).set(title=f'Distribution of r/{self.Topic} topics\nn={len(pred)}')
        mids = [rect.get_x() + rect.get_width() / 2 for rect in d.ax.patches]
        plt.xticks(ticks =mids, labels= [1,2,3,4,5,6,7,8])
        plt.tight_layout()
        plt.show()

    def _Plot_TS(self):

        _, pred = self.get_topic_predict(list(self.Comments['body']))
        t = range(len(pred))
        sns.set_style('dark')
        ts = sns.scatterplot(x=t, y=[p+1 for p in pred])
        plt.tight_layout()
        plt.show()

    def _Plot_Ani(self):

        _, pred = self.get_topic_predict(list(self.Comments['body']))
        pred = [p+1 for p in pred]

            
        def norm_pdf(x, i):
            mu = np.mean(pred[:i])
            sigma = np.std(pred[:i])
            return ss.norm.pdf(x, mu, sigma)

        class UpdateDist:
            def __init__(self, ax):
                sns.set_style('darkgrid')
                self.line, = ax.plot([], [], 'k-')
                self.text = ax.text(0.1,.95,'')
                self.x = np.linspace(0, 9, 200)
                self.ax = ax
                self.freeze = []

                # Set up plot parameters
                self.ax.set_xlim(0, 10)
                self.ax.set_ylim(0, 1)
                self.ax.grid(True)

                # This vertical line represents the theoretical value, to
                # which the plotted distribution should converge.
                for i in range(10):
                    self.ax.axvline(i, linestyle='--', color='black')
        

            def __call__(self, i):
                # This way the plot can continuously run and we just keep
                # watching new realizations of the process
                y =  norm_pdf(self.x, i)
                self.line.set_data(self.x, y)
                self.text.set_text(f't={i}')

                if i%25==0:
                    self.freeze.append(self.ax.plot(self.x, y))


                return self.line, self.text, 

        fig, ax = plt.subplots()
        ud = UpdateDist(ax)
        anim = FuncAnimation(fig, ud, frames=len(pred), interval=100, blit=True)
        plt.show()


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

        m.GSTButton.focus_set()
        m.GSTButton.update()

    def _ButtonRelease(self, e=""):

        m.GSTButton.focus_set()
        m.GSTButton.update()

    def _Create_GUI_Window(self):
    
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
        
        canvas2 = Tkinter.Canvas(window, highlightthickness=0)
        canvas2.configure(background = 'white')
        canvas2.place(x=25, y=50)
        canvas2.update()

        Message = "Checking for a valid Credentials File. Please Wait . . .\n"

        textbox = Tkinter.Text(canvas2, relief=Tkinter.FLAT)
        #textbox.insert(Tkinter.END, "Type a Sub Reddit Topic in the Entry Box Below.\n")
        textbox.insert(Tkinter.END, Message)
        textbox.configure(font=("Arial",12))

        textbox.place(x=20, y=50)
        textbox['width'] = 80
        textbox['height'] = 26
        textbox['bg'] =   '#eaeaf2' # 'white'
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

        GSTButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.GSTButton = GSTButton
        GSTButton.place(x=332,y=531)
        
        GSTButton.bind('<ButtonPress-1>',self._ButtonPress)
        GSTButton.bind('<ButtonRelease-1>',self._ButtonRelease)

        text = 'PLOT TOPIC DISTRIBUTION'
        command = self._Plot_Dist

        PTDButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTDButton = PTDButton
        PTDButton.place(x=550,y=531)

        text = 'PLOT TIME-SERIES'
        command = self._Plot_TS

        PTSButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTSButton = PTSButton
        PTSButton.place(x=550,y=561)
        PTSButton.place_forget()
        
        text = 'GET REDDIT CREDENTIALS'
        command = self._Get_Credentials

        GCButton = Tkinter.Button(canvas, width=105, text=text, command=command)
        __main__.GCButton = GCButton
        GCButton.place(x=25,y=531)

        GCButton['state'] = 'disabled'
        
        m.window = window
        self._check_tbox_focus()
        window.update()
        
        

#----------------------------------------------------------------

if __name__ == '__main__':

    app = gui_interface()

    def on_closing():
        m.window.destroy()
        root.destroy()
    m.window.protocol("WM_DELETE_WINDOW", on_closing)
    m.window.mainloop()




      
