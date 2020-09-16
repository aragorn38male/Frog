import curses, time
import random

WIDTH = 100
HEIGHT = 46
MAX_X = WIDTH-2
MAX_Y = HEIGHT-2
SCORE=0
LIVES=3

class Car(object):

    def __init__(self, window, x, y , speed,dir, char=chr(64)):
        self.window = window
        self.x = x
        self.y = y
        self.char = char
        self.dir = dir
        self.speed = speed
        self.chrono=0

    def render(self):
        self.window.addstr(self.y, self.x ,  self.char)

    def move(self):
        self.chrono+=1
        if self.chrono==self.speed:
            self.chrono=0
            self.window.addstr(self.y, self.x, " ")
            if self.x < 1:
                self.dir=0
                self.x = 1
            if self.x > MAX_X:
                self.dir=1
                self.x = MAX_X
            if self.dir:    
                self.x -= 1
            else:
                self.x += 1

class Rail(object):

    def __init__(self,window, y ):
        self.window = window
        self.y = y

    def render(self):
        for _ in range(1,MAX_X+1):
            self.window.addstr(self.y, _ ,  "#")
            self.window.addstr(self.y+2, _ ,  "#")


class Frog(object):

    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y

    def render(self):
        self.window.addstr(self.y, self.x, "o")
        
    def reset(self):
        self.window.addstr(self.y, self.x, " ")

    def move_up(self):
        global SCORE
        self.y -= 1
        if self.y < 2:
            self.y = MAX_Y
            SCORE+=1

    def move_down(self):
        self.y += 1
        if self.y > MAX_Y:
            self.y = MAX_Y

    def move_left(self):
        self.x -= 1
        if self.x < 1:
            self.x = MAX_X

    def move_right(self):
        self.x += 1
        if self.x > MAX_X:
            self.x = 1


if __name__ == "__main__":
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    window = curses.newwin(HEIGHT, WIDTH , 0, 0)
    window.keypad(1)
    window.border(0)

    r=[]
    c=[]
    r_pos=[]
    for _ in range(2,42,2):
        if random.choice([1,1]):
            r_pos.append(_)
    #r_pos = [3, 8, 13, 20, 25, 31, 38] #Positions Rails non-calculées
    for _ in range(len(r_pos)):
        r.append(Rail(window, r_pos[_]))
    for _ in range(len(r)):
        speed = random.randint(3,20)
        dir = random.choice([0,1])
        for i in range(5):      #Nombre ennemi par rangée
            c.append(Car(window, random.randint(0,MAX_X), r_pos[_]+1, speed, dir))

    f = Frog(window, 50, 44)
  
    play=True

    while play:
        window.addstr(1, 2 ,  "Score: " + str(SCORE))
        window.addstr(1, 91 ,  "Vies: " + str(LIVES))
        window.refresh()
        window.timeout(0)
        f.render()
        for _ in range(len(r)):
            r[_].render()
            if f.y == r[_].y:
                window.addstr(f.y, f.x ,  "o")
                #window.refresh()
            if f.y == r[_].y+2:
                window.addstr(f.y, f.x ,  "o")
                #window.refresh()
        for _ in range(len(c)):
            c[_].render()
            c[_].move()
            if f.x == c[_].x and f.y == c[_].y:
                LIVES-=1
                f.x , f.y = 50 , 44
                if LIVES<1:
                    play=False
        
        event = window.getch()

        if event == 27:
            break
        elif event == 259:
            f.reset()
            f.move_up()
        elif event == 258:
            f.reset()
            f.move_down()
        elif event == 260:
            f.reset()
            f.move_left()
        elif event == 261:
            f.reset()
            f.move_right()
        else:
            pass
        
curses.endwin()