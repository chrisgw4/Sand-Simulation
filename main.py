import pygame
import random


class Particle:
    def __init__(self, new_id, color):
        self.x = 0
        self.y = 0
        self.id = new_id
        self.velocity = 1
        self.rect = pygame.Rect(0,0,1,1)
        self.color = color
        self.free = False

        # self.rect = pygame.rect.Rect(left=0, top=0, width=1, height=1)
        # self.rect.x = self.x
        # self.rect.y = self.y
    def update(self, array, scale, particle_array):
        if self.free:
            if self in particle_array:
                particle_array.remove(self)
            array[self.y][self.x] = None
            del self
            return

        self.move_down(array,scale)
        self.check_down_left(array, scale)
        self.check_down_right(array, scale)

    # Returns True if something below, False if nothing is below
    def check_down(self, array):
        if self.y+1 < len(array):
            return array[self.y+1][self.x] is not None

    def check_down_type(self, array):
        if self.check_down(array):
            return array[self.y+1][self.x].id
        return -1


    def move_down(self, array, scale):
        farthest_fall = 0
        for x in range(self.y, self.y + self.velocity+1):

            if x < len(array)-1 and len(array[x]) > self.x >= 0:
                if array[x][self.x] is None: # Check nothing is below
                    farthest_fall = x

        if 0 < farthest_fall < len(array)-1:
            array[farthest_fall][self.x] = array[self.y][self.x]
            array[self.y][self.x] = None
            self.y = farthest_fall
            self.rect.x = self.x * scale
            self.rect.y = self.y * scale
            self.velocity += 1
            return True

        self.velocity = 1
        return False

    def check_up(self, array):
        if self.y - 1 >= 0:
            return array[self.y - 1][self.x] is not None

    def check_up_type(self, array):
        if self.check_up(array):
            return array[self.y-1][self.x].id
        return -1

    def check_down_left(self, array, scale):
        if self.y + 1 < len(array) and self.x-1 >= 0:
            if array[self.y+1][self.x-1] is None and self.check_down_type(array) != 1: # Check nothing is below
                if 0 < self.y+1 < len(array) and self.x-1 >= 0:
                    array[self.y+1][self.x-1] = array[self.y][self.x]
                    array[self.y][self.x] = None
                    self.y = self.y+1
                    self.x = self.x-1
                    self.rect.x = self.x * scale
                    self.rect.y = self.y * scale

    def check_down_right(self, array, scale):
        if self.y + 1 < len(array) and self.x+1 < len(array[self.y]):
            if array[self.y+1][self.x+1] is None and self.check_down_type(array) != 1 :  # Check nothing is below
                array[self.y+1][self.x+1] = array[self.y][self.x]

                array[self.y][self.x] = None
                self.y = self.y+1
                self.x = self.x+1
                self.rect.x = self.x * scale
                self.rect.y = self.y * scale
            # elif self.id == 0 and array[self.y+1][self.x+1] is not None and array[self.y+1][self.x+1].id != 0 and self.check_down_type(array) != 1:
            #     print("not None")
            #     farthest_fall = self.y+1
            #     move_val = 1
            #     while farthest_fall - move_val > 0 and array[farthest_fall - move_val][self.x+1] is not None:
            #         move_val += 1

                # if array[self.y+1][self.x+1] is not None:
                #     array[farthest_fall - move_val][self.x+1] = array[self.y+1][self.x+1]
                #     array[farthest_fall - move_val][self.x+1].y = farthest_fall - move_val
                #     array[farthest_fall - move_val][self.x+1].x = self.x
                #     array[self.y+1][self.x + 1] = None
                #
                # array[self.y+1][self.x+1] = array[self.y][self.x]
                # array[self.y][self.x] = None
                # self.y = self.y+1
                # self.x = self.x+1
                # self.rect.x = self.x * scale
                # self.rect.y = self.y * scale

    def check_left(self, array): # return true if something, return false if nothing
        if self.x-1 >= 0:
            return array[self.y][self.x-1] is not None

    def check_left_type(self, array):
        if self.check_left(array):
            return array[self.y][self.x-1].id
        return -1

    def move_left(self, array, scale):
        if self.x - 1 >= 0:
            if not self.check_left(array) and self.check_down(array):#(self.y == len(array)-1 or array[self.y+1][self.x] is not None):
                array[self.y][self.x-1] = array[self.y][self.x]
                array[self.y][self.x] = None
                self.y = self.y
                self.x = self.x-1
                self.rect.x = self.x * scale
                self.rect.y = self.y * scale
                return True
        return False

    def check_right(self, array): # return true if something, return false if nothing
        if self.x+1 < len(array[self.y]):
            return array[self.y][self.x+1] is not None

    def check_right_type(self, array):
        if self.check_right(array):
            return array[self.y][self.x+1].id
        return -1

    def move_right(self, array, scale):
        if self.x + 1 < len(array[self.y]):
            if not self.check_right(array) and self.check_down(array):#(len(array)-1 or array[self.y+1][self.x] is not None): # Check nothing is below
                array[self.y][self.x+1] = array[self.y][self.x]
                array[self.y][self.x] = None
                self.y = self.y
                self.x = self.x+1
                self.rect.x = self.x * scale
                self.rect.y = self.y * scale



