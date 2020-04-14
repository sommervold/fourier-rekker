import cmath

class Vector:
    def __init__(self, speed, constant):
        self.speed = speed
        self.id = -1
        self.pos = complex(0,0)
        self.endpoint = complex(0,0)
        self.constant = constant


    def calculate(self, t, pos):
        # calculate the vector
        self.pos = pos
        self.endpoint = pos + self.constant * cmath.exp(self.speed * 2 * cmath.pi * complex(0,1) * t)
        return self.endpoint

    def draw(self, canvas):

        # Draw the vector on the canvas
        x0,y0 = self.pos.real, self.pos.imag
        x1,y1 = self.endpoint.real, self.endpoint.imag
        canvas.coords(self.id, x0,y0,x1,y1)

    def create(self, canvas):
        self.id = canvas.create_line(0,0,0,0, width=3)
