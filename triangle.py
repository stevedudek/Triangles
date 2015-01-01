"""
Model to communicate with a Triangle simulator over a TCP socket

"""

TRI_GEN = 12    # Size of Big Triangles - Fixed at 12

"""
Parameters for each Triangle: (x,y), corner, direction
Corner: connector attachment is 'L' = Left, 'R' = Right, 'C' = Center
Direction: As viewed from corner, lights go 'L' = Left, 'R' = Right
"""
NUM_BIG_TRI = 6

BIG_COORD = [ ((0, 0), 'C', 'R'),
              ((0, 1), 'L', 'L'),
              ((4, 0), 'L', 'R'),
              ((2, 0), 'C', 'L'),
              ((6, 0), 'C', 'R'),
              ((6, 1), 'L', 'L') ]

from HelperFunctions import ROTATE_CLOCK, ROTATE_COUNTER, ROTATE_COORD_CLOCK
from HelperFunctions import distance
from collections import defaultdict
from color import RGB
from random import choice

def load_triangles(model):
    return Triangle(model)

class Triangle(object):

    """
    Triangle coordinates are stored in a hash table.
    Keys are (x,y) coordinate tuples
    Values are (strip, pixel) tuples, sometimes more than one.
    
    Frames implemented to shorten messages:
    Send only the pixels that change color
    Frames are hash tables where keys are (x,y) coordinates
    and values are (r,g,b) colors
    """
    def __init__(self, model):
        self.model = model
        self.cellmap = self.add_strips(BIG_COORD)
        self.curr_frame = {}
        self.next_frame = {}
        self.init_frames()

    def __repr__(self):
        return "Triangles(%s)" % (self.model, self.side)

    def all_cells(self):
        "Return the list of valid coords"
        return list(self.cellmap.keys())

    def cell_exists(self, coord):
        return self.cellmap[coord]

    def set_cell(self, coord, color):
        # inputs an (x,y) coord
        if self.cell_exists(coord):
            self.next_frame[coord] = color

    def set_cells(self, coords, color):
        for coord in coords:
            self.set_cell(coord, color)

    def set_all_cells(self, color):
        self.set_cells(self.all_cells(), color)

    def clear(self):
        ""
        self.force_frame()
        self.set_all_cells((0,0,0))
        self.go()

    def go(self):
        self.send_frame()
        self.model.go()
        self.update_frame()

    def update_frame(self):
        for coord in self.next_frame:
            self.curr_frame[coord] = self.next_frame[coord]

    def send_frame(self):
        for coord,color in self.next_frame.items():
            # Has the color changed? Hashing to color values
            if self.curr_frame[coord] != color:
                # Hashing to strip, fixture values
                self.model.set_cells(self.cellmap[coord], color)

    def force_frame(self):
        for coord in self.curr_frame:
            self.curr_frame[coord] = (-1,-1,-1)  # Force update

    def init_frames(self):
        for coord in self.cellmap:
            self.curr_frame[coord] = (0,0,0)
            self.next_frame[coord] = (0,0,0)
            
    def get_rand_cell(self):
        return choice(self.all_cells())

    def get_strip_from_coord(self, coord):
        "pulls the first strip that fits a coordinate"
        choices = self.cellmap[coord]
        (strip, fix) = choices[0]
        return strip

    def add_strips(self, coord_table):
        cellmap = defaultdict(list)
        for strip, (big_coord, corner, direction) in enumerate(coord_table):
            cellmap = self.add_strip(cellmap, strip, big_coord, corner, direction)
        return cellmap

    def add_strip(self, cellmap, strip, big_coord, corner, direction):
        """
        Stuff the cellmap with a Triangle strip, going row by column
        """

        (x_offset, y_offset) = big_coord
        x_offset *= TRI_GEN
        y_offset *= TRI_GEN
        if point_up(big_coord) == False:
            y_offset += TRI_GEN - 1

        for y in range(TRI_GEN):
            for x in range(row_width(y)):
                xcoord = x_offset + x + y
                ycoord = y_offset
                if point_up(big_coord):
                    ycoord += y
                else:
                    ycoord -= y
                coord = (xcoord,ycoord)
                fix = self.calc_fix(coord, big_coord, corner, direction)
                cellmap[coord].append((strip, fix))
        
        return cellmap

    def calc_fix(self, coord, big_coord, corner, direction):
        """
        This heavy lifter function converts coordinates in fixtures
        """
        fix = 0
        rowflip = 0  # Whether the row flips order
          
        (x,y) = coord
        (big_x, big_y) = big_coord

        x -= (big_x * TRI_GEN)    # Remove big-grid offsets
        y -= (big_y * TRI_GEN)    # Remove big-grid offsets
        
        # Fix downward pointing grids
        if point_up(big_coord) == False:    # odd = pointing down
            y = TRI_GEN - y - 1
        
            # Swap the light direction: L -> R and R -> L
            if direction == 'L':
              direction = 'R'
            else:
              direction = 'L'
          
        if direction == 'R':    # Left-right direction of wiring
            rowflip = 1
        else:
            rowflip = 0
          
        # y row coordinate first. We're building up LEDs one row at a time.
        for row in range(y):
            fix += row_width(row)
        
        # add x column coordinate. Even rows serpentine back
        if y % 2 == rowflip:    # even
            fix += row_width(y) - (x-y) - 1
        else:   # odd
            fix += (x-y)

        # Coordinate transformation depending on how the Triangle is hung
        if corner == 'C':
            return ROTATE_CLOCK[fix]
        elif corner == 'R':
            if direction == 'L':
                return fix
            else:
                return ROTATE_COUNTER[fix]

        else:
            if direction == 'L':
                return ROTATE_COUNTER[fix]
            else:
                return fix

    def get_row(self, row):
        "Return all (x,y) coordinates on a row (y)"
        cells = []
        for coord in self.all_cells():
            (x,y) = coord
            if y == row:
                cells.append(coord)
        return cells

    def six_mirror(self, coord):
        "Returns the six-fold mirror coordinates"
        mirrors = []
        for cell in self.mirror_coords(coord):
            mirrors.append(coord)
            mirrors.append(vert_mirror(coord))

        return mirrors

    def mirror_coords(self, coord):
        "Returns the coordinate with its two mirror coordinates"
        
        mirrors = []
        mirrors.append(coord)
        mirrors.append(self.rotate_left(coord))
        mirrors.append(self.rotate_right(coord))

        return mirrors

    def rotate_right(self, coord):
        """
        Rotates a coord right in its triangle space
        """
        return self.rotate_left(self.rotate_left(coord))

    def rotate_left(self, coord):
        """
        Rotates a coord left in its triangle space
        """
        strip = self.get_strip_from_coord(coord)
        reduced_coord = reduce_coord(coord, strip)
        rotated_coord = ROTATE_COORD_CLOCK[reduced_coord]
        expanded_coord = expand_coord(rotated_coord, strip)
        #print coord, reduced_coord, rotated_coord, expanded_coord
        return expanded_coord
    
