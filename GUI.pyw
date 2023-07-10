
import os
import sys
import time
import tkinter as Tkinter
import tkinter.filedialog
import webbrowser

import __main__
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import praw
import seaborn as sns
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from sklearn.decomposition import PCA

from lda.lda_infer import ldaInfer
from redditscraper.redditscraper import redditScraper

tkFileDialog = tkinter.filedialog
from aws_poster.aws_post import getTopicAPI

#Abbreviate
m = __main__

# Create and hide the root window
root = Tkinter.Tk()
root.wm_title("REDDIT_SCRAPER")
root.withdraw()

class guiInterface():

    def __init__(self, n_topics=8):
        
        self.Access = 0
        self.n_topics = n_topics
        
        self.gui_window = self._Create_GUI_Window()
        self.credentials = self.__get_credentials_file__()
        
        msg ="\n\nGetting a Reddit Instance. Please Wait . . . \n\n"

        m.textbox.delete(1.0, Tkinter.END)
        m.textbox.insert(1.0, msg )
        m.textbox.configure(fg='black')
        m.textbox.update()

        self.scraper = redditScraper(self.credentials, psaw=False)

        self.get_topics = getTopicAPI()


        m.PTSButton['state'] = 'normal'
        m.PTDButton['state'] = 'normal'
        m.PAGButton['state'] = 'normal'
        m.GSTButton['state'] = 'normal'
        m.STButton['state'] = 'normal'

        m.textbox.delete(1.0, Tkinter.END)
        
        self.LDA = ldaInfer(os.path.join('LDA','models','hash_vect.pk'),
                             os.path.join('LDA','models',f'lda_model_{self.n_topics}.pk'))
        
    def __get_topic_predict__(self, texts):
        clean_text, pred = self.LDA.infer(texts)
        # print(pred)
        pred =  [np.where(r==r.max())[0][0] for r in pred]
        return clean_text, pred
    
    def __get_credentials_file__(self, credentials_file = 'Credentials.txt'):

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

    def _get_topic__(self, e=""):

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
                _, pred = self.__get_topic_predict__([title])
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
            
    def __get_credentials__(self):

        return self.__get_credentials_file__()

    def __plot_dist__(self):

        _, pred = self.__get_topic_predict__(list(self.Comments['body']))
        t = range(len(pred))
        sns.set_style('dark')
        d = sns.displot(pred, bins=self.n_topics).set(title=f'Distribution of r/{self.Topic}\nn={len(pred)}')
        mids = [rect.get_x() + rect.get_width() / 2 for rect in d.ax.patches]
        plt.xticks(ticks =mids, labels= list(range(1, self.n_topics+1)))
        plt.tight_layout()
        plt.show()

    def __plot_tse__(self):

        _, pred = self.__get_topic_predict__(list(self.Comments['body']))
        t = range(len(pred))
        sns.set_style('darkgrid')
        t_mean = [_t for _t in range(0, max(t), 5)]
        p_mean = [int(np.mean(pred[i:i+5])+1) for i  in range(0, max(t), 5)]
        # ts = sns.scatterplot(t, [p+1 for p in pred])
        ts = sns.lineplot(x=t_mean, y=p_mean)
        plt.tight_layout()
        ts.set(ylim=(0,self.n_topics))
        plt.axhline(y=int(np.mean(pred))+1,c='red', ls='--')
        plt.legend(['moving mean', 'group mean'])
        plt.title("Topic Drift Over Time")
        plt.tight_layout()
        plt.show()

    def __plot__animation__(self):
 
        class UpdateDist():
            def __init__(self, ax, pred, n_topics):

                sns.set_style('darkgrid')

                z_list = [0]*n_topics
                topics = [z_list.copy() for i in range(n_topics)]
                for i in range(n_topics):
                    topics[i][i] = 1
                # topics = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],
                #           [0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],
                #           [0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]


                topics.extend(pred)
                X = np.array(topics)
                
                self.pca = PCA(n_components=2)
                x_t_top = self.pca.fit_transform(X[:n_topics]).T
                self.x_t_obs = self.pca.transform(X[n_topics:]).T

                # markers = ['o', 'd', '+', 'v', '^', '<', '>', 's']
                # counter = 0
                patches = []
                x = x_t_top[0][:]
                y= x_t_top[1][:]
                for i in range(n_topics):
                    circle =  mpatches.Circle((x[i], y[i]), 0.08, ec="none")
                    ax.annotate(str(i), 
                                xy=(x[i], y[i]),
                                ha="center", va='center')
                    patches.append(circle)
                collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
                ax.add_collection(collection)

                self.scatter,  = ax.plot([], [],
                                        marker='o',
                                        ls='',
                                        color='black',
                                        label='Comments')
                
                
                
                pad = 0.1
                midx = (min(x)+max(x))/2
                midy = (min(y)+max(y))/2
                ax.axvline(midx, color='grey', alpha=0.5)
                ax.axhline(midy, color ='grey', alpha=0.5)
                ax.annotate('PC2', xy=(midx+.01, max(y)+0.05))
                ax.annotate('PC1', xy=(min(x)-.09, midy+.01))

                self.text = ax.text(min(x)-pad+.01,min(y)-pad+.01,'')
                self.ax = ax
                # Set up plot parameters
                self.ax.set_xlim(min(x)-pad, max(x)+pad)
                self.ax.set_ylim(min(y)-pad,max(y)+pad)

            def __call__(self, i):
                # This way the plot can continuously run and we just keep
                # watching new realizations of the process
                self.scatter.set_data(self.x_t_obs[0][:i],         
                                      self.x_t_obs[1][:i])
                self.text.set_text(f't={i}')
                
                return self.scatter, self.text, 

        # Fixing random state for reproducibility
        np.random.seed(19680801)

        _, pred = self.LDA.infer(list(self.Comments['body']))
        fig, ax = plt.subplots()
        sns.set_style('darkgrid')
        ud = UpdateDist(ax, pred, self.n_topics)
        anim = FuncAnimation(fig, ud, frames=len(pred), interval=100, blit=True)
        plt.title("PCA Plot of Topics and Comments")
        plt.show()

    def __show_topics__(self):
        webbrowser.open_new(os.path.join('LDA','results',f'ldavis_prepared_{self.n_topics}.html'))

    def _check_tbox_focus(self):

        Topic = m.TBox.get().strip()
        Limit = m.LBox.get().strip()
        
        if "LIMIT" not in Limit and "Type Sub Reddit Topic Here"  not in Topic:
            
            return

        if  'canvas.!entry>' in repr(m.window.focus_get()):

            if "LIMIT" in m.LBox.get().strip():

                m.LBox.delete(0, Tkinter.END)
                m.LBox.configure(fg='black')

        elif  'canvas.!entry2>' in repr(m.window.focus_get()):

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

        LBox = Tkinter.Entry(canvas, bg='white', width=5)
        __main__.LBox = LBox
        LBox.place(x=25,y=532)
        LBox.configure(font=("Arial",13), fg='light grey')
        LBox.delete(0, Tkinter.END)
        LBox.insert(0, "LIMIT")
        
        m.LBox = LBox

        TBox = Tkinter.Entry(canvas, bg='white', width=27)
        __main__.TBox = TBox
        TBox.place(x=79,y=532)
        TBox.configure(font=("Arial",13), fg='light grey')
        TBox.delete(0, Tkinter.END)
        TBox.insert(Tkinter.END, "  Type Sub Reddit Topic Here")

        m.TBox = TBox

        text = 'GET  SUBREDDIT  TOPIC'
        command = self._get_topic__

        GSTButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.GSTButton = GSTButton
        GSTButton.place(x=332,y=531)
        
        GSTButton.bind('<ButtonPress-1>',self._ButtonPress)
        GSTButton.bind('<ButtonRelease-1>',self._ButtonRelease)

        GSTButton['state'] = 'disabled'

        text = 'PLOT TOPIC DISTRIBUTION'
        command = self.__plot_dist__

        PTDButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTDButton = PTDButton
        PTDButton.place(x=550,y=531)

        PTDButton['state'] = 'disabled'

        text = 'PLOT TIME-SERIES'
        command = self.__plot_tse__

        PTSButton = Tkinter.Button(canvas, width=30, text=text, command=command)
        __main__.PTSButton = PTSButton
        PTSButton.place(x=550,y=561)
        PTSButton.place_forget()

        PTSButton['state'] = 'disabled'

        text = 'TOPIC PREDICTION PCA'
        command = self.__plot__animation__

        PAGButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.PAGButton = PAGButton
        PAGButton.place(x=332,y=561)
        PAGButton.place_forget()

        PAGButton['state'] = 'disabled'

        text = 'SHOW TOPICS'
        command = self.__show_topics__

        STButton = Tkinter.Button(canvas, width=29, text=text, command=command)
        __main__.STButton = STButton
        STButton.place(x=550,y=10)
        STButton.place_forget()

        STButton['state'] = 'disabled'
        
        text = 'GET REDDIT CREDENTIALS'
        command = self.__get_credentials__

        GCButton = Tkinter.Button(canvas, width=105, text=text, command=command)
        __main__.GCButton = GCButton
        GCButton.place(x=25,y=531)

        GCButton['state'] = 'disabled'
        
        m.window = window
        self._check_tbox_focus()
        window.update()
        
        

#----------------------------------------------------------------

if __name__ == '__main__':

    app = guiInterface(8)

    def on_closing():
        m.window.destroy()
        root.destroy()
    m.window.protocol("WM_DELETE_WINDOW", on_closing)
    m.window.mainloop()




      
