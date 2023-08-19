import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


colors = {
    0: 'white',
    1: '#097EB9',
    2: '#10A831',
    3: '#D91616',
    4: '#AD0FCA',
    5: '#DCD921',
    6: '#209D99',
    7: '#A93939',
    8: '#BBCF51'
}


class MyButton(tk.Button):
    def __init__(self, x, y, number=0, master=None, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Consolas 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mines = 0
        self.is_open = False

    def __repr__(self):
        return f'button {self.x}:{self.y} | {self.number} | {self.is_mine} '


class MineSweeper:
    window = tk.Tk()
    row = 7
    col = 10
    mines = 10
    is_game_over = False
    is_first_click = True

    def __init__(self):
        self.buttons = []
        self.opened_non_mine_buttons = 0
        for i in range(MineSweeper.row + 2):
            temp = []
            for j in range(MineSweeper.col + 2):
                btn = MyButton(x=i, y=j, master=MineSweeper.window)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        # print(clicked_button)
        if MineSweeper.is_game_over:
            return

        if not clicked_button.is_mine:
            self.opened_non_mine_buttons += 1

        if self.opened_non_mine_buttons == (MineSweeper.row * MineSweeper.col) - MineSweeper.mines:
            showinfo('Winner', 'Congratulations, You Win!')
            MineSweeper.is_game_over = True

        if MineSweeper.is_first_click:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_ceils()
            self.print_buttons()
            MineSweeper.is_first_click = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.is_game_over = True
            showinfo('Game over', 'You lose!')
            for i in range(1, MineSweeper.row):
                for j in range(1, MineSweeper.col):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_mines, 'black')
            if clicked_button.count_mines:
                clicked_button.config(text=clicked_button.count_mines, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_mines, 'black')
            if cur_btn.count_mines:
                cur_btn.config(text=cur_btn.count_mines, disabledforeground=color)
            else:
                cur_btn.config(text=' ', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mines == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #    continue
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.row\
                                and 1 <= next_btn.y <= MineSweeper.col and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.is_first_click = True
        MineSweeper.is_game_over = False

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)

        win_settings.wm_title('Settings')

        row_entry = tk.Entry(win_settings)
        tk.Label(win_settings, text='Num of rows').grid(row=0, column=0)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, MineSweeper.row)

        col_entry = tk.Entry(win_settings)
        tk.Label(win_settings, text='Num of columns').grid(row=1, column=0)
        col_entry.grid(row=1, column=1, padx=20, pady=20)
        col_entry.insert(0, MineSweeper.col)

        mine_entry = tk.Entry(win_settings)
        tk.Label(win_settings, text='Num of mines').grid(row=2, column=0)
        mine_entry.grid(row=2, column=1, padx=20, pady=20)
        mine_entry.insert(0, MineSweeper.mines)

        save_btn = tk.Button(win_settings, text='Confirm', command=lambda: self.change_settings(row_entry, col_entry, mine_entry))
        save_btn.grid(row=3, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, col: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(col.get()), int(mines.get())
        except ValueError:
            showerror('ERROR!', 'you entered the wrong value')
            return

        MineSweeper.row = int(row.get())
        MineSweeper.col = int(col.get())
        MineSweeper.mines = int(mines.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        setings_menu = tk.Menu(menubar, tearoff=0)
        setings_menu.add_command(label='Play', command=self.reload)
        setings_menu.add_command(label='Settings', command=self.create_settings_win)
        setings_menu.add_command(label='Close', command=self.window.destroy)
        menubar.add_cascade(label='File', menu=setings_menu)

        count = 1
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.col + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, MineSweeper.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, MineSweeper.col + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.row + 2):
            for j in range(MineSweeper.col + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_mines in colors:
                    color = colors.get(btn.count_mines, 'black')
                    btn.config(text=btn.count_mines, fg=color)

    def start(self):
        self.create_widgets()
        # self.open_all_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.col + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("M", end=' ')
                else:
                    print(btn.count_mines, end=' ')
            print()

    def insert_mines(self, number: int):
        indexes = self.get_mines_places(number)
        print(indexes)
        # count = 1
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.col + 1):
                btn = self.buttons[i][j]
                # btn.number = count
                if btn.number in indexes:
                    btn.is_mine = True
                # count += 1

    def count_mines_in_ceils(self):
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.col + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_mines = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.row * MineSweeper.col + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.mines]


game = MineSweeper()
game.start()