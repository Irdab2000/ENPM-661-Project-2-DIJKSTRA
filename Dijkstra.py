#!/usr/bin/python3
import queue
from obstacle_gen import gen_obstacles
import sys
import pygame
sys.setrecursionlimit(60000)


visited = []  #Stores all the nodes that have been visited (open list)
explored = [] #Stores all the nodes with the optimum cost and parent (closed list)
#action_set = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
num_actions = 8 
free_array,clearance_array = gen_obstacles()
#print("Got necessary arrays") # To get coordinates of obstacles and free spaces
path_gen = [] # list to dtore path generated


class Node:
    def __init__(self):
        self.parent_idx = None #Parent index
        self.state_idx = None #State index
        self.cost_to_come = 0 #Cost to come to state


def check_if_in_visited(node):
    #print("Checking in visited") #Function to check if node is in visited list 
    flag = True
    for dummy in visited:
        if(dummy.state_idx == node.state_idx):
            flag = False
            break
        #print(flag)
    return flag 

def check_if_in_explored(node):
    #print("CHecking in explored")#Function to check if node is in explored list
    flag = True
    for dummy in explored:
        if(dummy.state_idx == node.state_idx):
            flag = False
            #print(flag)
            break
    return flag 


def copy_node(node): #Function to get a copy of node
    copy = Node()
    copy.cost_to_come = node.cost_to_come
    copy.parent_idx = node.parent_idx
    copy.state_idx = node.state_idx
    return copy


def append_to_explored(node,i,j,added_cost): #FUnction that checks necessary conditions and appends to closed list
        #print("moving north")
        curr_node = copy_node(node)
        new_posn = [curr_node.state_idx[0] +i,curr_node.state_idx[1]+j] #Nextt state
        if([new_posn[0],new_posn[1]] in free_array): #Checking if new position is in fre space
            curr_node.state_idx = new_posn #Updating position
            curr_node.parent_idx = node.state_idx #Updating parent
            new_cost = node.cost_to_come + added_cost 
            curr_node.cost_to_come = new_cost #Updating new cost
            for dummy in range(len(visited)):
                if(visited[dummy].state_idx == curr_node.state_idx): #Checking if the node is in visited list
                    if(new_cost > visited[dummy].cost_to_come): #If new cost is greater than cost already present
                        curr_node.cost_to_come = visited[dummy].cost_to_come #Updating new cost
                        curr_node.parent_idx = visited[dummy].parent_idx #Updating parent 
                        break
             #print("[0,0]curr_node =",curr_node.state_idx)
            if(check_if_in_explored(curr_node)): #Checking if node is in visited
               for dummy_node in visited: 
                    if(dummy_node.state_idx == curr_node.state_idx):
                        #print("Match found")
                        #print("Parent of",curr_node.state_idx," is:",curr_node.parent_idx)
                        #print("Appendind coord to explored:",curr_node.state_idx)
                        explored.append(dummy_node) #Appending to explored 
                        break     

def get_cost(node,i,j,added_cost):
        #print("Getting cost") #Function to get cost for action and updating visited (open) list
        curr_node = copy_node(node)  
        #print("coord:",curr_node.state_idx)
        new_posn = [curr_node.state_idx[0]+i,curr_node.state_idx[1]+j] #Updating position
        if([new_posn[0],new_posn[1]]  in free_array): #Checking if new position is in fre space
            curr_node.state_idx = new_posn #Updating position
            curr_node.parent_idx = node.state_idx #Updating parent
            new_cost = node.cost_to_come + added_cost
            #curr_node.cost_to_come = new_cost
            #print("[0,0]curr_node =",curr_node.state_idx)
            if(check_if_in_explored(curr_node)): #Checking if node is in explored (closed) list
                if(check_if_in_visited(curr_node)): #Checking if node is in visited (open) list
                    #new_cost = node.cost_to_come + 1
                    #print("Appending to visited")
                    curr_node.cost_to_come = new_cost #Updating the cost
                    #print("Moving north, Appendng coord to visited:",curr_node.state_idx)
                    visited.append(curr_node) #Appending to visited
                else:                                   #If already in visited node
                    #print("Updating cost to move north")
                    for dummy in range(len(visited)):   
                        if(visited[dummy].state_idx == curr_node.state_idx):
                            if(new_cost < visited[dummy].cost_to_come): #If new cost calculated is lesser than the cost already present
                                visited[dummy].cost_to_come = new_cost
                                visited[dummy].parent_idx = curr_node.parent_idx # Updating cost and parent in visited list
                                break
                            else:
                                new_cost = visited[dummy].cost_to_come 
            else:
                return 100000 #Returning high cost if the node is already in explored list 
            return new_cost #Returning the calculated cost
        else:
            #print("Cannot move north:")
            return 100000   #Returning highcost if node is not in bounded space or on an obstacle

