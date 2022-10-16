import pygame
screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

output = []
BACKGROUND_SURF = pygame.Surface((1920,1080))
BACKGROUND_SURF.fill((0,0,0))
mouse_releaced = False

pygame.init()
FPS = 60
menu_open = False

detail = True
input_alpha = False

fnt = pygame.font.Font(None,90)
pause_surf = fnt.render("Paused",True,(250,250,250))
pause_rect = pause_surf.get_rect(center = (960,450))

class cell_pointer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("Textures/Pointer.png")
        self.image = pygame.transform.scale(self.image,(104,184))
        self.rect = self.image.get_rect(midtop = (960,350))

def load_file() -> None:
    global brainfuck,cells_pos,cells_neg
    with open("brainfuck.txt","r") as f:
        brainfuck = [i for i in list(f.read()) if i in ["+","-","<",">","[", "]" , "," ,"."]]
    cells_pos = [0]
    cells_neg = [0]

load_file()

menu_lib = {
    0:"Resume",
    1:"Detail : True",
    2:"FPS : 60",
    3:"Exit"
}

function_lib = {
    0:"resume()",
    1:"change_detail()",
    2:"change_fps()",
    3:"close()"
}

current_fps = 0
fps_s = [60,120,144,160,240,1000]

def resume():
    global menu_open
    menu_open = False

def change_detail():
    global detail
    if menu_lib[1][9:] == "True":
        menu_lib[1] = "Detail : False"
        detail = False
    else:
        menu_lib[1] = "Detail : True"
        detail = True

def change_fps():
    global FPS,current_fps
    current_fps += 1
    if current_fps == 6: current_fps = 0
    FPS = fps_s[current_fps]
    menu_lib[2] = menu_lib[2][:6] + str(fps_s[current_fps])



def close():
    pygame.quit()
    exit()

