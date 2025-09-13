import pymssql
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

a = 0
b = 0
c = 0
left = 0
right = 0
com_level = ['高','中','低','非常低']
# 定义年份范围
year_ranges = ("1980-1990", "1990-2000", "2000-2010", "2010-2020")

def get_level(level):
    match level:
        case '高':
            return 3
        case '中':
            return 2
        case '低':
            return 1
        case '非常低':
            return -1

def get_games():
    # 获取当前选中的类型和平台
    selected_Genre = combo_var_Genre.get()
    selected_Platform = combo_var_Platform.get()
    selected_Gsales = combo_var_Gsales.get()
    selected_Cscore = combo_var_Cscore.get()
    selected_Uscore = combo_var_Uscore.get()
    a = get_level(selected_Gsales)
    b = get_level(selected_Cscore)
    c = get_level(selected_Uscore)
    # 获取选中的年份范围，并分割为两个年份
    selected_year_range = combo_var_year.get()
    year_start, year_end = map(int, selected_year_range.split('-'))


    # 查询数据库中符合条件的所有游戏
    cursor.execute(f"select DISTINCT name, Platform, Year_of_Release, Genre, Publisher, Global_Sales, Critic_Score, User_Score, %d*Global_Sales + %d*Critic_Score/10 + %d*User_Score as Score from vgsales WHERE [Genre] = '{selected_Genre}' AND [Platform] = '{selected_Platform}' and Year_of_Release between {year_start} and {year_end} and Critic_Score is not null ORDER BY Score DESC"% (a, b, c))
    games = cursor.fetchall()


    # 创建一个新的窗口
    new_window = tk.Toplevel(root)
    new_window.title("推荐的游戏")

    #获取屏幕尺寸，使窗口位于屏幕中央
    screenWidth = new_window.winfo_screenwidth()
    screenHeight = new_window.winfo_screenheight()
    wdWidth = int(screenWidth * 0.8)
    wdHeigh = int(screenHeight * 0.8)
    new_window.geometry('%dx%d+%d+%d' % (wdWidth, wdHeigh, (screenWidth - wdWidth) / 2, (screenHeight - wdHeigh) / 2))

    tree = ttk.Treeview(new_window, columns=('name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Global_Sales', 'Critic_Score', 'User_Score'), show='headings')
    tree.column('name', width=100, anchor='center')
    tree.column('Platform', width=100, anchor='center')
    tree.column('Year_of_Release', width=100, anchor='center')
    tree.column('Genre', width=100, anchor='center')
    tree.column('Publisher', width=100, anchor='center')
    tree.column('Global_Sales', width=100, anchor='center')
    tree.column('Critic_Score', width=100, anchor='center')
    tree.column('User_Score', width=100, anchor='center')

    tree.heading('name', text='游戏名')
    tree.heading('Platform', text='平台')
    tree.heading('Year_of_Release', text='发售时间')
    tree.heading('Genre', text='游戏类型')
    tree.heading('Publisher', text='出版商')
    tree.heading('Global_Sales', text='全球销售量')
    tree.heading('Critic_Score', text='专家评价')
    tree.heading('User_Score', text='用户评价')

    for row in games:
        tree.insert('', 'end', values=(row['name'], row['Platform'], row['Year_of_Release'], row['Genre'], row['Publisher'], row['Global_Sales'], row['Critic_Score'], row['User_Score']))

    tree.pack(fill='both', expand=True)
    new_window.mainloop()

server = 'yzzzzy'
username = 'sa'
password = '123456'
database = 'steamtest'

try:
    db = pymssql.connect(server, username, password, database)
    print("Connected to the database!")
except pymssql.Error as e:
    print(f"Error: Unable to connect to the database. {e}")

cursor = db.cursor(as_dict=True)

cursor.execute("SELECT DISTINCT [Genre] FROM [steamtest].[dbo].[vgsales]")
results_Genre = cursor.fetchall()
game_Genre = tuple(result['Genre'] for result in results_Genre)