def move_north(node,optimal): #Function to move up
    if(optimal == True): #this action has been chosen as optimal 
        y_move = -1 # One row before current node
        x_move = 0  #Same column
        added_cost = 1 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
        

    else: #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = -1
        x_move = 0 
        added_cost = 1
        cost =get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost

def move_south(node,optimal): #Function to move down
    if(optimal == True): # this action has been chosen as optimal
        y_move = 1 # One row after current node
        x_move = 0 #Same column
        added_cost = 1 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost)#Append to explored
        
    else: #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = 1
        x_move = 0 
        added_cost = 1
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost

def move_east(node,optimal): #Function to move right
    if(optimal == True):  # this action has been chosen as optimal
        y_move = 0 # Same row
        x_move = 1 # One column after current node
        added_cost = 1 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
    
    else: #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = 0
        x_move = 1 
        added_cost = 1
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost

def move_west(node,optimal): #Function to move left
    if(optimal == True): # this action has been chosen as optimal
        y_move = 0 # Same row
        x_move = -1 # One column before current node
        added_cost = 1 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
    else:   #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = 0 
        x_move = -1 
        added_cost = 1
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost

def move_northeast(node,optimal): #Function to move up-right
    if(optimal == True):  # this action has been chosen as optimal
        y_move = 1 # One row after current node
        x_move = 1 ## One column after current node
        added_cost = 1.4 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
    else:  #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = 1 
        x_move = 1
        added_cost = 1.4
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost
    
def move_northwest(node,optimal): #Function to move up-left
    if(optimal == True): # this action has been chosen as optimal
        y_move = 1 # One row after current node
        x_move = -1 # One column before current node
        added_cost = 1.4 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
    else:  #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = 1
        x_move = -1
        added_cost = 1.4
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost  #Returns the calculated cost

def move_southeast(node,optimal): #Function to move down-right
    if(optimal == True): # this action has been chosen as optimal
        y_move = -1 # One row before current node
        x_move = 1 # One column after current node
        added_cost = 1.4 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored
    else:  #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = -1
        x_move = 1
        added_cost = 1.4
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost

def move_southwest(node,optimal): #Function to move down-left
    if(optimal == True): # this action has been chosen as optimal
        y_move = -1 # One row before current node
        x_move = -1 # One column before current node
        added_cost = 1.4 #Cost to move in that direction
        append_to_explored(node,x_move,y_move,added_cost) #Append to explored        
    else:  #Not yet chosen as optimal, going to get cost to move in this direction
        y_move = -1
        x_move = -1
        added_cost = 1.4
        cost = get_cost(node,x_move,y_move,added_cost)
        return cost #Returns the calculated cost
        
