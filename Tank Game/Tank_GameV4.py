import turtle
import math
import random

class screensetup:
    screen = turtle.Screen()
    screen.setup(500,500)
    screen.setworldcoordinates(-150.0,-150.0,150.0,150.0)
    screen.tracer(0)  
    turtle.speed(0) 

    
    def drawy(val):
        # line
        turtle.forward(300)
        
        # set position
        turtle.up()
        turtle.setpos(val,300)
        turtle.down()
        
        # another line
        turtle.backward(300)
        
        # set position again
        turtle.up()
        turtle.setpos(val+10,0)
        turtle.down()
        
    # method to draw y-axis lines
    def drawx(val):
        
        # line
        turtle.forward(300)
        
        # set position
        turtle.up()
        turtle.setpos(300,val)
        turtle.down()
        
        # another line
        turtle.backward(300)
        
        # set position again
        turtle.up()
        turtle.setpos(0,val+10)
        turtle.down()
    
    for i in range(30):
        drawy(10*(i+1))
 
    # set position for x lines
    turtle.right(90)
    turtle.up()
    turtle.setpos(0,0)
    turtle.down()
    
    # x lines
    for i in range(30):
        drawx(10*(i+1))
    
    turtle.hideturtle()

class tanks:
    def __init__(self,x,y,angle,size,v,health,color,targetx,targety,rotate):
        self.x=x
        self.y=y
        self.size=size
        self.angle=angle
        self.v=v
        self.health=health
        self.color=color
        self.targetx=targetx
        self.targety=targety
        self.rotate=rotate

    def draw(self):
        turtle.color(self.color)
        turtle.pu()
        turtle.goto(self.x,self.y-self.size)
        turtle.pd()
        turtle.setheading(0)
        turtle.circle(self.size)
        turtle.pu()
        turtle.goto(self.x,self.y)
        turtle.pd()
        turtle.goto(self.x+math.cos(self.angle)*self.size * 1.5,self.y+math.sin(self.angle)*self.size *1.5)
               
    def move(self):
        self.x+=math.cos(self.angle)* self.v
        self.y+=math.sin(self.angle)* self.v
        self.angle+=self.rotate

    def target(self, x, y):
        # Set the target coordinates
        self.targetx = x
        self.targety = y

        # Calculate the difference in x and y coordinates between the tank and the target
        dx = self.targetx - self.x
        dy = self.targety - self.y

        # Calculate the angle from the tank to the target using the arctangent of the differences (this is the angle the enemy aims)
        self.angle = math.atan2(dy, dx)

        

    def controlrotation(self,rotate):
        self.rotate=rotate

    def controlvelocity(self,velocity):
        self.v=velocity
    

    
    def distanceTo(self, other):
        #calculate distance between two tanks
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)
    
    def checkBorder(self):
        #check to see if object has moved beyond border and correct its position if True
        if self.x >= 150:
            self.x = 150
        if self.x <= -150:
            self.x = -150
        if self.y >= 150:
            self.y = 150
        if self.y <= -150:
            self.y = -150
            
    def collisionPrevention(self, enemy):
        # create a world boarder for enimes and user.
        self.checkBorder()
        enemy.checkBorder()

        # Calculate the difference in x and y coordinates of two tanks
        dx = self.x - enemy.x
        dy = self.y - enemy.y
        
        distance = self.distanceTo(enemy)

        # Calculate the sum of the radii of the two tanks
        sumOfRadii = self.size + enemy.size

        # If the distance between the two tanks is less than the sum of their radii, there is a collision
        if distance < sumOfRadii:
            # Calculate the amount of overlap between the two tanks
            overlap = sumOfRadii - distance

            # Calculate the unit vector x and y values.
            ux = dx / distance
            uy = dy / distance

            # Move the 2 tanks away from each other by half of the overlap distance
            self.x += ux * overlap / 2
            self.y += uy * overlap / 2
            enemy.x -= ux * overlap / 2  
            enemy.y -= uy * overlap / 2

class keyboard:
    def __init__(self,tank):
        keyboard.tank = tank
        keyboard.end=0
        screensetup.screen.listen() 
        screensetup.screen.onkeypress(self.kmove, "Up") 
        screensetup.screen.onkeyrelease(self.kstop, "Up")
        screensetup.screen.onkeypress(self.kleft, "Left")
        screensetup.screen.onkeyrelease(self.kleftstop, "Left")
        screensetup.screen.onkeypress(self.kright, "Right")
        screensetup.screen.onkeyrelease(self.krightstop, "Right")
        screensetup.screen.onkeypress(self.kend, "Escape")
    def kmove(self):  
        keyboard.tank.controlvelocity(1)
    def kstop(self):
        keyboard.tank.controlvelocity(0)
    def kleft(self):
        keyboard.tank.controlrotation(.02)
    def kleftstop(self):
        keyboard.tank.controlrotation(0)
    def kright(self):
        keyboard.tank.controlrotation(-.02)
    def krightstop(self):
        keyboard.tank.controlrotation(0)
    def kend(self):
        keyboard.end=1

def insertionSort(A):
    # Iterate over the array from the second element (index 1) to the end
    for i in range(1,len(A)):
        # The element to be compared with the sorted part of the array
        key = A[i]
        # The last index of the sorted part of the array
        j = i - 1
        # While there are elements in the sorted part of the array and they are greater than the key
        while j>=0 and key[1] < A[j][1]:
            # Shift the elements of the sorted part of the array to the right
            A[j+1] = A[j]
            # Move to the previous element
            j -= 1
        # Insert the key into its correct position in the sorted part of the array
        A[j+1] = key
    # return sorted array A
    return A


user=tanks(10,10,0,5,0,10,"blue",0,0,0)
keyboard(user)

numtanks= 4
enemy = [] 
for i in range(numtanks):    
    enemy+=[tanks(random.randint(5,195),random.randint(5,195),random.randint(0,360),5,0.2,10,"red",0,0,0)]

while not keyboard.end: 
    turtle.clear()
    

    for i in range(numtanks):
        for j in range(i + 1, numtanks):
            enemy[i].collisionPrevention(enemy[j])
        
        enemy[i].target(user.x,user.y)
        enemy[i].move()
        enemy[i].draw()
        user.collisionPrevention(enemy[i])
    user.move()
    user.draw()

    # Calculate the distances from the user to each enemy tank
    distances = [(i,user.distanceTo(enemy[i])) for i in range(numtanks)]
    
    # Sort the distances in ascending order using the insertionSort function
    distances = insertionSort(distances)

    # Print the ID and distance of the closest enemy tank
    print(f"Closest enemy is tank: {distances[0][0]}, Distance to the enemy: {distances[0][1]:.2f}", end='\r')


    screensetup.screen.update()
