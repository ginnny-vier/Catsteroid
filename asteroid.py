from turtle import position
from if3_game.engine import Sprite
from pyglet import window
from math import cos, sin, radians
from random import randint

RESOLUTION = (800,600)


class Space_items(Sprite):
    def __init__(self, image, position, anchor, speed = (0,0), rotation_speed = 0):
        super().__init__(image, position, anchor = anchor)
        self.speed = speed #100 pixel / par seconde sur l'axe des X et de 200 sur l'axe des Y
        self.rotation_speed = rotation_speed


    def update(self, dt):
        super().update(dt) # DT = delta time ou temps entre chaques frames
        #position actuelle
        pos_x = self.position[0]
        pos_y = self.position[1]

        #calcul deplacement (distance parcourue = vitesse * le temps)
        # move = vitesse de x * dt et vitesse de y * dt 
        move = (self.speed[0] * dt, self.speed[1] * dt)

        #application du deplacement
        pos_x += move[0]
        pos_y += move[1]

        # correction position si hors ecran
        if pos_x > RESOLUTION[0] + 32:
            pos_x = -32
        elif pos_x < -32:
            pos_x = RESOLUTION[0] + 32

        if pos_y > RESOLUTION[1] + 32:
            pos_y = -32
        elif pos_y < -32:
            pos_y = RESOLUTION[1] + 32

        # on bouge l'objet
        self.position = (pos_x , pos_y )

        self.rotation += self.rotation_speed * dt # calcule de la rotation. Attribut de la classe
        # self.rotation ==> vient de l'engine
      
class Spaceship(Space_items):

    def __init__(self, position):
        image = "images/spaceship.png"
        anchor = (32,32)
        super().__init__(image, position, anchor)
        self.velocity = 0

    def update(self, dt):
        delta_speed_x = cos(radians(self.rotation)) * self.velocity
        delta_speed_y = sin(radians(self.rotation)) * self.velocity * -1
         
        self.speed = (self.speed[0] + delta_speed_x, self.speed[1] + delta_speed_y)

        super().update(dt)


    def on_key_press(self, key, modifiers ): #modifiers == shift et alt
        if key == window.key.LEFT:
            self.rotation_speed = -100

        elif key == window.key.RIGHT:
            self.rotation_speed = 100

        elif key == window.key.UP:
            self.velocity = 5

        elif key == window.key.SPACE:
            self.spawn_bullet()

    def on_key_release(self, key, modifiers):
        if key == window.key.LEFT and self.rotation < 0:
            self.rotation_speed = 0
        elif key == window.key.RIGHT and self.rotation > 0:
            self.rotation_speed = 0
        elif key == window.key.UP:
            self.velocity = 0 

    def spawn_bullet(self):
        bullet_velocity = 100

        speed_x = cos(radians(self.rotation)) * bullet_velocity
        speed_y = sin(radians(self.rotation)) * bullet_velocity * -1

        bullet_speed = (self.speed[0] + speed_x, self.speed[1] + speed_y)

        x = cos(radians(self.rotation)) *  40
        y = sin(radians(self.rotation)) *  40 * -1


        bullet_position = (self.position[0] + x, self.position[1] + y)

        bullet = Bullet(bullet_position, bullet_speed)
        self.layer.add(bullet)

    def on_collision(self, other):
            if isinstance(self,Asteroid128):
                self.destroy()


class Asteroid128(Space_items):

    def __init__(self, position, speed,level=3):

        self.level = level
        if level == 3:
            image = "images/asteroid128.png"
            anchor = (64,64)

        elif level == 2:
            image = "images/asteroid64.png"
            anchor = (32,32)

        else:
            image = "images/asteroid32.png"
            anchor = (16,16)
    
        rotation_speed = 50
        super().__init__(
            image, position, anchor, speed, rotation_speed)

        def destroy(self):
            if self.level > 1:
                for n in range (2):
                    speed_x = randint(-300, 300)
                    speed_y = randint(-300, 300)
                    speed = (speed_x, speed_y)
                    
                    level = self.level - 1

                    asteroid = Asteroid128(self.position, speed, level=level )

                    self.layer.add(asteroid)

            super().destroy()


class Bullet(Space_items):
    def __init__(self, position, speed):

        image = "images/bullet.png"
        anchor = (8,8)
        rotation_speed = 100
        super().__init__(image, position, anchor, speed, rotation_speed)

        self.lifetime = 0
    
    def update(self, dt):
        super().update(dt)
        self.lifetime += dt
        if self.lifetime >= 3:
            self.destroy()


    def on_collision(self, other):
        if isinstance(other, Asteroid128):
            self.destroy()
            other.destroy()






        



