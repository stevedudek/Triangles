from HelperFunctions import*

#
# Fader class and its collection: the Faders class
#
class Faders(object):
    def __init__(self, triangle_model):
        self.triangle = triangle_model
        self.fader_array = []
        self.max_faders = 1000

    def add_fader(self, color, pos, change=0.1, intense=1.0, growing=False):
        new_fader = Fader(self.triangle, color, pos, change, intense, growing)
        self.add_fader_obj(new_fader)

    def add_fader_obj(self, new_fader):
        if self.num_faders() < self.max_faders:
            self.fader_array.append(new_fader)

    def cycle_faders(self, refresh=True):
        if refresh:
            self.triangle.black_all_cells()

        # Draw, update, and kill all the faders
        for f in self.fader_array:
            if f.is_alive():
                f.draw_fader()
                f.fade_fader()
            else:
                f.black_cell()
                self.fader_array.remove(f)

    def num_faders(self):
        return len(self.fader_array)

    def fade_all(self):
        for f in self.fader_array:
            f.black_cell()
            self.fader_array.remove(f)


class Fader(object):
    def __init__(self, triangle_model, color, pos, change=0.25, intense=1.0, growing=False):
        self.triangle = triangle_model
        self.pos = pos
        self.color = color
        self.intense = intense
        self.growing = growing
        self.decrease = change

    def draw_fader(self):
        self.triangle.set_cell(self.pos, gradient_wheel(self.color, self.intense))

    def fade_fader(self):
        if self.growing:
            self.intense += self.decrease
            if self.intense >= 1.0:
                self.intense = 1.0
                self.growing = False
                self.intense -= self.decrease
        else:
            self.intense -= self.decrease

    def is_alive(self):
        return self.growing or self.intense > 0.01

    def black_cell(self):
        self.triangle.black_cell(self.pos)


#
# Brick class and its collection: the Bricks class
#
class Bricks(object):
    def __init__(self, trianglemodel, bounce=False):
        self.triangle = trianglemodel
        self.bounce = bounce
        self.brick_array = []

    def add_brick(self, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0, use_faders=False, change=0.25):
        new_brick = Brick(self.triangle, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x, accel_y, use_faders, change)
        self.brick_array.append(new_brick)

    def move_bricks(self, refresh=True):
        if refresh:
            self.triangle.black_all_cells()

        # Draw, move, update, and kill all the bricks
        for b in self.brick_array:
            b.draw_brick()
            b.move_brick(self.bounce)
            b.age_brick()

        for b in self.brick_array:
            if not b.is_alive():
                self.brick_array.remove(b)

    def kill_brick(self, b):
        if b in self.brick_array:
            b.kill_faders()
            self.brick_array.remove(b)

    def set_all_dx(self, dx):
        for b in self.brick_array:
            b.set_dx(dx)

    def set_all_dy(self, dy):
        for b in self.brick_array:
            b.set_dy(dy)

    def set_all_accel_x(self, accel_x):
        for b in self.brick_array:
            b.set_accel_x(accel_x)

    def set_all_accel_y(self, accel_y):
        for b in self.brick_array:
            b.set_accel_y(accel_y)

    def num_bricks(self):
        return len(self.brick_array)

    def get_bricks(self):
        return self.brick_array


class Brick(object):
    def __init__(self, trianglemodel, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0,
                 use_faders=False, change=0.25):
        self.triangle = trianglemodel
        self.color = color
        self.life = life
        self.pos = pos
        self.length = length
        self.pitch = pitch
        self.length_x = length_x
        self.length_y = length_y
        self.dx = dx
        self.dy = dy
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.use_faders = use_faders
        self.faders = Faders(trianglemodel) if self.use_faders else None
        self.change = change

    def draw_brick(self):
        for i in range(int(round(self.length / self.pitch)) + 1):
            pos = (round(self.pos[0] + (i * self.pitch * self.length_x)),
                   round(self.pos[1] + (i * self.pitch * self.length_y)))
            if self.use_faders:
                self.faders.add_fader(self.color, pos, intense=1.0, growing=False, change=self.change)
            else:
                self.triangle.set_cell(pos, self.color)

        if self.use_faders:
            self.faders.cycle_faders(False)

    def move_brick(self, bounce):
        new_x = self.pos[0] + self.dx
        new_y = self.pos[1] + self.dy

        if bounce:
            if new_x < 0 or new_x >= self.triangle.width:
                self.dx *= -1
                new_x = self.pos[0] + self.dx
            if new_y < 0 or new_y >= self.triangle.height:
                self.dy *= -1
                new_y = self.pos[1] + self.dy

        self.pos = (new_x, new_y)
        self.dx, self.dy = self.dx + self.accel_x, self.dy + self.accel_y

    def age_brick(self):
        self.life -= 1

    def is_alive(self):
        return self.life > 0

    def get_coord(self):
        return self.pos

    def get_x(self):
        (x,y) = self.pos
        return x

    def get_y(self):
        (x,y) = self.pos
        return y

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def get_life(self):
        return self.life

    def set_dx(self, dx):
        self.dx = dx

    def set_dy(self, dy):
        self.dy = dy

    def set_accel_x(self, accel_x):
        self.accel_x = accel_x

    def set_accel_y(self, accel_y):
        self.accel_y = accel_y

    def set_length_x(self, length_x):
        self.length_x = length_x

    def set_length_y(self, length_y):
        self.length_y = length_y

    def set_x(self, x):
        (old_x, y) = self.pos
        self.pos = (x, y)

    def set_y(self, y):
        (x, old_y) = self.pos
        self.pos = (x, y)

    def set_life(self, life):
        self.life = life

    def kill_faders(self):
        if self.faders:
            self.faders.fade_all()