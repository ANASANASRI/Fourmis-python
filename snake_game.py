###########################################################
#                          Snake                          #
###########################################################


## Libraries
import pygame
import random


## Colors & Parameters
## Colors
YELLOW  = (255, 255, 0)
GREEN   = (34,139,34)
WHITE   = (255,255,255)
GRAY    = (128,128,128)
RED     = (255, 100, 50)
OLIVE   = (128, 128, 0)
LIME    = (0, 255, 0)
AQUA    = (0, 255, 255)
TEAL    = (0, 128, 128)
FUCHSIA = (255, 0, 255)
PURPLE  = (128, 0, 128)
BLACK   = (0, 0, 0)
Food_colors = [WHITE, RED, RED]

## Dimesnions
w  = 800 # the width of the grid
h  = 500 # the height of the grid
rw = 20  # the width of cells of the grid
rh = 20  # the height of cells of the grid


## Class Food
class Food(object):
    
    def __init__(self, color:tuple=RED):
        self.x = rw * random.randint(0, w//rw - 1)
        self.y = rh * random.randint(0, h//rh - 1)
        self.color = color
        self.colors = Food_colors
        
    def update(self):
        """update the position of the Food"""
        self.x = rw * random.randint(0, w//rw - 1)
        self.y = rh * random.randint(0, h//rh - 1)        
    
    def draw(self, screen):
        """draw the food on the screen"""
        self.color = random.choice(self.colors)
        pygame.draw.rect(screen, self.color, (self.x, self.y, rw, rh))


## Class Snake
class Snake:
    def __init__(self, x:int=0, y:int=0, body_color:tuple=AQUA, head_color:tuple=YELLOW):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.lenght = 1
        self.body = [[x, y]]
        self.body_color = body_color
        self.head_color = head_color
        self.food_pos = 0
        
    def update(self):
        """update the postion of the snake"""
        self.x += self.vx
        self.y += self.vy
        self.body.append([self.x, self.y])
        if len(self.body) > self.lenght:
            self.body = self.body[1:]
        self.food_pos += 1

    def move(self, event:pygame.event):
        """move the snake using keys"""
        if event.key == pygame.K_LEFT:
            self.vx = -rw
            self.vy = 0
        elif event.key == pygame.K_RIGHT:
            self.vx = rw
            self.vy = 0
        elif event.key == pygame.K_UP:
            self.vx = 0
            self.vy = -rh
        elif event.key == pygame.K_DOWN:
            self.vx = 0
            self.vy = rh
            
    def check_contact(self) -> bool:
        body_contact = any([self.body[-1] == cube for cube in self.body[:-1]])
        edge_contact = any([self.x < 0, self.x + rw > w, self.y < 0, self.y + rh > h])
        return body_contact or edge_contact
    
    def eat_food(self, food:Food) -> bool:
        x_contact = food.x < self.body[-1][0] + 1 < food.x + rw
        y_contact = food.y < self.body[-1][1] + 1 < food.y + rh
        return x_contact and y_contact

    def draw(self, screen):
        """draw the snake on the screen"""
        head = self.body[-1]
        pygame.draw.rect(screen, self.head_color, ((head[0] + 1, head[-1] + 1, rw - 1, rh - 1)))
        for cube in self.body[:-1]:
            pygame.draw.rect(screen, self.body_color, (cube[0] + 1, cube[-1] + 1, rw - 1, rh - 1)) 
        if self.food_pos < self.lenght:
            food = self.body[-self.food_pos]
            pygame.draw.rect(screen, self.food_color, ((food[0] - 1, food[-1] - 1, rw + 2, rh + 2)))


## Main function
def main():
    pygame.init()
    screen=pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    font1 = pygame.font.SysFont('Arial', 18)
    font2 = pygame.font.SysFont('Decorative', 60)
    
    ## image & sons
    land = pygame.image.load(r'terrain.jpg')
    land = pygame.transform.scale(land, (w, h))
    #contact = pygame.mixer.Sound('accident1.wav')
    #eat = pygame.mixer.Sound('eat.wav')
    
    ## create new snake & food
    snake = Snake()
    food = Food()
    
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                snake.move(event)

        ## update the screen
        screen.blit(land, (0, 0))
        snake.update()
        snake.draw(screen)
        food.draw(screen)
        
        ## check contact between snake and egdes 
        if snake.check_contact():
            #contact.play()
            text1 = font2.render('Game Over', True, WHITE)   
            text2 = font2.render(f'Your score is : {snake.lenght - 1}', True, WHITE)   
            screen.blit(text1,(w//3, h//3))
            screen.blit(text2,(w//4, h//2))
            pygame.display.update()
            pygame.time.wait(2000)
            snake = Snake()
            food = Food()
        
        ## check contact between snake and food
        if snake.eat_food(food):
            #eat.play()
            snake.food_color = food.color
            snake.food_pos = 0
            snake.lenght += 1
            food.update()        
        
        ## update score text
        text = font1.render(f'score : {snake.lenght - 1}', True, WHITE)   
        screen.blit(text,(w - 5*rw, rh))
        
        pygame.display.update()
        clock.tick(10)
        

if __name__ == '__main__':
    main()
