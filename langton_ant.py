#########################################################################################################
#                                               Langton's ant                                           #
#########################################################################################################

## Rules
# > At a white square, turn 90° clockwise, flip the color of the square, move forward one unit
# > At a black square, turn 90° counter-clockwise, flip the color of the square, move forward one unit


## Libraries
import pygame
import numpy as np



## Parameters and colors
## Dimensions of the grid
w  = 800  # the width of the grid
h  = 500  # the height of the grid
rw = 5    # the width of the cells of the grid
rh = 5    # the height of the cells of the grid

## Colors
GREEN = (34,139,34)
WHITE = (255,255,255)
GRAY = (128,128,128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (28,128,130)



## The Grid Class
class Grid(object):
    
    def __init__(self, w:int=w, h:int=h, rw:int=rw, rh:int=rh, c:tuple=GRAY):
        self.w     = w  # the width of the grid
        self.h     = h  # the height of the grid
        self.rw    = rw # the width of the cells
        self.rh    = rh # the height of the cells
        self.color = c  # the color of the grid lines
        self.create_grid() # create the grid
        
        
    def create_grid(self):
        """create a numpy array which represente the grid"""
        self.grid = np.zeros((self.h // self.rh, self.w // self.rw)).astype('int')
        
    def draw_grid(self, screen:pygame.display.set_mode):
        """draw a grid on the screen with the given dimensions"""
        ## draw the vertical lines
        for i in range(self.w // self.rw + 1):
            pygame.draw.lines(screen, self.color, False, [(i * self.rh, 0), (i * self.rh, self.h)], 1)

        ## draw the horizontal lines
        for i in range(h // rh + 1):
            pygame.draw.lines(screen, self.color, False, [(0, i * self.rw), (self.w, i * self.rw)], 1)
            
            
    def draw_cell(self, screen:pygame.display.set_mode, i:int, j:int):
        """update the color of the cell (i, j)"""
        
        ## 1 for black color 0 for white
        if self.grid[i, j] == 1:
            cell_color = BLACK
        else:
            cell_color = WHITE
        pygame.draw.rect(screen, cell_color, (j*self.rw + 1, i*self.rh + 1, rw - 1, rh - 1))




## The Ant Class
class Ant(object):
    
    def __init__(self, x:int, y:int, vx:int=0, vy:int=1, c:tuple=RED):
        self.x     = x  # the x coordinate of the ant
        self.y     = y  # the y coordiante of the ant
        self.vx    = vx # the x velocity of the ant
        self.vy    = vy # the y velocity of the ant
        self.color = c  # the color of the ant
        self.step  = 0  # the number of steps that the ant has done
        
        
    def update_cell(self, grid:Grid):
        """update the color of the cell on which the ant is standing"""
        
        ## getting the number of the cell on which the ant is on
        i = int(self.y // grid.rh) % grid.grid.shape[0]
        j = int(self.x // grid.rw) % grid.grid.shape[1]
        
        ## getting the color of the cell on which the ant is on
        cell = grid.grid[i, j]
        
        ## if the color of the cell is black turn 90° counter-clockwise
        if cell == 1:
            self.vx, self.vy = self.vy, -self.vx
            cell = 0
            
        ## if the color of the cell is white turn 90° clockwise
        else:
            self.vy, self.vx = self.vx, -self.vy
            cell = 1
           
        ## switching the value of the cell to the new value
        grid.grid[i, j] = cell
        
        
    def update(self, grid:Grid):
        """update the postion of the ant"""
        
        self.x += self.vx * grid.rw
        self.y += self.vy * grid.rh
        self.step += 1
        
    def draw(self, screen:pygame.display.set_mode):
        """draw the ant on the screen"""
        
        self.x = rw * (self.x // rw)
        self.y = rh * (self.y // rh)
        pygame.draw.rect(screen, self.color, (self.x + 1, self.y + 1, rw - 1, rh - 1))


## The main function 
def main():
    pygame.init()
    
    ## initiating the screen
    screen = pygame.display.set_mode((w, h + 50))
    pygame.display.set_caption('Ants')
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    
    ## create the ant
    ant = Ant(x=w//2- rw, y=h//2 - rh)
    
    ## create the grid
    grid = Grid()
    grid.draw_grid(screen)
    ant.draw(screen)
    
    ##  adding text to the screen
    font = pygame.font.SysFont('Arial', 18)
    
    start_text = "press SPACE to start or to pause"
    counter_text = f'step : {ant.step}'
    text1 = font.render(start_text, True, BLACK)
    text2 = font.render(counter_text, True, BLACK)
    screen.blit(text1, (10, h + 2))
    screen.blit(text2, (w - 120, h + 2))
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONUP:
                point = pygame.mouse.get_pos()
                (i, j) = (point[1] // grid.rw, point[0] // grid.rh)
                grid.grid[i, j] = int(not grid.grid[i, j])
                grid.draw_cell(screen, i, j)
                ant.draw(screen)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulate = True
                    while simulate:
                        ant.update_cell(grid)
                        (i, j) = int(ant.y // grid.rw) % grid.grid.shape[0], int(ant.x // grid.rh) % grid.grid.shape[1]
                        grid.draw_cell(screen, i, j)
                        ant.update(grid)
                        ant.draw(screen)
                        counter_text = f'step : {ant.step}'
                        text4 = font.render(counter_text, True, BLACK)
                        pygame.draw.rect(screen, WHITE, (w-120, h+1, 120, 50))
                        screen.blit(text4, (w - 120, h + 2))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                simulate = False
                                running  = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    simulate = not simulate
        pygame.display.update()

    pygame.quit()      


if __name__ == '__main__':
    main()
