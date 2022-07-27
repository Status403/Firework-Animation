import math
import time
import pygame
import random
pygame.init()

class Main:
    FPS = 60
    COLORS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 165, 0),
        (255, 255, 255),
        (230, 230, 250),
        (255, 192, 203)
            ]

    def __init__(self, num_launchers, min_frequency, max_frequency, width=800, height=800):
        self.win = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Firework!")
        Main.WIDTH = width
        Main.HEIGHT = height

        self.launchers = []
        self.create_launchers(num_launchers,min_frequency,max_frequency)
    
    def create_launchers(self, num_launchers, min_frequency, max_frequency):
        space_between_launchers = 2
        if num_launchers >= self.WIDTH / (self.Launcher.WIDTH + space_between_launchers):
            num_launchers = int(self.WIDTH // (self.Launcher.WIDTH + space_between_launchers))

        launcher_space = self.WIDTH / num_launchers

        for i in range(num_launchers):
            frequency = random.randint(min_frequency,max_frequency)
            x = launcher_space * i + launcher_space/2 - self.Launcher.WIDTH/2
            y = self.HEIGHT - self.Launcher.HEIGHT
            self.launchers.append(self.Launcher(x,y,frequency,self.win))
    
    def draw(self):
        self.win.fill("black")
        for launcher in self.launchers:
            launcher.draw()

        pygame.display.update()
    
    def run(self):
        clock = pygame.time.Clock()
        
        r = True
        while r:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE]:
                    r = False
                    break
            
            for launcher in self.launchers:
                launcher.loop(self.WIDTH,self.HEIGHT)
            self.draw()
        pygame.quit()
    
    class Launcher:
        WIDTH = 30
        HEIGHT = 30
        COLOR = "grey"
        MIN_EXPLODE_HEIGHT = 300
        MAX_EXPLODE_HEIGHT = 700

        def __init__(self, x, y, frequency,win):
            self.x = x 
            self.y = y 
            self.frequency = frequency
            self.start_time = time.time()
            self.fireworks = []
            self.win = win
        
        def launch(self):
            color = random.choice(Main.COLORS)
            explode_height = random.randint(self.MIN_EXPLODE_HEIGHT, self.MAX_EXPLODE_HEIGHT)
            firework = self.Firework(self.x+self.WIDTH/2,self.y,-5,explode_height,color,self.win)
            self.fireworks.append(firework)

        def loop(self, max_width, max_height):
            current_time = time.time()
            time_elapsed = current_time - self.start_time
            if time_elapsed * 1000 >= self.frequency:
                self.start_time = current_time
                self.launch()
            fireworks_to_remove = []
            for firework in self.fireworks:
                firework.move(max_width,max_height)
                if firework.exploded and len(firework.projectiles) == 0:
                    fireworks_to_remove.append(firework)
            
            for firework in fireworks_to_remove:
                self.fireworks.remove(firework)
    
        def draw(self):
            pygame.draw.rect(self.win, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))
            for firework in self.fireworks:
                firework.draw()
        
        class Firework:
            RADIUS = 15
            MAX_PROJECTILES = 40
            MIN_PROJECTILES = 25
            PROJECTILE_VEL = 3

            def __init__(self, x, y, y_vel, explode_height, color,win):
                self.x = x 
                self.y = y 
                self.y_vel = y_vel
                self.explode_height = explode_height
                self.color = color
                self.win = win
                self.exploded = False
                self.projectiles = []
        
            def explode(self):
                self.exploded = True
                num_projectiles = random.randint(self.MIN_PROJECTILES,self.MAX_PROJECTILES)
                self.create_projectiles(num_projectiles)
            
            def create_projectiles(self, num_projectiles):
                angle_dif = math.pi * 2 / num_projectiles
                current_angle = 0
                vel = self.PROJECTILE_VEL
                for _ in range(num_projectiles):
                    x_vel = math.sin(current_angle) * vel
                    y_vel = math.cos(current_angle) * vel
                    color = random.choice(Main.COLORS)
                    self.projectiles.append(self.Projectile(self.x,self.y,x_vel,y_vel,color,self))
                    current_angle += angle_dif
            
            def create_sub_projectiles(self, x, y, angle):
                num_projectiles = 24
                angle_dif = 2*angle/360 * math.pi  / num_projectiles
                delta_x = (x - self.x) 
                delta_y = (y - self.y)
                if delta_y == 0:
                    if delta_x > 0:
                        current_angle =  90/360 * 2 * math.pi
                    else:
                        current_angle = 270/360 * 2 * math.pi
                else:
                    current_angle = math.atan2(delta_x,delta_y)
                current_angle += 0.5*angle_dif
                if current_angle < 0:
                    current_angle = 2* math.pi + current_angle
                
                current_angle = current_angle - (angle*0.5)/360 * 2*math.pi
                if current_angle < 0:
                    current_angle = 2*math.pi + current_angle 
                vel = 1
                for _ in range(num_projectiles):
                    x_vel = math.sin(current_angle) * vel
                    y_vel = math.cos(current_angle) * vel
                    color = random.choice(Main.COLORS)
                    projectile = self.SubProjectile(x,y,x_vel,y_vel,color,self)
                    self.projectiles.append(projectile)
                    current_angle += angle_dif
                    if current_angle > 2 * math.pi:
                        current_angle = current_angle - 2*math.pi
        
            def move(self, max_width, max_height):
                if not self.exploded:
                    self.y += self.y_vel
                    if self.y <= self.explode_height:
                        self.explode()
                
                projectiles_to_remove = []
                for projectile in self.projectiles:
                    projectile.move()
                    if projectile.x >= max_width or projectile.x < 0:
                        projectiles_to_remove.append(projectile)
                    elif projectile.y >= max_height or projectile.y < 0:
                        projectiles_to_remove.append(projectile)
                
                for projectile in projectiles_to_remove:
                    self.projectiles.remove(projectile)
        
            def draw(self):
                if not self.exploded:
                    pygame.draw.circle(self.win,self.color,(self.x,self.y),self.RADIUS)
            
                for projectile in self.projectiles:
                    if projectile.alpha > 0:
                        projectile.draw()
                
            class Projectile:
                WIDTH = 5
                HEIGHT = 10
                ALPHA_DECREMENT = 3

                def __init__(self, x, y, x_vel, y_vel, color,firework):
                    self.x = x
                    self.y = y 
                    self.x_vel = x_vel 
                    self.y_vel = y_vel
                    self.color = color
                    self.firework = firework
                    self.alpha = 255
                
                def move(self):
                    self.x += self.x_vel
                    self.y += self.y_vel
                    if self.alpha > 0 and self.alpha <= self.ALPHA_DECREMENT:
                        self.alpha = 0
                        angle = 360
                        self.firework.create_sub_projectiles(self.x,self.y,angle)
                    else:
                        self.alpha = self.alpha-self.ALPHA_DECREMENT
                
                def draw(self):
                    self.draw_rect_alpha(self.firework.win, self.color + (self.alpha,), (self.x,self.y,self.WIDTH,self.HEIGHT))
                                
                @staticmethod
                def draw_rect_alpha(surface, color, rect):
                    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
                    pygame.draw.rect(shape_surf,color,shape_surf.get_rect())
                    surface.blit(shape_surf,rect)
                
            class SubProjectile(Projectile):
                WIDTH = 3
                HEIGHT = 6
                ALPHA_DECREMENT = 5
                def __init__(self, x, y, x_vel, y_vel, color, firework):
                    super().__init__(x, y, x_vel, y_vel, color, firework)
                
                def move(self):
                    self.x += self.x_vel
                    self.y += self.y_vel
                    if self.alpha > 0 and self.alpha <= self.ALPHA_DECREMENT:
                        self.alpha = 0
                    else:
                        self.alpha = self.alpha-self.ALPHA_DECREMENT



if __name__ == "__main__":
    num_launchers = 3 #if larger than window size, it will take the maximum ammount possible
    min_frequency = 2000
    max_frequency = 5000
    width = 1920 * 1 #optional
    height = 1080 * 1 #optional
    Main(num_launchers, min_frequency, max_frequency, width, height).run()
