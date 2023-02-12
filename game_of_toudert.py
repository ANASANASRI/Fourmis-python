###########################################################
#                    Game Of Life                         #
###########################################################

## Rules:
# >Any live cell with two or three live neighbours survives.
# >Any dead cell with three live neighbours becomes a live cell.
# >All other live cells die in the next generation. Similarly, all other dead cells stay dead.

## Liberaires
import pygame
import numpy as np


## Parameters and colors
## Dimensions of the grid
w  = 800  # the width of the grid
h  = 500  # the height of the grid
rw = 20    # the width of the cells of the grid
rh = 20    # the height of the cells of the grid

## Colors
GREEN = (34,139,34)
WHITE = (255,255,255)
GRAY  = (128,128,128)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE  = (28,128,130)


## Tha Grid Class
class Grid(object):
    
    def __init__(self, w:int=w, h:int=h, rw:int=rw, rh:int=rh, c:tuple=GRAY):
        self.w     = w  # the width of the grid
        self.h     = h  # the height of the grid
        self.rw    = rw # the width of the cells
        self.rh    = rh # the height of the cells
        self.color = c  # the color of the grid lines
        self.create_grid() # create the grid
        self.copy = self.create_copy()
        self.step = 0
        
        
    def create_grid(self):
        """create a numpy array which represente the grid"""
        self.grid = np.zeros((self.h // self.rh, self.w // self.rw)).astype('int')
        
    def create_copy(self):
        return self.grid.copy()
    
    def draw_grid(self, screen:pygame.display.set_mode):
        """draw a grid on the screen with the given dimensions"""
        ## draw the vertical lines
        for i in range(self.w // self.rw + 1):
            pygame.draw.lines(screen, self.color, False, [(i * self.rh, 0), (i * self.rh, self.h)], 1)

        ## draw the horizontal lines
        for i in range(h // rh + 1):
            pygame.draw.lines(screen, self.color, False, [(0, i * self.rw), (self.w, i * self.rw)], 1)
            
    def set_cell_number(self, i:int, j:int):
        self.grid[i, j] = int(not self.grid[i, j])
        
    def set_cell_color(self, i:int, j:int, screen):
        if self.grid[i, j]:
            color = BLACK
        else:
            color = WHITE
        pygame.draw.rect(screen, color, (j*self.rw + 1, i*self.rh + 1, self.rw - 1, self.rh - 1))
        
    
    def update_cell(self, x:np.float, y:np.float, screen):
        (i, j) = (y // self.rw, x // self.rh)
        self.grid[i, j] = int(not self.grid[i, j])
        self.set_cell_color(i, j,screen)
        
    def random_schema(self, screen:pygame.display.set_mode, n:int):
        r1 = np.random.randint(0, self.grid.shape[0], n)
        r2 = np.random.randint(0, self.grid.shape[1], n)
        self.grid[r1, r2] = 1
        self.draw_cells(screen)
        
    def update(self):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                nb_neighbours = self.number_of_alive_neighbours(i, j)
                if self.grid[i, j]:
                    if nb_neighbours < 2 or nb_neighbours > 3:
                        self.copy[i, j] = 0
                else:
                    if nb_neighbours == 3:
                        self.copy[i, j] = 1.
        self.step += 1
            
    def number_of_alive_neighbours(self, i:int, j:int)->int:
        i_min, i_max = np.max([0, i - 1]), np.min([self.grid.shape[0], i + 2])
        j_min, j_max = np.max([0, j - 1]), np.min([self.grid.shape[1], j + 2])
        sub_grid = self.grid[i_min:i_max, j_min:j_max]
        bool_grid = sub_grid[sub_grid == 1.]
        return bool_grid.shape[0] - self.grid[i, j]
    
    def draw_cells(self, screen:pygame.display.set_mode):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.set_cell_color(i, j, screen)
        
    def update_cells_color(self, screen:pygame.display.set_mode):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.copy[i, j] == 1 and self.grid[i, j] != 1:    
                    color = RED
                elif self.copy[i, j] == 1:
                    color = BLACK
                elif self.copy[i, j] == 0:
                    color = WHITE
                pygame.draw.rect(screen, color, (j*self.rw + 1, i*self.rh + 1, self.rw - 1, self.rh - 1))                    


## The main function
def main():
    pygame.init()
    screen = pygame.display.set_mode([w, h + 50])
    screen.fill(WHITE)
    pygame.display.set_caption('Game Of Life')
    clock = pygame.time.Clock()
    
    grid = Grid()
    grid.draw_grid(screen)
    font = pygame.font.SysFont('Arial', 18)
    counter_text = f'step : {grid.step}'
    text2 = font.render(counter_text, True, BLACK)
    text = font.render('space:start(pause) n:new r:random', True, BLACK)   
    screen.blit(text,(10, h + 5))
    screen.blit(text2, (w - 120, h + 2))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                (x, y) = pygame.mouse.get_pos()
                grid.update_cell(x, y, screen)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid.random_schema(screen, n=w//rw)
                    
                elif event.key ==pygame.K_SPACE:
                    simulate = True            
                    while simulate:
                        grid.copy = grid.create_copy()
                        grid.update()
                        grid.update_cells_color(screen)
                        
                        if (grid.grid == grid.copy).all():
                            simulate = False
                        
                        grid.grid = grid.copy
                        counter_text = f'step : {grid.step}'
                        text2 = font.render(counter_text, True, BLACK)
                        pygame.draw.rect(screen, WHITE, (w-120, h+1, 120, 50))
                        screen.blit(text2, (w - 120, h + 2))
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                
                            elif event.type == pygame.MOUSEBUTTONUP:
                                (x, y) = pygame.mouse.get_pos()
                                grid.update_cell(x, y, screen)
                                
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_n:
                                    grid.create_grid()
                                    grid.step = 0
                                    simulate = False
                                    
                                elif event.key ==pygame.K_SPACE:
                                    simulate = not simulate
                               
                        pygame.display.update()
                        clock.tick(10)
            pygame.display.update()
            
    pygame.quit()


if __name__ == '__main__':
    main()
