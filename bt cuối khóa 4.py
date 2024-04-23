import pygame, time
from random import *
from pygame import mixer


pygame.init()

#Khai báo màu
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
GREY = (210, 210 ,210)
GRAY = (128,128,128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

#tạo cửa sổ
WIDTH = 432
HEIGHT = 512

cuaso = pygame.display.set_mode((WIDTH, HEIGHT)) #2 dấu ngoặc
pygame.display.set_caption('Flappy Bird')

icon = pygame.image.load(r'D:\bt python 4\mk.png') #nếu không có r thì đổi thành dấu /
pygame.display.set_icon(icon)

fps = 30
clock = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/background-day.png'), (432,768))
base = pygame.transform.scale2x(pygame.image.load(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/base.png'))

#_________________BACKGROUND_____________
class Background():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 3

    def show(self):
        cuaso.blit(self.image, (self.x, self.y))
        cuaso.blit(self.image, (self.x + self.width, self.y))

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x += self.width
        

    
    
#______________Tạo bird_________
bird_die = pygame.image.load(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/12.png')
Bird_die = pygame.transform.rotate(bird_die,270)
class Bird(pygame.sprite.Sprite):
    lst_anh = []
    for i in range(1,4):
        lst_anh.append(pygame.image.load(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/1' + str(i) + '.png'))

    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.count = 0
        self.surf = self.lst_anh[self.count]
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
        self.speed = 0
        self.gravity = 0.5
        self.flyspeed = -5
        self.diefall = False
        self.angle = 20

    def show(self):
        self.surf = self.lst_anh[self.count]
        self.count += 1
        if self.count == len(self.lst_anh):
            self.count = 0

        #cuaso.blit(self.surf, self.rect)

    def update(self):
        #công thức tính gia tốc: y = y0 + V0*t + 0.5gt**2. Coi t = 1 => y = y0 + 0.5G
        self.rect.y += self.speed + 0.5*self.gravity
        self.speed += self.gravity


        if self.rect.y < 0:
            self.rect.y = 0

        if mousedown == True:
            self.angle = 20
            self.speed = self.flyspeed
            cuaso.blit(pygame.transform.rotate(self.surf, 20), self.rect)
            pygame.mixer.music.load('flappy_bird_library/audio/wing.ogg')
            pygame.mixer.music.play(0)

        self.angle -= 1
        if self.angle < -20:
            self.angle = -20
        cuaso.blit(pygame.transform.rotate(self.surf, self.angle), self.rect)

        if self.diefall:            
            bird.rect.y = 600

    

#_____________Tạo cột_________________
blank = 106
xuoi = pygame.image.load('flappy_bird_library\sprites\pipe-green.png')
nguoc = pygame.transform.rotate(xuoi,180)
height = (pygame.image.load('flappy_bird_library\sprites\pipe-green.png').get_height())

class Cot(pygame.sprite.Sprite):
    def __init__(self, anh):
        super().__init__()
        self.x = 350       
        self.y = randrange(192,312,20)
        self.surf = anh
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
        
    def show(self):
        cuaso.blit(self.surf, self.rect)

    

score = 0
highscore = 0


#____________Xử lý cột______________

pipes = pygame.sprite.Group()
def Pipes():
    global pipes
    cot1 = Cot(xuoi)
    cot2 = Cot(nguoc)
    cot2.rect.y = cot1.y - blank - height    
    pipes.add(cot1, cot2)




def Xuly_Pipe():
    global  pipes, score, highscore
    #Score(score, highscore)
    for i in pipes:
        i.show()
        #cuaso.blit(i.surf, i.rect)
        i.rect.x -= 5
       
        if  i.rect.x < 50:
            i.kill()
            
        if bird.diefall == False:
            if   i.rect.x == bird.rect.x :
                score += 1/2
                pygame.mixer.music.load('flappy_bird_library/audio/point.ogg')
                pygame.mixer.music.play(0)



def reset():
    global bird, score, pipes
    bird = Bird(60,300)
    score = 0
    for i in pipes:
        i.kill()
        
    cotmoi =pygame.USEREVENT + 1
    Pipes()
    





#____________Xử lý Score, Highscore___________
    
#=======XỬ LÝ HIGHSCORE=======
f = open(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/highscore.txt', 'r', encoding = 'utf-8')
data = f.read()
f.close()
f1 = open(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/highscore.txt', 'r', encoding = 'utf-8')
data2 = f1.read()
f1.close()
data3 = data2.split('\n')
data4 = []
print(data3)
for i in data3:
    data4.append((i))
data4.sort()
data5 = []
data5.append(data4[-1])

if data == []:
    highscore = 0

else:
    highscore = data5[0]


           
def breakstreak():
    global score, highscore
    if int (score) >= int (highscore):
        highscore = score      
    font = pygame.font.SysFont('FVF Fernado 08', 30)
    text_highscore = font.render('Highscore: ', str(highscore), BLACK)
    cuaso.blit(text_highscore, (290, 20))
    


def Show_score():
    string_score = str(int(score)) 
    for i in range (len(string_score)):
        show = pygame.image.load('D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/' + string_score[i] + '.png')
        cuaso.blit(show, (200 - (len(string_score)//2-i)*25, 30))
        



#================= CHƯƠNG TRÌNH CHÍNH=======================
background = Background(0,0, bg)
baseground = Background(0,380, base)   
bird = Bird(60,300)
Pipes()
cotmoi = pygame.USEREVENT + 1
pygame.time.set_timer(cotmoi, 1000)
mousedown = False
run = True

while run:
    #cuaso.fill(WHITE)
    background.show()
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == cotmoi:
            Pipes()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True

        if event.type == pygame.MOUSEBUTTONUP:
            mousedown = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
        
    bird.show()
    bird.update()
    Xuly_Pipe()
    breakstreak()
   
    
        
    if pygame.sprite.spritecollideany(bird, pipes) or bird.rect.y > 380:
        pygame.mixer.music.load('flappy_bird_library/audio/hit.ogg')
        pygame.mixer.music.play(0)
        bird.diefall = True
        cotmoi = False
        font = pygame.font.SysFont('FVF Fernado 08', 40, 'bold')
        repeat_text = font.render('Press R to replay', True, RED, WHITE)
        cuaso.blit(repeat_text, (100,300))
        
        bangdiem = pygame.image.load(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/scoreboard.png')
        cuaso.blit(bangdiem, (100, 50))
        
        font = pygame.font.SysFont('FVF Fernado 08', 30)
        text_scoreboard = font.render(str(score), True, BLACK)
        cuaso.blit(text_scoreboard, (275, 155))

        text_highscoreboard = font.render(str(score), True, BLACK)
        cuaso.blit(text_highscoreboard, (275, 200))

        if score > int(data5[0]):
            f = open(r'D:/bt python 4/bt cuối khóa 4/flappy_bird_library/sprites/highscore.txt', 'a', encoding = 'utf-8')
            data1 = f.write('\n' + str(score))
            f.close()
            
    



    
    baseground.show()
    baseground.update()
    
    Show_score()
    pygame.display.update() 
pygame.quit()


#https://uoit.ca/forms/online/view.php?id=302334&mf_resume=5aa318f920



                                 


