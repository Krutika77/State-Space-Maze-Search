import pygame

class Maze():
    
    pygame.init()

    def __init__(self):
        
        openFile = input("Enter name of input file: ")
        maze = open(openFile).read().split('\n')
        self.height = len(maze)
        self.width = len(maze[1])
        
        # Determining start, goal, block and path positions
        self.walls = [] 
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                try:
                    if maze[i][j] == "P":
                        self.start = (i, j)
                        temp.append(False)
                    elif maze[i][j] == ".":
                        self.goal = (i, j)
                        temp.append(False)
                    elif maze[i][j] == " ":
                        temp.append(False) 
                    else:
                        temp.append(True)
                except IndexError:
                    temp.append(False)
            self.walls.append(temp)

        # To store the solution path once we find one
        self.solution = None

    # Returns neighbouring nodes (where can we traverse to next)   
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = [] 
        for action, (r, c) in candidates:
            if r >= 0 and r < self.height and c >= 0 and c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
        
    # Finds the path and path cost
    def solve(self):
        
        self.step_cost = 0

        # Initializes the stack/queue to the starting position
        start = Node(state=self.start, parent=None, action=None)
        choice = input("Enter your choice: DFS OR BFS? ")
        if choice == "DFS":
            check = DFS_Stack()
        elif choice == "BFS":
            check = BFS_Queue()
        else:
            print("Invalid choice")
        check.push(start)

        # To make sure we do not end up checking the same node/path multiple times
        self.explored = set()

        # Until solution found
        while True:

            # Choose a node from the stack/queue
            node = check.pop()

            # If the node is the goal then we found a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                    self.step_cost += 1
                self.solution = (actions, cells)
                self.graphic_rep()
                return

            # Marks the node as explored
            self.explored.add(node.state)

            # Adds neighbors to the stack/list to visit next
            for action, state in self.neighbors(node.state):
                if not check.has_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    check.push(child)
                    
    # Displays the graphic demonstration of the maze and the path discovered using pygame
    def graphic_rep(self):
        
        block_size=20
        # canvas on which to display everything 
        window = (self.height*block_size,self.width*block_size)
        screen = pygame.display.set_mode(window)
        background = pygame.Surface(window)
        
        # Displaying the maze with red blocks representing the walls, blue the start position, green the goal and the path in yellow 
        
        for i, row in enumerate(self.walls[:len(self.walls)-1]):
            for j, col in enumerate(row):
                if col:
                    pygame.draw.rect(background,(255,0,0),(i*block_size,j*block_size,18,18))
                elif (i, j)==self.start:
                    pygame.draw.rect(background,(0,0,255),(i*block_size,j*block_size,18,18))
                elif (i, j)==self.goal:
                    pygame.draw.rect(background,(0,255,0),(i*block_size,j*block_size,18,18))
                elif (i, j) in self.solution[1]:
                    pygame.draw.rect(background,(255,225,0),(i*block_size,j*block_size,18,18))
                else:
                    pygame.draw.rect(background,(128,128,128),(i*block_size,j*block_size,18,18))
        
        screen.blit(background,(0,0))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        pygame.quit()

# Datastructure to store traversible steps as nodes
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Stack(LIFO) datastructure to store and traverse nodes, used for DFS search
class DFS_Stack():
    """A list is created here to keep track of the """
    def __init__(self):
        self.check = [] 

    def push(self, node):
        self.check.append(node)

    def has_state(self, state):
        for node in self.check:
            if node.state == state:
                return True

    def empty(self):
        if len(self.check) == 0:
            return True

    def pop(self):
        if self.empty():
            raise Exception("the stack is empty")
        else:
            node = self.check[-1]
            # removes the last node and updates the list
            self.check = self.check[:-1]
            # return the node to check weather its the "."(goal) or to discover its successor if not.
            return node

# Queue(FIFO) datastructure to store and traverse nodes, used for BFS search
class BFS_Queue(DFS_Stack):
# Inherits the remaining functions from DFS_Stack

    def pop(self):
        if self.empty():
            raise Exception("the queue is empty")
        else:
            node = self.check[0]
            self.check = self.check[1:]
            return node
        
m = Maze()
m.solve()
# Since all the step costs are equal to one, it displays the number of steps in the path taken
print("path cost:", m.step_cost)




