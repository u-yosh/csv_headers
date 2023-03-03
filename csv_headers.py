
'''
フォルダを選択すると、そのなかにあるCSVの先頭行を取得する
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import glob
import csv
import pandas as pd

class Application(ttk.Frame):
    def __init__(self, master, y=True, x=True):
        super().__init__(master)
        self.master.geometry("1200x500")
        self.dir = '~/'

        #初期パーツ
        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack()
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        self.label1 = tk.Label(self.entry_frame, text="指定行数")
        self.label1.pack(side = 'left')
        option = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.variable = tk.StringVar()
        self.combobox = ttk.Combobox(self.entry_frame,values=option, textvariable = self.variable, state='readonly')
        self.combobox.current(4)
        self.combobox.pack()

        self.edit_button = tk.Button(self.button_frame, text="フォルダ選択", command=lambda:self.on_get_csvfiles())
        self.edit_button.pack()
        self.clear_btn = tk.Button(self.button_frame, text="クリア", command=lambda:self.destroy_canvas_widget())

    def destroy_canvas_widget(self):
        try:
            self.master_frame.destroy()
            self.edit_button.pack()
            self.clear_btn.pack_forget()
        except AttributeError:
            print("non frame")

    def create_canvas(self):
        self.master_frame = tk.Frame(self.master)
        self.master_frame.pack()
        self.canvas = tk.Canvas(self.master_frame ,width=2000, height=1000)
        self.canvas.propagate(False)
        # Scrollbar を生成して配置
        self.ybar = ttk.Scrollbar(self.master_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.ybar.pack(side=tk.RIGHT, fill=tk.Y)

        #Canvas Widget を配置
        self.canvas.config(yscrollcommand=self.ybar.set)
        self.canvas.config(scrollregion=(0,0,1000,1000)) #スクロール範囲
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW, width=2000)

    #コールバック関数
    def on_get_csvfiles(self):
        self.create_canvas()
        file_path = self.filedialog_open()
        csv_list = self.get_csv_list(file_path)
        summary_of_extracted_heders_dict = self.get_csv_deaders(csv_list, int(self.variable.get()))
        dfs, keys = self.get_dataframelist_and_filenamelist(summary_of_extracted_heders_dict)
        for count,df in enumerate(dfs):
            self.create_tableview(df,keys,count)

        self.edit_button.pack_forget()
        self.clear_btn.pack()

    #表の生成
    def create_tableview(self,df,keys,count):
        _InFrame_=ttk.LabelFrame(self.frame,width=1200,height=250,text=keys[count],)
        #スクロールの範囲を修正
        _InFrame_.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        _TreeList_ = ttk.Treeview(_InFrame_,selectmode = 'none',show = "headings",height = 6,)
        tree_h_scroll=ttk.Scrollbar(_InFrame_,orient=tk.HORIZONTAL,command=_TreeList_.xview)
        tree_v_scroll=ttk.Scrollbar(_InFrame_,orient=tk.VERTICAL,command=_TreeList_.yview)

        #treeviewににスクロールをセット
        _TreeList_['xscrollcommand'] = tree_h_scroll.set
        _TreeList_['yscrollcommand'] = tree_v_scroll.set
        # ヘッダーを設定する
        _TreeList_['columns'] = list(df.columns)
        for col in df.columns:
            _TreeList_.column(col, width=100,stretch=False)
            _TreeList_.heading(col, text=col)

        # データを表示する
        for index, row in df.iterrows():
            values = list(row)
            _TreeList_.insert('', index, text=index, values=values)

        _InFrame_.grid(padx = 5, pady = 5, ipadx = 5, ipady = 5)
        # 1列目を可変サイズとする
        _InFrame_.columnconfigure(0, weight=1)
        # 1行目を可変サイズとする
        _InFrame_.rowconfigure(0, weight=1)
        # 内部のサイズに合わせたフレームサイズとしない
        _InFrame_.grid_propagate(False)
        _TreeList_.grid(row = 0,column = 0, sticky = tk.N+tk.S+tk.E+tk.W  )
        tree_h_scroll.grid(row = 1,column = 0,sticky = tk.EW )
        tree_v_scroll.grid(row = 0,column = 1,sticky = tk.NS )

    #フォルダを開くダイアログ
    def filedialog_open(self):
        fld = filedialog.askdirectory(initialdir = self.dir)
        return fld

    #パスからCSVを取得
    def get_csv_list(self,filepath):
        file_extention = "*.csv"
        csv_files = glob.glob(filepath + "/" + file_extention )
        return csv_files

    #先頭行を取得
    def get_csv_deaders(self,csv_list, head):
        dict = {}
        tmp_extracted_heders = []

        for csvfile in csv_list:
            with open(csvfile, 'r') as file:
                reader = csv.reader(file)
                for i ,row in enumerate(reader):
                    if i > head :
                        continue
                    tmp_extracted_heders.append(row)

                dict[csvfile] = tmp_extracted_heders
                tmp_extracted_heders = []
        return dict

    def get_dataframelist_and_filenamelist(self,dict):
        df_list = []
        key_list = []
        for key, value in dict.items():
            df = pd.DataFrame(value[1:], columns= value[0])
            key_list.append(key)
            df_list.append(df)
        return df_list,key_list



if __name__ == "__main__":
    root = tk.Tk()
    Application(root)

    root.mainloop()
