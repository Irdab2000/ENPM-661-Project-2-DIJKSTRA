#!/usr/bin/python3
import pygame

def gen_obstacles():
    # Initialize Pygame
    #pygame.init()

    # Set the window dimensions
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 250

    # # Create the Pygame window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Obstacle Course")

    # # Define the colors
    BACKGROUND_COLOR = pygame.Color("red")
    OBSTACLE_COLOR = pygame.Color("black")
    CLEARANCE_COLOR = pygame.Color("white")

    # # Create the window for the obstacle course
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    # # Fill the surface with the background color
    surface.fill(BACKGROUND_COLOR)

    # # Blit the surface onto the Pygame window
    
    #window.blit(surface, (0, 0))
    occupied_coords = []
    free_coords = []
    clearance_coords = []
    for x in range(0,WINDOW_WIDTH): #Getting coordinates using half planes and semi algebraic models
        for y in range(0, WINDOW_HEIGHT):
            if(x>=95 and x<=155 and y>= 140 and y<=250):                    
                 clearance_coords.append([x,y])
                 #pygame.draw.rect(surface, CLEARANCE_COLOR, (x, y ,1,1))
                 if(x>=100 and x<=150 and y>=145 and y<=245):
                    occupied_coords.append([x,y])
                    #pygame.draw.rect(surface, OBSTACLE_COLOR, (x, y,1 ,1))                     
                              #Getting obstacle and free coordinates
            elif(x>=95 and x<=155 and y>=0 and y<=110):
                 clearance_coords.append([x,y])
                 if(x>=100 and x<=150 and y>=5 and y<=105):
                     occupied_coords.append([x,y])
            else:
                flag_clearance = check_if_in_triangle(x,y,300,45,231,87,369,87)
                if(flag_clearance):
                    clearance_coords.append([x,y])
                    flag_obstacle = check_if_in_triangle(x,y,300,50,235,87,365,87)
                    if(flag_obstacle):
                        occupied_coords.append([x,y])
                flag_clearance = check_if_in_triangle(x,y,300,205,231,162,369,162)
                if(flag_clearance):
                    clearance_coords.append([x,y])
                    flag_obstacle = check_if_in_triangle(x,y,300,200,235,162,365,162)
                    if(flag_obstacle):
                        occupied_coords.append([x,y])
                if(x>=231 and x<=369 and y>=87 and y<=162):
                    clearance_coords.append([x,y])
                    if(x>=235 and x<=365 and y>=87 and y<=162):
                        occupied_coords.append([x,y])
                flag_clearance = check_if_in_triangle(x,y,457,237,457,13,515,125)
                if(flag_clearance):
                    clearance_coords.append([x,y])
                    flag_obstacle = check_if_in_triangle(x,y,460,225,460,25,510,125)
                    if(flag_obstacle):
                        occupied_coords.append([x,y])
                if([x,y] not in clearance_coords):
                    free_coords.append([x,y])

    for [x,y] in clearance_coords:
        pygame.draw.rect(surface, CLEARANCE_COLOR, (x, y,1 ,1))
        window.blit(surface, (0, 0))                                           #Using the coordinates to display the generated map.
        pygame.display.update()
    for [x,y] in occupied_coords:
        pygame.draw.rect(surface,OBSTACLE_COLOR,(x,y,1,1))
        window.blit(surface, (0, 0))
        pygame.display.update()
    #print(free_coords[0])
    #print(occupied_coords[0])

    pygame.quit()
    print(free_coords[0],free_coords[-1])

    return free_coords,clearance_coords

def check_if_in_triangle(x,y,x1,y1,x2,y2,x3,y3): #Functon that checks if a given point is inside the triangle made using three vertices [x1,y1],[x2,y2],[x3,y3]
    area = 0.5 * abs((x1 * y2 + x2 * y3 + x3 * y1) - (x2 * y1 + x3 * y2 + x1 * y3))
    area1 = 0.5 * abs((x * y2 + x2 * y3 + x3 * y) - (x2 * y + x3 * y2 + x * y3))
    area2 = 0.5 * abs((x1 * y + x * y3 + x3 * y1) - (x * y1 + x3 * y + x1 * y3))
    area3 = 0.5 * abs((x1 * y2 + x2 * y + x * y1) - (x2 * y1 + x * y2 + x1 * y))

    # Calculate the barycentric coordinates
    alpha = area1 / area
    beta = area2 / area
    gamma = area3 / area

    # Check if the point is inside the triangle
    if abs(alpha + beta + gamma - 1) < 0.00001:
        return True
    else:
        return False


if __name__ == "__main__":
    occupied_coords = gen_obstacles()