class Sand(Particle):
    def __init__(self):
        super().__init__(new_id=0,color=pygame.Color(255,255,175,255))  # set id to 0 for sand

    def move_down(self, array, scale):
        farthest_fall = 0
        for x in range(self.y, self.y + self.velocity + 1):

            if x < len(array)-1 and self.x < len(array[x]) and self.x >= 0:
                if array[x][self.x] is None or array[x][self.x].id != 0:  # Check nothing is below
                    farthest_fall = x

        if farthest_fall > 0 and farthest_fall < len(array)-1:
            if array[farthest_fall][self.x] is not None:
                # particle_array.remove(array[farthest_fall][self.x])
                move_val = 1
                while farthest_fall-move_val > 0 and array[farthest_fall-move_val][self.x] is not None:
                    move_val += 1
                array[farthest_fall-move_val][self.x] = array[farthest_fall][self.x]
                array[farthest_fall-move_val][self.x].y = farthest_fall-move_val
                array[farthest_fall - move_val][self.x].x = self.x
                array[farthest_fall][self.x] = None
            array[farthest_fall][self.x] = array[self.y][self.x]
            array[self.y][self.x] = None
            self.y = farthest_fall
            self.rect.x = self.x * scale
            self.rect.y = self.y * scale
            self.velocity += 1
            return True

        self.velocity = 1
        return False

    # def check_down_left(self, array, scale):
    #     if self.y + 1 < len(array) and self.x-1 >= 0:
    #         if (array[self.y+1][self.x-1] is None or (array[self.y+1][self.x-1] is not None and array[self.y+1][self.x-1].id == 1)) and array[self.y+1][self.x] is not None: # Check nothing is below
    #             array[self.y+1][self.x-1] = array[self.y][self.x]
    #             array[self.y][self.x] = None
    #             self.y = self.y+1
    #             self.x = self.x-1
    #             self.rect.x = self.x * scale
    #             self.rect.y = self.y * scale
    #
    # def check_down_right(self, array, scale):
    #     if self.y + 1 < len(array) and self.x+1 < len(array[self.y]):
    #         if (array[self.y+1][self.x+1] is None or (array[self.y+1][self.x+1] is not None and array[self.y+1][self.x+1].id == 1)) and array[self.y+1][self.x] is not None: # Check nothing is below
    #             array[self.y+1][self.x+1] = array[self.y][self.x]
    #             array[self.y][self.x] = None
    #             self.y = self.y+1
    #             self.x = self.x+1
    #             self.rect.x = self.x * scale
    #             self.rect.y = self.y * scale