##
## tri cell primitives
##

def point_up(coord):
    (x,y) = coord
    if (x+y) % 2 == 0:
        return True
    else:
        return False

def get_big_coord(strip):
    ((big_x, big_y), corner, direction) = BIG_COORD[strip]
    return (big_x, big_y)

def row_width(row):
    return ((TRI_GEN-row-1)*2)+1

def vert_mirror(coord):
    """
    Returns the coordinate and its vertical mirror
    """
    (x,y) = coord
    new_x = row_width(y) - x - 1

    return coord + (new_x,y)

def min_max_row():
    "Returns the (minimum,maximum) row (y) values"
    min_y = 1000
    max_y = -1000

    for ((big_x, big_y), corner, direction) in BIG_COORD:
        if big_y < min_y:
            min_y = big_y
        if big_y > max_y:
            max_y = big_y

    return (min_y * TRI_GEN, (max_y * TRI_GEN)+(TRI_GEN-1) )

def get_base(strip):
    (big_x,big_y) = get_big_coord(strip)
    return (big_x * TRI_GEN, big_y * TRI_GEN)

def get_all_func(get_func):
    """
    Iterator over all Triangles
    Function must return a list of coordinates
    """
    #return [get_func(tri) for tri in range(NUM_BIG_TRI)]
    cells = []
    for tri in range(NUM_BIG_TRI):
        cells += get_func(tri)
    return cells

def reduce_coord(coord, strip=0):
    "Reduces a coordinate to (0,0) space"
    (big_x,big_y) = get_big_coord(strip)
    (x,y) = coord
    x -= big_x * TRI_GEN
    y -= big_y * TRI_GEN

    if point_up(get_big_coord(strip)) == False:
        y = TRI_GEN-1-y

    return (x,y)

def expand_coord(coord, strip=0):
    "Expands a reduced coordinate back to its big-tri space"
    (big_x,big_y) = get_big_coord(strip)
    (x,y) = coord

    if point_up(get_big_coord(strip)) == False:
        y = TRI_GEN-1-y

    x += big_x * TRI_GEN
    y += big_y * TRI_GEN

    return (x,y)

def center(strip=0):
    "Returns a Triangle's center coordinate. Handles point-down triangles too"
    pad = TRI_GEN-1
    (x,y) = get_base(strip)
    if point_up(get_big_coord(strip)):
        return (x + pad, y + (int)(TRI_GEN*0.4))
    else:
        return (x + pad, y + (int)(TRI_GEN*0.6))