def backtrack(goal_node): #Function that implements backtracking

    visited_set = [] 
    while(goal_node.parent_idx is not None): #Runs till it reaches the start node
        #print("parent index of ",goal_node.state_idx," is: ", goal_node.parent_idx)
        
        path_gen.append(goal_node.state_idx) #Appending to the list that stores path
        visited_set.append(goal_node.state_idx)
        #print(path_gen[i])

        for node in explored:
             if(node.state_idx == goal_node.parent_idx):
                 if node.state_idx in visited_set:
                     print(node.state_idx)
                     raise ValueError("Cycle detected in path")
                 else:
                    #print("Match found:", goal_node.state_idx)
                    goal_node = copy_node(node)
                    #print("After change:",goal_node.state_idx)
                    break
    print("Backtracking complete")
  
def dijkstra(node,goal):  #Dijkstra fun
    curr_node = copy_node(node)
    print("Running:,",curr_node.state_idx)
    cost_arr = []   
    cost_up = move_north(curr_node,False) #Get cost to move up
    #print("cost to go north from ",curr_node.state_idx,":",cost_up)
    cost_arr.append(cost_up) 
    cost_down = move_south(curr_node,False) #Get cost to move down
    #print("cost to go south from ",curr_node.state_idx,":",cost_down)
    cost_arr.append(cost_down) 
    cost_right= move_east(curr_node,False) #Get cost to move right
    #print("cost to go east from ",curr_node.state_idx,":",cost_right)
    cost_arr.append(cost_right)
    cost_left= move_west(curr_node,False) #Get cost to move left
    #print("cost to go left from ",curr_node.state_idx,":",cost_left)
    cost_arr.append(cost_left)
    cost_up_right= move_northeast(curr_node,False) #Get cost to move up-right
    #print("cost to go northeast from ",curr_node.state_idx,":",cost_up_right)
    cost_arr.append(cost_up_right)
    cost_up_left= move_northwest(curr_node,False) #Get cost to move up-left
   # print("cost to go northwest from ",curr_node.state_idx,":",cost_up_left)
    cost_arr.append(cost_up_left)
    cost_down_right= move_southeast(curr_node,False) #Get cost to move down-right
    #print("cost to go southeast from ",curr_node.state_idx,":",cost_down_right)
    cost_arr.append(cost_down_right)
    cost_down_left= move_southwest(curr_node,False) #Get cost to move down-left
   # print("cost to go southwest from ",curr_node.state_idx,":",cost_down_left)
    cost_arr.append(cost_down_left)
    ind = cost_arr.index(min(cost_arr)) #Getting minimum cost
    #print("optmal action chosen")
    if ind == 0:
        move_north(curr_node,True)   #Choosing action based on the index
    elif ind == 1:
        move_south(curr_node,True)
    elif ind ==2 :
        move_east(curr_node,True)
    elif ind == 3 :
        move_west(curr_node,True)
    elif ind == 4 :
        move_northeast(curr_node,True)
    elif ind == 5 :
        move_northwest(curr_node,True)
    elif ind == 6 :
        move_southeast(curr_node,True)
    elif ind == 7 :
        move_southwest(curr_node,True)

    res = visited.pop(0)  #Popping the first node in visited (open) list
    #print("Popped from visited:",res.state_idx)
    #print(visited[0].state_idx)
    #dijkstra(visited[0],goal)
    return visited[0]

def get_startcoord_input(): #function to get start coordinates from user
    flag = False
    x = int(input("Enter x-ccordinate of start position:"))
    y = int(input("Enter y coordinate of start position:"))
    y = 249-y
    if(x<0 or x>=600 or y<0 or y>=250):
        print("Start coordinates out of bounds, Please enter x and y coordinates again")
        return [flag]
    elif([x,y] in clearance_array):
        print("Start coordinates on an obstacle, Please enter x and y coordinates again")
        return [flag]
    else:
        return [True,x,y]
def get_goalcoord_input(): #Function to get goal coordinates from user
    flag = False
    xg = int(input("Enter x-ccordinate of goal position:"))
    yg = int(input("Enter y coordinate of goal position:"))
    yg = 249-yg
    if(xg<0 or xg>=600 or yg<0 or yg>=250):
        print("Goal coordinates out of bounds, Please enter x and y coordinates again")
        return [flag]
    elif([xg,yg] in clearance_array):
        print("goal coordinates on an obstacle, Please enter x and y coordinates again")
        return [flag]
    else:
        return [True,xg,yg]

