
import os
import sys
import time
import praw
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
import webbrowser
from sklearn.decomposition import PCA
tkFileDialog = tkinter.filedialog

#Abbreviate
m = __main__

# Create and hide the root window
root = Tkinter.Tk()
root.wm_title("REDDIT_SCRAPER")
root.withdraw()

def beta_pdf(x, a, b):
    return (x**(a-1) * (1-x)**(b-1) * math.gamma(a + b)
            / (math.gamma(a) * math.gamma(b)))

class UpdateDist:
    def __init__(self, ax, prob=0.5):
        self.success = 0
        self.prob = prob
        self.line, = ax.plot([], [], 'k-')
        self.x = np.linspace(0, 1, 200)
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)

        # This vertical line represents the theoretical value, to
        # which the plotted distribution should converge.
        self.ax.axvline(prob, linestyle='--', color='black')

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            self.success = 0
            self.line.set_data([], [])
            return self.line,

        # Choose success based on exceed a threshold with a uniform pick
        if np.random.rand(1,) < self.prob:
            self.success += 1
        y = beta_pdf(self.x, self.success + 1, (i - self.success) + 1)
        self.line.set_data(self.x, y)
        return self.line,

class gui_interface():

    def __init__(self):
        
        self.Access = 0
        
        self.gui_window = self._Create_GUI_Window()
        self.credentials = self.__Get_Credentials_File__()
        
        msg ="\n\nGetting a Reddit Instance. Please Wait . . . \n\n"

        m.textbox.delete(1.0, Tkinter.END)
        m.textbox.insert(1.0, msg )
        m.textbox.configure(fg='black')
        m.textbox.update()

        self.scraper = redditscraper(self.credentials, psaw=False)


        m.PTSButton['state'] = 'normal'
        m.PTDButton['state'] = 'normal'
        m.PAGButton['state'] = 'normal'
        m.GSTButton['state'] = 'normal'
        m.STButton['state'] = 'normal'

        m.textbox.delete(1.0, Tkinter.END)
        
        self.LDA = lda_infer(os.path.join('LDA','models','hash_vect.pk'),
                             os.path.join('LDA','models','lda_model_8.pk'))
        
    def get_topic_predict(self, texts):
        clean_text, pred = self.LDA.infer(texts)
        # print(pred)
        pred =  [np.where(r==r.max())[0][0] for r in pred]
        return clean_text, pred
    
    def __Get_Credentials_File__(self, credentials_file = 'Credentials.txt'):

        Valid_Keys = 0
        Access = 0

        time.sleep(3)

        m.textbox.delete(1.0, Tkinter.END)  
        
        while not os.path.isfile(credentials_file) or not Valid_Keys or not Access:

            self.credentials_dictionary = {}

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
               
               for Line in CF_Data.splitlines():
                  if not Line.strip():
                     continue

                  Key, Value = Line.split('=')

                  self.credentials_dictionary[Key.strip()] = Value.strip()

               cred = self.credentials_dictionary
               
               if os.path.isfile('Verified_Credentials.txt'):
                  
                  VCF = open(credentials_file, 'r')
                  VCF_Data = VCF.read()
                  VCF.close()

                  if VCF_Data == CF_Data:
                      
                      m.GCButton.place_forget()
                      m.PTSButton.place(x=550,y=561)
                      m.PAGButton.place(x=332,y=561)
                      m.STButton.place(x=550,y=10)
                      m.textbox.delete(1.0, Tkinter.END)
                      m.textbox.configure(fg='black')
                      m.textbox.update()
                      return self.credentials_dictionary
               
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
                  m.PAGButton.place(x=332,y=561)
                  m.textbox.delete(1.0, Tkinter.END)
                  m.textbox.configure(fg='black')
                  m.textbox.update()
               
               else:

                  credentials_file = ""

                  continue

               return self.credentials_dictionary

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

        Access = 0

        #Get Subreddit Pre-Check
        try:

            cred = self.credentials_dictionary

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

        if not Access:
            
            msg = '\nWeb Access Error.\n'
            msg += 'Please check your Sub_Reddit_Topic. --> '+ self.Topic +'\n'
            msg += 'Server could not understand request due to invalid syntax.'
            #msg += repr(Test_Request)
            
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
        
        #Attempt 1 Get Initial Request 
        self.Comments = self.scraper.Get_Reddit_Comments(self.Topic, 
                                    Limit=(self.Limit), 
                                    how='top',
                                    after='5y')

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
        d = sns.displot(pred, bins=8).set(title=f'Distribution of r/{self.Topic} topics\nn={len(pred)}')
        mids = [rect.get_x() + rect.get_width() / 2 for rect in d.ax.patches]
        plt.xticks(ticks =mids, labels= [1,2,3,4,5,6,7,8])
        plt.tight_layout()
        plt.show()

    def _Plot_TS(self):

        _, pred = self.get_topic_predict(list(self.Comments['body']))
        t = range(len(pred))
        sns.set_style('dark')
        t_mean = [_t for _t in range(0, max(t), 5)]
        p_mean = [int(np.mean(pred[i:i+5])+1) for i  in range(0, max(t), 5)]
        # ts = sns.scatterplot(t, [p+1 for p in pred])
        ts = sns.lineplot(x=t_mean, y=p_mean)
        plt.tight_layout()
        ts.set(ylim=(0,8))
        plt.axhline(y=int(np.mean(pred))+1,c='red', ls='--')
        plt.legend(['moving mean', 'group mean'])
        plt.show()
        # Create plot
        # ax.scatter(x_t_top[0], x_t_top[1], alpha=0.8, c="red", edgecolors='none', s=30, label="Topics")
        # ax.scatter(x_t_obs[0], x_t_obs[1], alpha=0.8, c="blue", edgecolors='none', s=30, label="Comments")
        #
        # plt.title('Topic Plotting with PCA (n_comp=2)')
        # plt.legend(loc=2)
        # plt.show()

        # Fixing random state for reproducibility
        # np.random.seed(19680801)
        #
        # fig, ax = plt.subplots()
        # ud = UpdateDist(ax, prob=0.7)
        # anim = FuncAnimation(fig, ud, frames=100, interval=100, blit=True)
        # plt.show()

    def _Plot_Animation(self):
        _, pred = self.LDA.infer(list(self.Comments['body']))
        topics = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],
                 [0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],
                 [0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]
        topics.extend(pred)
        X = np.array(topics)
        pca = PCA(n_components=2)
        X_transformed = pca.fit_transform(X)
        x_t_top = X_transformed[:8].T
        x_t_obs = X_transformed[8:].T

        markers = ['o', 'd', '+', 'v', '^', '<', '>', 's']
        counter = 0
        for i, m in zip(range(8), markers):
            plt.plot(x_t_top[0][i], x_t_top[1][i], m, label="Topic {}".format(counter+1))
            counter += 1

        plt.plot(x_t_obs[0], x_t_obs[1], 'x', color='yellow', label='Comments')

        plt.legend(numpoints=1)
        plt.xlim(-1, 1.8)
        plt.title("PCA Plot of Topics and Comments (n_dim=2)")
        plt.show()

    def _Show_Topics(self):
        webbrowser.open_new(os.path.join('LDA','results','ldavis_prepared_8.html'))

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

        GSTButton['state'] = 'disabled'

        text = 'PLOT TOPIC DISTRIBUTION'
        command = self._Plot_Dist

        PTDButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTDButton = PTDButton
        PTDButton.place(x=550,y=531)

        PTDButton['state'] = 'disabled'

        text = 'PLOT TIME-SERIES'
        command = self._Plot_TS

        PTSButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTSButton = PTSButton
        PTSButton.place(x=550,y=561)
        PTSButton.place_forget()

        PTSButton['state'] = 'disabled'

        text = 'PLOT TOPIC GRAPH'
        command = self._Plot_Animation

        PAGButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.PAGButton = PAGButton
        PAGButton.place(x=332,y=561)
        PAGButton.place_forget()

        PAGButton['state'] = 'disabled'

        text = 'SHOW TOPICS'
        command = self._Show_Topics

        STButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.STButton = STButton
        STButton.place(x=550,y=10)
        STButton.place_forget()

        STButton['state'] = 'disabled'
        
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




      