def all_centers():
    return [center(strip) for strip in range(NUM_BIG_TRI)]

def corners(strip=0):
    "Returns the 3 corner coordinates of a Triangle"
    pad = TRI_GEN-1
    (x,y) = get_base(strip)
    if point_up(get_big_coord(strip)):
        return [(x,y), (x+pad,y+pad), (x+pad+pad,y)]    # L,C,R
    else:
        return [(x,y+pad), (x+pad,y), (x+pad+pad,y+pad)]    # L,C,R

def all_corners():
    "Return the corners of all triangles"
    return get_all_func(corners)

def left_corner(strip=0):
    return corners(strip)[0]

def all_left_corners():
    return [left_corner(strip) for strip in range(NUM_BIG_TRI)]

def edge(strip=0):
    "Returns the edge pixel coordinates of a Triangle"
    "Uses the 3 corners to draw each linear edge"

    corns = corners(strip)
    width = row_width(0)-1

    if point_up(get_big_coord(strip)):
        return tri_in_line(corns[0],1,width) + tri_in_line(corns[1],5,width) + tri_in_line(corns[2],3,width)
    else:
        return tri_in_line(corns[0],5,width) + tri_in_line(corns[1],1,width) + tri_in_line(corns[2],3,width)

def all_edges():
    "Return all the edge pixels"
    return get_all_func(edge)

def neighbors(coord):
    "Returns a list of the three tris neighboring a tuple at a given coordinate"
    (x,y) = coord

    if (x+y) % 2 == 0:  # Even
        neighbors = [ (1, 0), (0, -1), (-1, 0) ]    # Point up
    else:
        neighbors = [ (1, 0), (0, 1), (-1, 0) ]     # Point down

    return [(x+dx, y+dy) for (dx,dy) in neighbors]

def tri_in_line(coord, direction, distance=0):
    """
    Returns the coord and all pixels in the direction
    along the distance
    """
    return [tri_in_direction(coord, direction, x) for x in range(distance)]

def tri_in_direction(coord, direction, distance=1):
    """
    Returns the coordinates of the tri in a direction from a given tri.
    Direction is indicated by an integer
    There are 6 directions along hexagonal axes

     2  /\  1
     3 |  | 0
     4  \/  5

    """
    for i in range(distance):
        coord = tri_nextdoor(coord, direction)
    return coord

def tri_nextdoor(coord, direction):
    """
    Returns the coordinates of the adjacent tri in the given direction
    Even (point up) and odd (point down) tri behave different
    Coordinates determined from a lookup table
    """
    _evens = [ (1, 0), (1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1) ]
    _odds  = [ (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (1, 0) ]

    direction = direction % 6

    (x,y) = coord

    if (x+y) % 2 == 0:  # Even
        (dx,dy) = _evens[direction]
    else:
        (dx,dy) = _odds[direction]

    return (x+dx, y+dy)

def get_rand_neighbor(coord):
    """
    Returns a random neighbors
    Neighbor may not be in bounds
    """
    return choice(neighbors(coord))

def clock(coord, center):
    "Returns the clockwise cell"
    neighs = neighbors(coord)
    closest = near_neighbor(coord, center)

    for i in range(3):
        if closest == neighs[i]:
            return neighs[(i+2) % 3]

    print "can't find a clock cell"

def counterclock(coord, center):
    "Returns the counterclockwise cell"
    neighs = neighbors(coord)
    closest = near_neighbor(coord, center)

    for i in range(3):
        if closest == neighs[i]:
            return neighs[(i+1) % 3]

    print "can't find a counterclock cell"

def near_neighbor(coord, center):
    "Returns the neighbor of coord that is closest to center"
    best_coord  = coord
    min_dist = 1000

    for c in neighbors(coord):
        dist = distance(c, center)
        if dist < min_dist:
            best_coord = c
            min_dist = dist

    return best_coord

def get_ring(center, size):
    "Returns a list of coordinates that make up a centered ring"
    size = 1 + (2*size) # For hex shape

    t = tri_in_direction(center, 4, size)
    results = []
    for i in range(6):
        for j in range(size):
            results.append(t)
            t = tri_nextdoor(t,i)
    return results

def tri_shape(start, size):
    """
    Returns a list of coordinates that make up a triangle
    Triangle's left corner will be the 'start' pixel
    start's location will determine whether triangle points up or down
    """
    size = 1 + (2*size) # For hex shape

    (x,y) = start

    if point_up(start):
        corns = [start, tri_in_direction(start,1,size+1), tri_in_direction(start,0,size+1)]
    else:
        corns = [tri_in_direction(start,5,size+1), start, tri_in_direction(start,0,size+1)]

    return tri_in_line(corns[0],1,size) + tri_in_line(corns[1],5,size) + tri_in_line(corns[2],3,size)