def visualize(path_gen,visited): #Function to visualize the graph
    pygame.init()

    # Set the window dimensions
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 250

    # Create the Pygame window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Obstacle Course")

    # Define the colors
    BACKGROUND_COLOR = pygame.Color("red")
    OBSTACLE_COLOR = pygame.Color("black")
    CLEARANCE_COLOR = pygame.Color("white")
    VISITED_COLOR = pygame.Color("green")
    PATH_COLOR = pygame.Color("blue")

    # Create the surface for the obstacle course
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Fill the surface with the background color
    surface.fill(BACKGROUND_COLOR)
    #obstacles = []
    pygame.draw.rect(surface, CLEARANCE_COLOR, (100-5, 145-5,50+10 ,100+10))
    pygame.draw.polygon(surface, CLEARANCE_COLOR, ((300,200+5),(365+4,162),(365+4,87),(300,50-5),(235-4,87),(235-4,162))) 
    pygame.draw.rect(surface, CLEARANCE_COLOR, (100-5,5-5,50+10,100+10))                                                                #Printing directly using the coordinates for visualization.
    pygame.draw.polygon(surface, CLEARANCE_COLOR, ((460-3,225+12),(460-3,25-12),(510+5,125)))
    # Draw the obstacles on the surface
    pygame.draw.rect(surface, OBSTACLE_COLOR, (100, 145,50 ,100))  
    pygame.draw.polygon(surface, OBSTACLE_COLOR, ((300,200),(365,162),(365,87),(300,50),(235,87),(235,162)))
    pygame.draw.rect(surface, OBSTACLE_COLOR, (100,5,50,100))
    pygame.draw.polygon(surface, OBSTACLE_COLOR, ((460,225),(460,25),(510,125)))   

    for idx,any in enumerate(explored):
        pygame.draw.rect(surface,VISITED_COLOR,(any.state_idx[0],any.state_idx[1],1,1))
        window.blit(surface,(0,0))
        pygame.display.update()
        pygame.time.wait(2)
    
    for idx, every in enumerate(path_gen):
        pygame.draw.rect(surface,PATH_COLOR,(every[0],every[1],1,1))
    # Blit the updated surface onto the Pygame window
        window.blit(surface, (0, 0))
    # Update the Pygame window display
        pygame.display.update()
    # Wait for a short time to show the current coordinate
        pygame.time.wait(2)

    
    # Blit the surface onto the Pygame window
    window.blit(surface, (0, 0))

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    start = Node()
    start.parent_idx = None #Initializing start node
    start.cost_to_come = 0
    a = True
    start_input = []
    while(a not in start_input):
        start_input = get_startcoord_input()    
    start.state_idx = [start_input[1],start_input[2]]
    goal_input = []
    while(a not in goal_input):
        goal_input = get_goalcoord_input()
    goal = [goal_input[1],goal_input[2]]
    #print("Appending coord to visited :", start.state_idx)
    visited.append(start) #Appending start node to open list
    #print("Appendind coord to explored:",start.state_idx)
    explored.append(start) #Appending start node to open list
    node = dijkstra(start,goal)
    flag = True
    while(flag == True): #To avoid recursion, I am using a loop to run Dijkstra.
        if(node.state_idx == goal): #Checking if goal has been reached
            curr_node = copy_node(node)
            print("Goal Reached\n")
        #visited.append(curr_node)
        #explored.append(curr_node)
        #for dummy_node in explored:
        #    print(dummy_node.state_idx)
            backtrack(curr_node) #Backtrack fun called
            path_gen.append(start.state_idx)
            flag = False
        else:
            node = dijkstra(node,goal)
    visualize(path_gen,visited)
    path_gen = path_gen.reverse