class Water(Particle):
    def __init__(self):
        super().__init__(new_id=1,color=pygame.Color(0,0,255,255))  # set id to 1 for water

    def update(self, array, scale, particle_array):
        if self.free:
            if self in particle_array:
                particle_array.remove(self)
            array[self.y][self.x] = None
            del self
            return


        self.dissolve_sand(array, scale, particle_array)
        self.decay_self(array, particle_array)
        self.interact_lava(array, scale, particle_array)

        self.move_down(array, scale)

        #if self.check_down(array):
            # self.check_down_left(array, scale)
            # self.check_down_right(array, scale)
        if not self.move_left(array, scale):
            self.move_right(array, scale)

    def move_down(self, array, scale):
        farthest_fall = 0
        for x in range(self.y, self.y + self.velocity + 1):

            if x < len(array)-1 and self.x < len(array[x]) and self.x >= 0:
                if array[x][self.x] is None or array[x][self.x].id == 3:  # Check nothing is below
                    farthest_fall = x

        if farthest_fall > 0 and farthest_fall < len(array):
            if array[farthest_fall][self.x] is not None:
                # particle_array.remove(array[farthest_fall][self.x])
                move_val = 1
                while farthest_fall-move_val > 0 and array[farthest_fall-move_val][self.x] is not None:
                    move_val += 1
                array[farthest_fall-move_val][self.x] = array[farthest_fall][self.x]
                array[farthest_fall-move_val][self.x].y = farthest_fall-move_val
                array[farthest_fall - move_val][self.x].x = self.x
                array[farthest_fall][self.x] = None
            array[farthest_fall][self.x] = array[self.y][self.x]
            array[self.y][self.x] = None
            self.y = farthest_fall
            self.rect.x = self.x * scale
            self.rect.y = self.y * scale
            self.velocity += 1
            return True

        self.velocity = 1
        return False

    def dissolve_sand(self, array, scale, particle_array):
        num = random.randrange(0,1000)
        deleted = False
        if num == 0:
            if self.y+1 < len(array) and self.check_down_type(array) == 0:
                #del array[self.y+1][self.x]
                array[self.y + 1][self.x].free = True
                #array[self.y+1][self.x] = None
                deleted = True
                # print("Deleted Below")

            elif self.x > 0 and array[self.y][self.x-1] is not None and array[self.y][self.x-1].id == 0:
                #del array[self.y][self.x-1]
                array[self.y][self.x - 1].free = True
                #array[self.y][self.x-1] = None
                deleted = True

                # print("Deleted Left")
            elif self.x+1 < len(array[self.y]) and array[self.y][self.x+1] is not None and array[self.y][self.x+1].id == 0:
                #del array[self.y][self.x+1]
                array[self.y][self.x + 1].free = True
                #array[self.y][self.x+1] = None
                deleted = True
                # print("Deleted Right")
            elif self.y > 0 and array[self.y-1][self.x] is not None and array[self.y-1][self.x].id == 0:
                #del array[self.y-1][self.x]
                array[self.y - 1][self.x].free = True
                #array[self.y-1][self.x] = None
                deleted = True
                # print("Deleted Above")

            if deleted:
                if self.color.g < 50:
                    self.color.g += 8
                    self.color.r += 8
                if self.color.b > 200:
                    self.color.b -= 4
    def decay_self(self, array, particle_array):
        num1 = random.randrange(0,100000)
        if num1 == 0:
            if array[self.y][self.x] in particle_array:
                #particle_array.remove(array[self.y][self.x])
                #array[self.y][self.x] = None
                self.free = True
                # print("decayed")

    def interact_lava(self, array, scale, particle_array):
        num = random.randrange(0,5)
        if num == 0:
            x_loc = -1
            y_loc = -1
            if self.check_down_type(array) == 2: # check if touching lava
                # if not array[self.y + 1][self.x].free:
                    array[self.y + 1][self.x].free = True
                    x_loc = self.x
                    y_loc = self.y+1
                    # temp = Steam()
                    # temp.y = self.y+1
                    # temp.x = self.x
                    # array[temp.y][temp.x] = temp
                    # temp.rect.x = temp.x * scale
                    # temp.rect.y = temp.y * scale
                    # particle_array.append(temp)
                    # temp.rect.size = (scale, scale)
            if self.check_up_type(array) == 2:
                if not array[self.y - 1][self.x].free:
                    array[self.y - 1][self.x].free = True
                    x_loc = self.x
                    y_loc = self.y - 1
                    # temp = Steam()
                    # temp.y = self.y-1
                    # temp.x = self.x
                    # array[temp.y][temp.x] = temp
                    # temp.rect.x = temp.x * scale
                    # temp.rect.y = temp.y * scale
                    # particle_array.append(temp)
                    # temp.rect.size = (scale, scale)
            if self.check_left_type(array) == 2:
                if not array[self.y][self.x-1].free:
                    array[self.y][self.x-1].free = True
                    x_loc = self.x -1
                    y_loc = self.y
                    # temp = Steam()
                    # temp.y = self.y
                    # temp.x = self.x-1
                    # array[temp.y][temp.x] = temp
                    # temp.rect.x = temp.x * scale
                    # temp.rect.y = temp.y * scale
                    # particle_array.append(temp)
                    # temp.rect.size = (scale, scale)
            if self.check_right_type(array) == 2:
                if not array[self.y][self.x+1].free:
                    array[self.y][self.x+1].free = True
                    x_loc = self.x + 1
                    y_loc = self.y

                    # temp = Steam()
                    # temp.y = self.y
                    # temp.x = self.x+1
                    # array[temp.y][temp.x] = temp
                    # temp.rect.x = temp.x * scale
                    # temp.rect.y = temp.y * scale
                    # particle_array.append(temp)
                    # temp.rect.size = (scale, scale)
            if x_loc != -1 and y_loc != -1:
                placement = 0
                while y_loc - placement > 0 and array[y_loc-placement][x_loc] is not None:
                    placement+=1
                temp = Steam()
                temp.y = y_loc-placement
                temp.x = x_loc
                array[temp.y][temp.x] = temp
                temp.rect.x = temp.x * scale
                temp.rect.y = temp.y * scale
                particle_array.append(temp)
                temp.rect.size = (scale, scale)
                self.free = True



