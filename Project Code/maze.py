from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

ROWS, COLS = 25, 30

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1,0,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

START_POS = (28, 23)
GOAL_POS  = (1, 1)  

def is_valid_position(x, z):
    """Check if position is valid (within bounds and not a wall)"""
    return (0 <= x < COLS and 0 <= z < ROWS and maze[z][x] == 0)

def get_neighbors(x, z):
    """Get valid neighbors for a position"""
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dz in directions:
        nx, nz = x + dx, z + dz
        if is_valid_position(nx, nz):
            neighbors.append((nx, nz))
    return neighbors

# Agent (Robot)

class Agent:
    """Robot agent that navigates the maze"""
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.y = 0.3
        self.color = (0.2, 0.5, 0.9)    

    def draw(self):
        cx, cz = self.x + 0.5, self.z + 0.5
        
        # Main body
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(cx, self.y, cz)
        glScalef(0.4, 0.5, 0.3)
        glutSolidCube(1)
        glPopMatrix()

        # Head
        glColor3f(0.9, 0.9, 0.95)
        glPushMatrix()
        glTranslatef(cx, self.y + 0.4, cz)
        glutSolidSphere(0.18, 16, 16)
        glPopMatrix()

        # Eyes
        glColor3f(0.1, 0.9, 1.0)
        glPushMatrix()
        glTranslatef(cx - 0.08, self.y + 0.42, cz + 0.15)
        glutSolidSphere(0.04, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(cx + 0.08, self.y + 0.42, cz + 0.15)
        glutSolidSphere(0.04, 10, 10)
        glPopMatrix()

        # Antenna
        glColor3f(0.8, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(cx, self.y + 0.55, cz)
        glRotatef(90, 1, 0, 0)
        glutSolidCylinder(0.02, 0.15, 8, 8)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(cx, self.y + 0.7, cz)
        glutSolidSphere(0.05, 10, 10)
        glPopMatrix()

        # Arms
        glColor3f(self.color[0] * 0.8, self.color[1] * 0.8, self.color[2] * 0.8)
        glPushMatrix()
        glTranslatef(cx - 0.25, self.y, cz)
        glScalef(0.12, 0.35, 0.12)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(cx + 0.25, self.y, cz)
        glScalef(0.12, 0.35, 0.12)
        glutSolidCube(1)
        glPopMatrix()

        # Legs
        glPushMatrix()
        glTranslatef(cx - 0.1, self.y - 0.3, cz)
        glScalef(0.12, 0.3, 0.12)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(cx + 0.1, self.y - 0.3, cz)
        glScalef(0.12, 0.3, 0.12)
        glutSolidCube(1)
        glPopMatrix()

        # Chest light
        glColor3f(0.2, 1.0, 0.3)
        glPushMatrix()
        glTranslatef(cx, self.y + 0.1, cz + 0.16)
        glutSolidSphere(0.05, 10, 10)
        glPopMatrix()

    def move_to(self, x, z):
        """Move agent to position"""
        self.x, self.z = x, z
# Maze Visualizer
class MazeVisualizer:
    """Handles the 3D visualization of the maze"""
    
    def __init__(self, move_delay=0.15):
        self.agent = Agent(START_POS[0], START_POS[1])
        self.move_delay = move_delay
        self.last_update_time = 0
        
        # Algorithm data
        self.movement_sequence = []
        self.discovered_nodes = set()
        self.final_path = []
        
        # State tracking
        self.current_move_index = 0
        self.is_exploring = True
        self.is_following_path = False
        
    def set_algorithm_data(self, movement_sequence, discovered_nodes, final_path):
        """Set the data from the search algorithm"""
        self.movement_sequence = movement_sequence
        self.discovered_nodes = discovered_nodes
        self.final_path = final_path
        self.current_move_index = 0
        self.is_exploring = True
        
    def update_agent(self):
        """Update agent position based on time"""
        current_time = time.time()
        
        if current_time - self.last_update_time >= self.move_delay:
            if self.is_exploring and self.current_move_index < len(self.movement_sequence):
                pos = self.movement_sequence[self.current_move_index]
                self.agent.move_to(pos[0], pos[1])
                self.current_move_index += 1
                self.last_update_time = current_time
                
                if self.current_move_index >= len(self.movement_sequence):
                    self.is_exploring = False
                    self.is_following_path = True
                    self.current_move_index = 0
                    #the agent now is following the optimal path
                    
                    
            elif self.is_following_path and self.current_move_index < len(self.final_path):
                pos = self.final_path[self.current_move_index]
                self.agent.move_to(pos[0], pos[1])
                self.current_move_index += 1
                self.last_update_time = current_time
                
                if self.current_move_index >= len(self.final_path):
                    self.is_following_path = False
                    #the agent reched the goal

    
    def draw_discovered_node(self, x, z):
        """Draw red marker for discovered nodes"""
        glColor3f(0.4, 0.05, 0.05)
        glPushMatrix()
        glTranslatef(x + 0.5, 0.03, z + 0.5)
        glScalef(0.7, 0.06, 0.7)
        glutSolidCube(1)
        glPopMatrix()
    
    def draw_wall(self, x, z):
        """Draw wall (glass panel)"""
        glColor3f(0.7, 0.7, 0.75)
        glPushMatrix()
        glTranslatef(x + 0.5, 0.5, z + 0.5)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glColor3f(0.85, 0.92, 0.95)
        glPushMatrix()
        glTranslatef(x + 0.5, 0.5, z + 0.5)
        glScalef(0.9, 0.85, 0.9)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glColor3f(0.85, 0.85, 0.9)
        glPushMatrix()
        glTranslatef(x + 0.5, 1.0, z + 0.5)
        glScalef(1.0, 0.08, 1.0)
        glutSolidCube(1.0)
        glPopMatrix()
    
    def draw_scene(self):
        """Draw the complete scene"""
        # Floor
        glColor3f(0.95, 0.95, 0.97)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(COLS, 0, 0)
        glVertex3f(COLS, 0, ROWS)
        glVertex3f(0, 0, ROWS)
        glEnd()

        # Grid lines
        glColor3f(0.85, 0.85, 0.87)
        glBegin(GL_LINES)
        for i in range(ROWS + 1):
            glVertex3f(0, 0.01, i)
            glVertex3f(COLS, 0.01, i)
        for i in range(COLS + 1):
            glVertex3f(i, 0.01, 0)
            glVertex3f(i, 0.01, ROWS)
        glEnd()

        # Draw discovered nodes
        if self.is_exploring:
            nodes_to_show = set()
            for i in range(min(self.current_move_index, len(self.movement_sequence))):
                nodes_to_show.add(self.movement_sequence[i])
            
            for node in nodes_to_show:
                if node != START_POS and node != GOAL_POS:
                    self.draw_discovered_node(node[0], node[1])
        else:
            for node in self.discovered_nodes:
                if node != START_POS and node != GOAL_POS:
                    self.draw_discovered_node(node[0], node[1])

        # Walls
        for r in range(ROWS):
            for c in range(COLS):
                if maze[r][c] == 1:
                    self.draw_wall(c, r)

        # Start marker
        glColor3f(0.2, 0.8, 0.2)
        glPushMatrix()
        glTranslatef(START_POS[0] + 0.5, 0.02, START_POS[1] + 0.5)
        glScalef(0.9, 0.04, 0.9)
        glutSolidCube(1)
        glPopMatrix()

        # Goal marker
        glColor3f(1.0, 0.84, 0.0)
        glPushMatrix()
        glTranslatef(GOAL_POS[0] + 0.5, 0.02, GOAL_POS[1] + 0.5)
        glScalef(0.9, 0.04, 0.9)
        glutSolidCube(1)
        glPopMatrix()

        # Agent
        self.agent.draw()
        
