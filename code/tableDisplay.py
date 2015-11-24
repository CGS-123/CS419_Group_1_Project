import curses
from screenmanager import ScreenManager

class tableDisplay:
    @staticmethod
    def navigate(data, x, y, screen):
        if x == 0 and y == 0:
            ScreenManager.throw(screen, "Naviagte with arrow keys and press q to exit")

        screen.clear()
        screen.keypad(1)
        active = tableDisplay.organize(data, x, y, screen)
        dim = screen.getmaxyx()
        screen.addstr(0, 0, active[0], curses.A_BOLD)
        for i in range(dim[0]-1):
            try:
                screen.addstr(i+1, 0, active[i+1])
            except:
                pass
        screen.refresh()
        choice = screen.getch()
        if choice == curses.KEY_LEFT:
            if x != 0:
                return tableDisplay.navigate(data, x-1, y, screen)
            else:
                return tableDisplay.navigate(data, x, y, screen)
        if choice == curses.KEY_RIGHT:
            return tableDisplay.navigate(data, x+1, y, screen)
        if choice == curses.KEY_DOWN:
            return tableDisplay.navigate(data, x, y+1, screen)
        if choice == curses.KEY_UP:
            if y != 0:
                return tableDisplay.navigate(data, x, y-1, screen)
            else:
                return tableDisplay.navigate(data, x, y, screen)
        if choice == ord('q'):
            return
        else:
            return tableDisplay.navigate(data, x, y, screen)




    #x and y represent top left of screen relative to entire datatable
    @staticmethod
    def organize(data, x, y, screen):
        dim = (25, 80)
        active = list()
        max_array = list()
        for i in range(len(data[0])):
            max_array.append(len(str(data[0][i]).decode("utf-8")))
        for i in range(len(data[1])):
            for j in range(len(data[0])):
                max_array[j] = max(max_array[j], len(str(data[1][i][j])))

        header_string = ""
        for i in range(len(data[0])):
            num_spaces = max_array[i] + 1 - len(str(data[0][i]))
            header_string = header_string + str(data[0][i]) + "  "
            for k in range(num_spaces):
                header_string = header_string + " "

        active.append(header_string[x:(dim[1]+x)])

        string = ""
        for i in range(dim[0]):
            try:
                for j in range(len(data[0])):
                    string = string + str(data[1][i+y][j]) + "  "
                    num_spaces = max_array[j] + 1 - len(str(data[1][i+y][j]))
                    for k in range(num_spaces):
                        string = string + " "
                active.append(string[x:(dim[1]+x)])
                string = ""
            except:
                active.append("end of table...")
                break

        return active