cursor.execute("select distinct [Platform] from [steamtest].[dbo].[vgsales]")
results_Platform = cursor.fetchall()
game_Plotform = tuple(result['Platform'] for result in results_Platform)


root = tk.Tk()
root.title("游戏推荐系统")
root.geometry("1100x700")
# 设置窗口背景为黑色
root.configure(bg="black")

# 加载图片
image1 = Image.open("steam.png")
image2 = Image.open("nitendo.png")
image3 = Image.open("playstation.jpg")
photo1 = ImageTk.PhotoImage(image1)
photo2 = ImageTk.PhotoImage(image2)
photo3 = ImageTk.PhotoImage(image3)

# 显示图片1
label1 = tk.Label(root, image=photo1, bg="black")
label1.image = photo1  # 保持对图片对象的引用
label1.place(x=100,y=180)

# 显示图片2
label2 = tk.Label(root, image=photo2, bg="black")
label2.image = photo2  # 保持对图片对象的引用
label2.place(x=400,y=150)

# 显示图片3
label3 = tk.Label(root, image=photo3, bg="black")
label3.image = photo3  # 保持对图片对象的引用
label3.place(x=800,y=150)

label_text = tk.Label(root, text="欢迎使用游戏推荐系统", bg="black", fg="white", font=("Arial", 15))
label_text.place(x=450,y=80)
label_choice1 = tk.Label(root,text="游戏平台",bg="black", fg="white", font=("Arial", 10))
label_choice1.place(x=100,y=380)
label_choice2 = tk.Label(root,text="游戏类型",bg="black", fg="white", font=("Arial", 10))
label_choice2.place(x=450,y=380)
label_choice3 = tk.Label(root,text="发布年份",bg="black", fg="white", font=("Arial", 10))
label_choice3.place(x=800,y=380)
label_choice4 = tk.Label(root,text="全球销量",bg="black", fg="white", font=("Arial", 10))
label_choice4.place(x=100,y=480)
label_choice5 = tk.Label(root,text="评论家分数",bg="black", fg="white", font=("Arial", 10))
label_choice5.place(x=450,y=480)
label_choice6 = tk.Label(root,text="玩家分数",bg="black", fg="white", font=("Arial", 10))
label_choice6.place(x=800,y=480)

combo_var_Genre = tk.StringVar()
combo_box_Genre = ttk.Combobox(root, textvariable=combo_var_Genre)
combo_box_Genre['values'] = game_Genre
combo_box_Genre.place(x=450,y=400)

combo_var_Platform = tk.StringVar()
combo_box_Platform = ttk.Combobox(root,textvariable=combo_var_Platform)
combo_box_Platform['values'] = game_Plotform
combo_box_Platform.place(x=100, y=400)

combo_var_year = tk.StringVar()
combo_box_year = ttk.Combobox(root, textvariable=combo_var_year)
combo_box_year['values'] = year_ranges
combo_box_year.place(x=800, y=400)

combo_var_Gsales = tk.StringVar()
combo_box_Gsales = ttk.Combobox(root,textvariable=combo_var_Gsales)
combo_box_Gsales['values'] = com_level
combo_box_Gsales.place(x=100,y=500)

combo_var_Cscore = tk.StringVar()
combo_box_Cscore = ttk.Combobox(root,textvariable=combo_var_Cscore)
combo_box_Cscore['values'] = com_level
combo_box_Cscore.place(x=450,y=500)

combo_var_Uscore = tk.StringVar()
combo_box_Uscore = ttk.Combobox(root,textvariable=combo_var_Uscore)
combo_box_Uscore['values'] = com_level
combo_box_Uscore.place(x=800,y=500)

button = tk.Button(root, text="获取推荐游戏", bg="white", command=get_games)  # 绑定事件处理函数
button.place(x=480, y=600)

root.mainloop()