class Lava(Particle):
    def __init__(self):
        super().__init__(new_id=2,color=pygame.Color(255,0,0,255))  # set id to 2 for lava
        self.vel_change = 0

    def update(self, array, scale, particle_array):
        if self.free:
            if self in particle_array:
                particle_array.remove(self)
            array[self.y][self.x] = None
            del self
            return

        self.move_down(array, scale)
        #self.check_down_left(array, scale)
        #pself.check_down_right(array, scale)
        if not self.move_left(array, scale):
            self.move_right(array, scale)


    def interact_water(self, array, scale, particle_array):
        pass


class Steam(Particle):
    def __init__(self):
        super().__init__(new_id=3,color=pygame.Color(230,230,230,150))  # set id to 3 for steam
        self.vel_change = 0
        self.count = 0

    def update(self, array, scale, particle_array):
        if self.free:
            if self in particle_array:
                particle_array.remove(self)
            array[self.y][self.x] = None
            del self
            return


        self.move_up(array, scale)
        self.break_through_up(array, scale, particle_array)
        # self.check_down_left(array, scale)
        # self.check_down_right(array, scale)
        if not self.move_left(array,scale):
            self.move_right(array, scale)
        self.count += 1
        if self.count % 4 ==0:
            self.decay()
        elif self.count == 9:
            self.count = 0
        # self.check_right(array, scale)
        #if not self.check_left(array, scale):
         #   self.check_right(array, scale)

    def move_up(self, array, scale):
        farthest_fall = 0
        for x in range(self.y, self.y - int(self.velocity) - 1, -1):

            if x < len(array) and x > 0 and len(array[x]) > self.x >= 0:
                if array[x][self.x] is None:  # Check nothing is above
                    farthest_fall = x


        if 0 < farthest_fall < len(array):
            array[farthest_fall][self.x] = array[self.y][self.x]
            array[self.y][self.x] = None
            self.y = farthest_fall
            self.rect.x = self.x * scale
            self.rect.y = self.y * scale
            self.velocity += 0.15
            return True

        self.velocity = 1
        return False

    def move_left(self, array, scale):
        if self.x - 1 >= 0:
            if not self.check_left(array) and self.check_up(array):#(self.y == len(array)-1 or array[self.y+1][self.x] is not None):
                array[self.y][self.x-1] = array[self.y][self.x]
                array[self.y][self.x] = None
                self.y = self.y
                self.x = self.x-1
                self.rect.x = self.x * scale
                self.rect.y = self.y * scale
                return True
        return False

    def move_right(self, array, scale):
        if self.x + 1 < len(array[self.y]):
            if not self.check_right(array) and self.check_up(array):#(len(array)-1 or array[self.y+1][self.x] is not None): # Check nothing is below
                array[self.y][self.x+1] = array[self.y][self.x]
                array[self.y][self.x] = None
                self.y = self.y
                self.x = self.x+1
                self.rect.x = self.x * scale
                self.rect.y = self.y * scale

    def break_through_up(self, array, scale, particle_array):
        if self.check_up(array):
            if array[self.y-1][self.x].id != 3:
                num = random.randrange(0,100)
                if num == 0:
                    if array[self.y-1][self.x] in particle_array:
                        array[self.y - 1][self.x].free = True
                        #array[self.y-1][self.x] = array[self.y][self.x]
                        #self.y = self.y-1
                        self.x = self.x
                        self.rect.x = self.x * scale
                        self.rect.y = self.y * scale
                       # array[self.y][self.x] = None
    def decay(self):
        if self.color.a > 50:
            self.color.a -= 1
        else:
            self.free = True








