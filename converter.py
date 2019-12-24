import cv2, numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Video Converter')
        self.frame = tk.Frame(self, width=600, height=300)
        self.frame.pack()
        
        self.param = [200, 200]
        self.param1, self.param2 = tk.Entry(self.frame), tk.Entry(self.frame)
        self.param1.insert(0, 200)
        self.param2.insert(0, 200)
        self.param1.place(x=150, y=10)
        self.param2.place(x=280, y=10)
        tk.Button(self.frame, text='set parameters', command=self.setParams, relief='ridge', width=15).place(x=10, y=10)
        tk.Button(self.frame, text='browse', command=self.getFile, relief='ridge', width=15).place(x=10, y=40)

    def setParams(self):
        params = self.param1.get(), self.param2.get()
        try:
            self.param = list(map(int, params))
            messagebox.showinfo('Success', 'Parameters changed successfully')
        except:
            messagebox.showerror('Error', 'Give integer parameters')
        

    def getFile(self, file=''):
        file = filedialog.askopenfilename(initialdir='/', title='select video file', filetypes=(('mp4 Files', '*.mp4'), ('mkv files', '*.mkv'), ('Other files', '*.*')))
        tk.Label(self.frame, text=file).place(x=150, y=40)
        if file != '':
            tk.Button(self.frame, text='Convert', command=lambda :self.convert(file), relief='ridge', width=15).place(x=10, y=70)
        else:
            messagebox.showwarning('Warning', 'Select the file to continue')

    def convert(self, fileName):
        opt=[]
        file = cv2.VideoCapture(fileName)
        self.width, self.height = int(file.get(cv2.CAP_PROP_FRAME_WIDTH)), int(file.get(cv2.CAP_PROP_FRAME_HEIGHT))
        i = 0
        frameCount = int(file.get(cv2.CAP_PROP_FRAME_COUNT))-5
        while True:
            frame = file.read()[1]
            canny = cv2.Canny(frame, self.param[0], self.param[1])
            rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
            opt.append(rgb)
            cv2.imshow('Wind', rgb)
            i+=1
            if cv2.waitKey(1)==27 or i == frameCount:
                cv2.destroyAllWindows()
                tk.Label(self.frame, text='Converted').place(x=150, y=70)
                self.save(opt, fps=file.get(cv2.CAP_PROP_FPS))
                break

    def save(self, opt, fps):
        loc = filedialog.asksaveasfilename(initialdir='/', title='select video file', filetypes=(('avi Files', '*.avi'), ('all Files', '*.*')))
        if loc !='':
            if loc[-4:] != '.avi':
                loc+='.avi'
            video = cv2.VideoWriter(loc, cv2.VideoWriter_fourcc(*'xvid'), fps, (self.width, self.height))
            for frame in opt:
                video.write(frame)
            video.release()
            messagebox.showinfo('Success', 'File is successfully saved')
        else:
            messagebox.showwarning('warning', 'To save the file please choose location')
            tk.Button(self.frame, text='Save', command=lambda :self.save(opt, fps), relief='ridge', width=15).place(x=10, y=100)
        
if __name__ == '__main__':
  win=Window()
