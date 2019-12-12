import pyglet
import random

MAX_WIDTH = 600
MAX_HEIGHT = 400
UNIT = 10

class Snake:

    def __init__(self):
        self.positions = [(0, 0)]
        self.direction = "UP"
        self.operations = {
            "UP": lambda x, y: (x, y+10),
            "DOWN": lambda x, y: (x, y-10),
            "LEFT": lambda x, y: (x-10, y),
            "RIGHT": lambda x, y: (x+10, y),
        }

    def body(self, x=0, y=0):
        points = ()
        for i in range(x, x + UNIT):
            for j in range(y, y + UNIT):
                points += ((i, j))
        return points
    
    def draw(self):
        for position in self.positions:
            print(position)
            points = self.body(x=position[0], y=position[1])
            pyglet.graphics.draw(UNIT ** 2, pyglet.gl.GL_POINTS, ('v2i', points))


    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        x, y = self.positions[-1]
        x, y = self.operations[self.direction](x, y)
        if x in range(0, MAX_WIDTH - UNIT + 1) and y in range(0, MAX_HEIGHT - UNIT + 1):
            self.positions.pop(0)
            self.positions.append([x, y])
    
    def grow(self):
        prev_x, prev_y = self.positions[-1]
        self.positions.append(self.operations[self.direction](prev_x, prev_y))


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
                self.pos[0], self.pos[1], self.pos[0] + UNIT, self.pos[1], 
                self.pos[0] + UNIT // 2, self.pos[1] - UNIT // 2, self.pos[0] + UNIT // 2, self.pos[1] + UNIT // 2,
                self.pos[0], self.pos[1] + UNIT // 2, self.pos[0] + UNIT, self.pos[1] - UNIT // 2,
                self.pos[0], self.pos[1] - UNIT // 2, self.pos[0] + UNIT, self.pos[1] + UNIT // 2,
                )
            ),
        )
        batch.draw()
    
    def reposition(self):
        rand_x = random.randint(0, MAX_WIDTH - UNIT)
        rand_y = random.randint(0, MAX_HEIGHT - UNIT)
        self.pos = [rand_x - rand_x % UNIT, rand_y - rand_y % UNIT]

window = pyglet.window.Window(width=MAX_WIDTH, height=MAX_HEIGHT)
snake = Snake()
food = Food()

def move_snake(qt):
    snake.move()

pyglet.clock.schedule_interval(move_snake, .10)

@window.event
def on_key_press(symbol, modifiers):
    movements = {
       pyglet.window.key.UP: "UP",
       pyglet.window.key.DOWN: "DOWN",
       pyglet.window.key.LEFT: "LEFT",
       pyglet.window.key.RIGHT: "RIGHT", 
    }
    try:
        snake.change_direction(movements[symbol])
    except KeyError:
        print("No such movement")

@window.event
def on_draw():
    window.clear()
    if snake.positions[-1] == food.pos:
        food.reposition()
        snake.grow()
        print("Gotcha!")
    snake.draw()
    food.draw()


pyglet.app.run()