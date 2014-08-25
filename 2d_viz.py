from pyglet import window, gl, graphics, app

win = window.Window(700, 500)
win.set_caption("2D IK Visualizer")

RED = (1, 0, 0, 1)

target = [350, 250]


def draw_point(p, rad, color):
    gl.glPointSize(rad)
    graphics.draw(1, gl.GL_POINTS, ('v2f', target), ('c4f', color))

@win.event
def on_draw():
    win.clear()
    
    gl.glLineWidth(8.0)
    graphics.draw(2, gl.GL_LINES, ('v2f', (10.0, 10.0, 100.0, 100.0)))
    
    # Draw target
    draw_point(target, 5, RED)
    


@win.event
def on_mouse_press(x, y, button, modifiers):
    target[0], target[1] = x, y

app.run()
