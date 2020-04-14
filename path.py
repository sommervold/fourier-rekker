

class Path:
    def __init__(self, vectors, startpoint, color, width):
        self.startpoint = startpoint # Startpoint when calculating the vectors, acts like an offset.
        self.vectors = self.order_vectors(vectors) # List of vectors that create this path
        self.path_ids = [] # List of trace-line ids
        self.width = width # Width of the traceline
        self.color = color if not color == '' else 'blue' # Color of the traceline
        self.endpoint = self.startpoint
        self.prev_endpoint = self.endpoint
        self.calculate(0)
        self.calculate(0)



    def draw(self, canvas, num_lines):
        for vector in self.vectors:
            vector.draw(canvas)

         # Delete old trace-lines, add new.
        if len(self.path_ids) > num_lines: # Deleting the oldest line if there are too many
            canvas.delete(self.path_ids[0])
            self.path_ids.pop(0)

        # Add new trace-lines
        x0, y0 = self.prev_endpoint.real, self.prev_endpoint.imag
        x1, y1 = self.endpoint.real, self.endpoint.imag

        self.path_ids.append(canvas.create_line(x0,y0,x1,y1, width=self.width, fill=self.color))


    def calculate(self, t):
        self.prev_endpoint = self.endpoint
        self.endpoint = self.startpoint

        # Loop through vectors and calculate next position. Set startposition equals to the end position of the previous vector
        for vector in self.vectors:
            self.endpoint = vector.calculate(t, self.endpoint)


    def order_vectors(self, vectors):
        complete = [vectors[0]]
        del vectors[0]
        for vector in vectors:
            for i in range(len(complete)):
                v = complete[i]
                if abs(vector.constant) < abs(v.constant):
                    complete.insert(i, vector)
                    break
                elif i+1 == len(complete):
                    complete.insert(-1, vector)

        return complete