class menu_item(pygame.sprite.Sprite):
    def __init__(self,num) -> None:
        super().__init__()
        self.image = pygame.Surface((300,50))
        self.image.fill((200,200,200))

        self.num = num
        self.rect = self.image.get_rect(center = (960,540 + 100 * num))
        self.fnt = pygame.font.Font(None,20)

    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((100,100,100))
            if mouse_releaced:
                exec(function_lib[self.num])
        else:
            self.image.fill((200,200,200))

        self.fnt_surf = self.fnt.render(menu_lib[self.num],True,(255,255,255))
        self.fnt_rect = self.fnt_surf.get_rect(center = (self.rect.width // 2, self.rect.height // 2))
        self.image.blit(self.fnt_surf,self.fnt_rect)

Menu = pygame.sprite.Group(menu_item(0),menu_item(1),menu_item(2),menu_item(3))

class instruction_pointer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((110,110),pygame.SRCALPHA)
        self.image.fill((255,255,0,100))
        self.rect = self.image.get_rect(topleft = (0,0))

Instruction_pointer = pygame.sprite.GroupSingle(instruction_pointer())
Cell_pointer = pygame.sprite.GroupSingle(cell_pointer())

texture_lib = {
    "+" : "Textures/Plus.png",
    "-" : "Textures/Minus.png",
    "<" : "Textures/Left.png",
    ">" : "Textures/Right.png",
    "[" : "Textures/Open.png",
    "]" : "Textures/Close.png",
    "," : "Textures/Comma.png",
    "." : "Textures/Dot.png"
}

class cell(pygame.sprite.Sprite):
    def __init__(self,pos,num,instruction:bool) -> None:
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.rect = self.image.get_rect(topleft = pos)

        self.image.fill((200,200,200))
        self.fnt = pygame.font.Font(None,32)
        disp_num = leftmost_cell if not instruction else leftmost_instruction

        if instruction:
            if len(brainfuck) <= disp_num + num:
                self.image.fill((200,200,200))

                return None

            img = pygame.image.load(texture_lib[brainfuck[disp_num + num]])
            self.image = pygame.transform.scale(img,(100,100))
        else:
            val = disp_num + num
            
            if val < 0:
                if abs(val) >= len(cells_neg):
                    val = "0"
                    cells_neg.append(0)
                else:val = str(cells_neg[abs(val)])
            else:
                if val >= len(cells_pos):
                    val = "0"
                    cells_pos.append(0)
                else: val = str(cells_pos[val])
            
            txt_surf = self.fnt.render(val,True,(0,0,0))
            w,h = txt_surf.get_width(),txt_surf.get_height()
            x,y = self.rect.width,self.rect.height
            pos = (x//2 - w//2, y//2 - h//2)

            self.image.blit(txt_surf,(pos))
        

        self.txt_surf = self.fnt.render(str(disp_num + num),True,(0,0,0))
        self.image.blit(self.txt_surf,(0,0))

current_cell = 0
leftmost_cell = -9
leftmost_cell_xpos = -35

leftmost_instruction = 0
leftmost_instruction_xpos = 5


def update_cells() -> None:
    global Cell_array,leftmost_cell_xpos,leftmost_cell
    if leftmost_cell_xpos + 100 <= 0:
        leftmost_cell_xpos += 105
        leftmost_cell += 1

    arr1 = [cell((leftmost_cell_xpos + (i * 105),540),i,False) for i in range(20)]
    

    if arr1[-1].rect.left >= 1920:
        leftmost_cell_xpos -= 105
        leftmost_cell -= 1

    Cell_array = pygame.sprite.Group(arr1)

def update_instructions() -> None:
    global Instruction_array,leftmost_instruction_xpos,leftmost_instruction

    if leftmost_instruction_xpos + 100 <= 0:
        leftmost_instruction_xpos += 105
        leftmost_instruction += 1

    arr2 = [cell((leftmost_instruction_xpos + (i * 105),5),i,True) for i in range(20)]

    if arr2[-1].rect.left >= 1920:
        leftmost_instruction_xpos -= 105
        leftmost_instruction -= 1

    Instruction_array = pygame.sprite.Group(arr2)

def move_cells(mov) -> None:
    global leftmost_cell_xpos,current_cell

    if detail:
        for i in range(10):
            leftmost_cell_xpos += mov

            update_cells()
            render()
            clock.tick(FPS)

        if mov > 0:
            leftmost_cell_xpos += 5
        if mov < 0:
            leftmost_cell_xpos -= 5

        update_cells()
    else:
        leftmost_cell_xpos += mov * 10

        if mov > 0:
            leftmost_cell_xpos += 5
        if mov < 0:
            leftmost_cell_xpos -= 5

def move_instructions(mov):
    global leftmost_instruction_xpos,leftmost_instruction,instruction_pos

    if detail:
        if mov > 0:bound = 8
        else: bound = 7
        if instruction_pos <= bound:
            if mov > 0:
                instruction_pos -= 1

                for i in range(10):
                    Instruction_pointer.sprites()[0].rect.left -= 10

                    render()
                    clock.tick(FPS)

                Instruction_pointer.sprites()[0].rect.left -= 5
        
            else:
                instruction_pos += 1

                for i in range(10):
                    Instruction_pointer.sprites()[0].rect.left += 10

                    render()
                    clock.tick(FPS)
                
                Instruction_pointer.sprites()[0].rect.left += 5
            
            return None

        for i in range(10):
            leftmost_instruction_xpos += mov

            update_instructions()
            render()
            clock.tick(FPS)

        if mov > 0:
            leftmost_instruction_xpos += 5
            instruction_pos -= 1
        if mov < 0:
            leftmost_instruction_xpos -= 5
            instruction_pos += 1
        
        update_instructions()
        render()
    else:
        if mov > 0: bound = 8
        else: bound = 7
        if instruction_pos <= bound:
            if mov > 0:
                instruction_pos -= 1
                Instruction_pointer.sprites()[0].rect.left -= 105
            else:
                instruction_pos += 1
                Instruction_pointer.sprites()[0].rect.left += 105
            
            return None
        
        leftmost_instruction_xpos += mov * 10

        if mov > 0:
            leftmost_instruction_xpos += 5
            instruction_pos -= 1
        if mov < 0:
            leftmost_instruction_xpos -= 5
            instruction_pos += 1
        
        update_instructions()
        render()

update_cells()
update_instructions()

def get_input():
    num = "Input -> "
    fnt = pygame.font.Font(None,30)
    fnt_surf = fnt.render(num,True,(200,200,200))
    fnt_rect = fnt_surf.get_rect(center = (960,540))

    bg = pygame.surface.Surface((1920,1080))
    bg.fill((0,0,0))

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if input_alpha:
                    num += str(event.key)
                    fnt_surf = fnt.render(num,True,(200,200,200))
                    fnt_rect = fnt_surf.get_rect(center = (960,540))

                elif chr(event.key).isnumeric():
                    num += chr(event.key)
                    fnt_surf = fnt.render(num,True,(200,200,200))
                    fnt_rect = fnt_surf.get_rect(center = (960,540))
                
                if event.key == pygame.K_RETURN:
                    if input_alpha: num = num[:-2]
                    if current_cell >= 0:
                        cells_pos[current_cell] = int("".join(num[8:]))
                    else:
                        cells_neg[abs(current_cell) - 1] = int("".join(num[8:]))
                    
                    return None
        
        screen.blit(bg,(0,0))
        screen.blit(fnt_surf,fnt_rect)
        pygame.display.update()
        clock.tick(FPS)


def render() -> None:
    screen.blit(BACKGROUND_SURF,(0,0))

    if menu_open:
        Menu.draw(screen)
        screen.blit(pause_surf,pause_rect)
    else:
        Cell_array.draw(screen)
        Instruction_array.draw(screen)
        Cell_pointer.draw(screen)
        Instruction_pointer.draw(screen)
        Terminal.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

def move_to_open() -> None:
    global instruction_pos,leftmost_instruction_xpos

    current = 1
    while brainfuck[instruction_pos] != "[" or current != 0:
        move_instructions(10)
        if brainfuck[instruction_pos] == "]":
            current += 1
        if brainfuck[instruction_pos] == "[":
            current -= 1
    
def move_to_closed() -> None:
    global instruction_pos,leftmost_instruction_xpos
    
    current = 1
    while brainfuck[instruction_pos] != "]" or current != 0:
        move_instructions(-10)

        if brainfuck[instruction_pos] == "]":
            current -= 1
        if brainfuck[instruction_pos] == "[":
            current += 1

class terminal(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.fnt = pygame.font.Font(None,25)
        self.update_text()
    
    def update_text(self) -> None:
        txt = "".join(output).split("\n")

        surfs = []
        rects = []
        for i in range(len(txt)):
            surf = self.fnt.render(txt[i],True,(255,255,255))
            rect = surf.get_rect(topleft = (0,i * 25))

            surfs.append(surf)
            rects.append(rect)

        width = max([i.width for i in rects])
        height = sum([i.height for i in rects])

        self.image = pygame.Surface((width,height))
        self.image.fill((100,100,100))

        for i in range(len(txt)):
            self.image.blit(surfs[i],rects[i])

        self.rect = self.image.get_rect(center = (960,810))

        
Terminal = pygame.sprite.GroupSingle(terminal())

instruction_pos = 0
while True:
    mouse_releaced = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_releaced = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                menu_open = True if not menu_open else False

            if event.key == pygame.K_RIGHT:
                move_cells(-10)
                move_instructions(-10)
            
            if event.key == pygame.K_LEFT:
                move_cells(10)
                move_instructions(10)
        
    if instruction_pos < len(brainfuck) and not menu_open:
        instruction = brainfuck[instruction_pos]

        if instruction == "<":
            move_cells(10)
            current_cell -= 1

        if instruction == ">":
            move_cells(-10)
            current_cell += 1

        if instruction in ["+","-"]:
            i = 1 if instruction == "+" else -1
            if current_cell >= 0 :
                cells_pos[current_cell] += i

                if cells_pos[current_cell] == -1:cells_pos[current_cell] = 255
                if cells_pos[current_cell] == 256:cells_pos[current_cell] = 0
            else:
                cells_neg[abs(current_cell) - 1] += i

                if cells_neg[abs(current_cell) - 1] == -1: cells_neg[abs(current_cell) - 1] = 255
                if cells_neg[abs(current_cell) - 1] == 256: cells_neg[abs(current_cell) - 1] = 0

        
        if instruction == ".":
            
            if current_cell >= 0:
                output.append(chr(cells_pos[current_cell]))
            else:
                output.append(chr(cells_neg[abs(current_cell) - 1]))
            
            Terminal.sprites()[0].update_text()

        if instruction == "[":
            if current_cell >= 0 and cells_pos[current_cell] == 0:
                move_to_closed()
                

            elif current_cell <= -1 and cells_neg[abs(current_cell) - 1] == 0:
                move_to_closed()

        if instruction == "]":
            if current_cell >= 0 and cells_pos[current_cell] != 0:
                move_to_open()

            elif current_cell <= -1 and cells_neg[abs(current_cell) - 1] != 0:
                move_to_open()
                
        if instruction == ',':
            get_input()
        
        update_cells()
        move_instructions(-10)
        update_instructions()

    if menu_open:
        [sprite.update() for sprite in Menu.sprites()]

    render()
    clock.tick(FPS)
