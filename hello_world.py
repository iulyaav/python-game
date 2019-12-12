import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label(
    'Hello World',
    font_name='Times New Roman',
    font_size=36,
    x=window.width//2, y=window.height - 80,
    anchor_x='center', anchor_y='center'
)

image = pyglet.resource.image("static/img/spies.jpg")


@window.event
def on_draw():
    window.clear()
    image.blit(150, 20)
    label.draw()


@window.event
def on_key_press(symbol, modifiers):
    print("A key was pressed: {}".format(symbol))

pyglet.app.run()