if __name__ == "__main__":
    # Start Pygame
    size_x = 400
    size_y = 600

    count = 0

    scale = 8

    screen = pygame.display.set_mode((int(size_x), int(size_y)))
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    particle_array = []


    arr = []

    for y in range(int(size_y/scale)- 0):
        arr.append([])

    for y in range(len(arr)):
        for x in range(int(size_x/scale)- 0):
            arr[y].append(None)

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)

    # create a text surface object,
    # on which text is drawn on it.


    # create a rectangular object for the
    # text surface object

    chosen_type = 0


    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                chosen_type = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                chosen_type = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                chosen_type = 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                chosen_type = 3

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                for array in arr:
                    for item in array:
                        if item is not None and item not in particle_array:
                            item.free = True
                            if item.y > len(array):
                                array[array.index(item)] = None
                                del item
                            else:
                                item.update(array, scale, particle_array)


            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                for i in range(5):
                    for x in range(5):
                        if chosen_type == 0:
                            temp = Sand()
                        elif chosen_type == 1:
                            temp = Water()
                        elif chosen_type == 2:
                            temp = Lava()
                        else:
                            temp = Steam()
                        temp.x = int(pygame.mouse.get_pos()[0] / scale) + i
                        temp.y = int(pygame.mouse.get_pos()[1] / scale) + x

                        if temp.y < len(arr) and temp.x < len(arr[temp.y]) and arr[temp.y][temp.x] is None:
                            arr[temp.y][temp.x] = temp
                            temp.rect.x = temp.x * scale
                            temp.rect.y = temp.y * scale
                            particle_array.append(temp)
                            temp.rect.size = (scale, scale)
                            #print(temp.x)
                            #print(temp.y)
                            count += 1
                print(f'Total Particles: {len(particle_array)}')

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")


        # RENDER YOUR GAME HERE
        temp = Sand()

        for particle in particle_array:
            pygame.draw.rect(screen, color=particle.color, rect=particle.rect)
            particle.update(arr, scale, particle_array)


        text = font.render(f'FPS: {int(clock.get_fps())}', True, pygame.Color(255,255,255,255))
        textRect = text.get_rect()

        screen.blit(text, textRect)

        # flip() the display to put your work on screen
        pygame.display.flip()



        clock.tick(60)  # limits FPS to 60

    pygame.quit()
