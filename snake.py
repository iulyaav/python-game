import pyglet
import random

MAX_WIDTH = 600
MAX_HEIGHT = 400

class Snake:

    def __init__(self):
        self.positions = [(0, 0)]
        self.size = 10
        self.direction = "UP"

    def body(self, x=0, y=0):
        points = ()
        for i in range(x, x + self.size):
            for j in range(y, y + self.size):
                points += ((i, j))
        return points
    
    def draw(self):
        for position in self.positions:
            print(position)
            points = self.body(x=position[0], y=position[1])
            pyglet.graphics.draw(self.size ** 2, pyglet.gl.GL_POINTS, ('v2i', points))
    
    def move_up(self):
        x, y = self.positions[-1]
        y += self.size
        if y in range(0, MAX_HEIGHT - self.size + 1):
            self.positions.pop(0)
            self.positions.append([x, y])

    def move_down(self):
        x, y = self.positions[-1]
        y -= self.size
        if y in range(0, MAX_HEIGHT - self.size + 1):
            self.positions.pop(0)
            self.positions.append([x, y])
    
    def move_left(self):
        x, y = self.positions[-1]
        x -= self.size
        if x in range(0, MAX_WIDTH - self.size + 1):
            self.positions.pop(0)
            self.positions.append([x, y])
    
    def move_right(self):
        x, y = self.positions[-1]
        x += self.size
        if x in range(0, MAX_WIDTH - self.size + 1):
            self.positions.pop(0)
            self.positions.append([x, y])

    
    def grow(self):
        grow_operation = {
            "UP": lambda x, y: (x, y+10),
            "DOWN": lambda x, y: (x, y-10),
            "LEFT": lambda x, y: (x-10, y),
            "RIGHT": lambda x, y: (x+10, y),
        }
        prev_x, prev_y = self.positions[-1]
        self.positions.append(grow_operation[self.direction](prev_x, prev_y))


class Food:

    def __init__(self):
        self.pos = []
        self.reposition()
        
    
    def draw(self):
        batch = pyglet.graphics.Batch()
        batch.add(
            8, 
            pyglet.gl.GL_LINES, 
            None, 
            ('v2i', (
                self.pos[0], self.pos[1], self.pos[0] + 10, self.pos[1], 
                self.pos[0] + 5, self.pos[1] - 5, self.pos[0] + 5, self.pos[1] + 5,
                self.pos[0], self.pos[1] + 5, self.pos[0] + 10, self.pos[1] - 5,
                self.pos[0], self.pos[1] - 5, self.pos[0] + 10, self.pos[1] + 5,
                )
            ),
        )
        batch.draw()
    
    def reposition(self):
        rand_x = random.randint(0, MAX_WIDTH)
        rand_y = random.randint(0, MAX_HEIGHT)
        self.pos = [rand_x - rand_x % 10, rand_y - rand_y % 10]

window = pyglet.window.Window(width=MAX_WIDTH, height=MAX_HEIGHT)
snake = Snake()
food = Food()


@window.event
def on_key_press(symbol, modifiers):
    movements = {
       pyglet.window.key.UP: snake.move_up,
       pyglet.window.key.DOWN: snake.move_down,
       pyglet.window.key.LEFT: snake.move_left,
       pyglet.window.key.RIGHT: snake.move_right, 
    }
    try:
        movements[symbol]()
        if snake.positions[-1] == food.pos:
            food.reposition()
            snake.grow()
            print("Gotcha!")

    except KeyError:
        print("No such movement")

    window.clear()
    snake.draw()

@window.event
def on_draw():
    window.clear()
    snake.draw()
    food.draw()

pyglet.app.run()