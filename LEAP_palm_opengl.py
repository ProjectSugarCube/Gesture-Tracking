

'''
def DrawGLScene():
	glBegin(GL_LINE_LOOP)
	circleSections=100
        for x in xrange(circleSections):
            angle = 2 * numpy.pi * x / circleSections
            glVertex2f(100+numpy.cos(angle)*100,100+numpy.sin(angle)*100)
        glEnd()
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import serial
import os
import threading
'''
matrix1 = [[0 for x in xrange(6)] for x in xrange(1)] 
matrix2 = [[0 for x in xrange(5)] for x in xrange(3)] 
matrix1[0][0] = 0
matrix1[0][1] = 0
matrix1[0][2] = 0
matrix1[0][3] = 0
matrix1[0][4] = 0
matrix1[0][5] = 0
'''
palm_matrix1 = [0 for x in xrange(3)]
palm_matrix1[0] = 0
palm_matrix1[1] = 0
palm_matrix1[2] = 0 
palm_matrix2 = [0 for x in xrange(3)]
palm_matrix2[0] = 0
palm_matrix2[1] = 0
palm_matrix2[2] = 0 
num_finger = 0
clockwiseness = 0
a=0
b=0
c=0
window = 0                                             # glut window number
width, height = 640, 480                               # window size
inct = 1
a_temp = 0
b_temp = 0
c_temp = 0

ESCAPE = '\033'

 
KEY_a = '\141'
 
KEY_b = '\142'
 
KEY_c = '\143'
 
KEY_d = '\144'
 
KEY_e = '\145'
 
KEY_f = '\146'
 
#Initiate the glut window
window = 0
 
# Rotation angle for the quadrilateral.
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
#AXIS direction
DIRECTION = 1

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        global clockwiseness
        global a,b,c
        frame = controller.frame()
        matrix1 = [[0 for x in xrange(6)] for x in xrange(1)] 
        num_finger = 0

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            #if not fingers.is_empty:
                # Calculate the hand's average finger tip position
            '''
                matrix1[0][0] = Leap.Vector()
                matrix1[0][1] = Leap.Vector()
                matrix1[0][2] = Leap.Vector()
                matrix1[0][3] = Leap.Vector()
                matrix1[0][4] = Leap.Vector()
                matrix1[0][5] = Leap.Vector()
                for finger in fingers:
                    #print "finger is", finger
                    #print "num_finger bef:", num_finger
                    matrix1[0][num_finger] = finger.tip_position
                    num_finger += 1
                    print "num_finger", num_finger
                avg_pos = num_finger
                print "Hand has %d fingers" %(len(fingers))
                print "finger tip position1 is: ", matrix1[0][0]
                print "finger tip position2 is: ", matrix1[0][1]
                print "finger tip position3 is: ", matrix1[0][2]
                print "finger tip position4 is: ", matrix1[0][3]
                print "finger tip position5 is: ", matrix1[0][4]
                
                global a
                global b
                global c
                
                global matrix1
                
                a = matrix1[0][0][0]+150
                b = matrix1[0][0][1]
                c = matrix1[0][0][2]
                print "x of finger 1 is :", a
                print "y of finger 1 is :", b
                print "z of finger 1 is :", c
               	
            

                num_finger = 0
            '''
            print "Hand sphere radius: %f mm, palm position: %s" % (
                  hand.sphere_radius, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)
            a=direction.pitch * Leap.RAD_TO_DEG
            b=normal.roll * Leap.RAD_TO_DEG
            c=direction.yaw * Leap.RAD_TO_DEG

            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    # Determine clock direction using the angle between the pointable and the circle normal
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counterclockwise"

                    

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

           

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"



def refresh2d(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():                                            # ondraw is called all the time

    global X_AXIS,Y_AXIS,Z_AXIS
    global DIRECTION
    global a_temp,b_temp, c_temp
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    #glClearColor(0.0, 0.0, 0.0, 0.0)
    #glLoadIdentity()                                   # reset position
    
    glClearDepth(1.0) 
    # The Type Of Depth Test To Do
    glDepthFunc(GL_LESS)
    # Enables Depth Testing
    glEnable(GL_DEPTH_TEST)
    # Enables Smooth Color Shading
    glShadeModel(GL_SMOOTH)   

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
 
    glMatrixMode(GL_PROJECTION)
    # Reset The Projection Matrix
    glLoadIdentity()
    
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(640)/float(480), 0.1, 100.0)
 
    glMatrixMode(GL_MODELVIEW)
    #print "coordinatezz: ", a
    # "Deal with itzz:",b
    # Move Right And Into The Screen
    glTranslatef(0.0,0.0,-6.0)
 
    # Rotate The Cube On X
    glRotatef(X_AXIS,1.0,0.0,0.0)
    # Rotate The Cube On Y
    glRotatef(Y_AXIS,0.0,1.0,0.0)
    # Rotate The Cube On Z
    glRotatef(Z_AXIS,0.0,0.0,1.0)
 
    # Start Drawing The Cube
    glBegin(GL_QUADS)
 
 
    # Set The Color To Blue
    glColor3f(0.0,1.0,0.0)
    # Top Right Of The Quad (Top)
    glVertex3f( 1.0, 1.0,-1.0)
    # Top Left Of The Quad (Top)
    glVertex3f(-1.0, 1.0,-1.0)
    # Bottom Left Of The Quad (Top)
    glVertex3f(-1.0, 1.0, 1.0)
    # Bottom Right Of The Quad (Top)
    glVertex3f( 1.0, 1.0, 1.0) 
 
 
    # Set The Color To Orange
    glColor3f(1.0,0.5,0.0)
    # Top Right Of The Quad (Bottom)
    glVertex3f( 1.0,-1.0, 1.0)
    # Top Left Of The Quad (Bottom)
    glVertex3f(-1.0,-1.0, 1.0)
    # Bottom Left Of The Quad (Bottom)
    glVertex3f(-1.0,-1.0,-1.0)
    # Bottom Right Of The Quad (Bottom)
    glVertex3f( 1.0,-1.0,-1.0) 
 
 
	# Set The Color To Red
    glColor3f(1.0,0.0,0.0)
    # Top Right Of The Quad (Front)
    glVertex3f( 1.0, 1.0, 1.0)
    # Top Left Of The Quad (Front)
    glVertex3f(-1.0, 1.0, 1.0)
    # Bottom Left Of The Quad (Front)
    glVertex3f(-1.0,-1.0, 1.0)
    # Bottom Right Of The Quad (Front)
    glVertex3f( 1.0,-1.0, 1.0)
 
 
    # Set The Color To Yellow
    glColor3f(1.0,1.0,0.0)
    # Bottom Left Of The Quad (Back)
    glVertex3f( 1.0,-1.0,-1.0)
    # Bottom Right Of The Quad (Back)
    glVertex3f(-1.0,-1.0,-1.0)
    # Top Right Of The Quad (Back)
    glVertex3f(-1.0, 1.0,-1.0)
    # Top Left Of The Quad (Back)
    glVertex3f( 1.0, 1.0,-1.0)
 
 
    # Set The Color To Blue
    glColor3f(0.0,0.0,1.0)
    # Top Right Of The Quad (Left)
    glVertex3f(-1.0, 1.0, 1.0) 
    # Top Left Of The Quad (Left)
    glVertex3f(-1.0, 1.0,-1.0)
    # Bottom Left Of The Quad (Left)
    glVertex3f(-1.0,-1.0,-1.0) 
    # Bottom Right Of The Quad (Left)
    glVertex3f(-1.0,-1.0, 1.0) 
 
 
    # Set The Color To Violet
    glColor3f(1.0,0.0,1.0)
    # Top Right Of The Quad (Right)
    glVertex3f( 1.0, 1.0,-1.0) 
    # Top Left Of The Quad (Right)
    glVertex3f( 1.0, 1.0, 1.0)
    # Bottom Left Of The Quad (Right)
    glVertex3f( 1.0,-1.0, 1.0)
    # Bottom Right Of The Quad (Right)
    glVertex3f( 1.0,-1.0,-1.0)
    # Done Drawing The Quad
    glEnd()
    refresh2d(width, height)
 

    ''' 
    for num in xrange(4):
    	glColor3f(0.0, 0.0, 1.0)                           # set color to blue 
    	glBegin(GL_LINE_LOOP)
    	circleSections=100
    	print "test: ", matrix1[0][num]
    	try:
    		a = matrix1[0][num][0]+150
    		b = matrix1[0][num][1]
    		c = matrix1[0][num][2]+50
                #commented out in circe2.py
                if c < 10 and c > -10:
                    print "It's not just you."
                    global X_AXIS,Y_AXIS,Z_AXIS
                    global DIRECTION
                    #str1 =  glReadPixels( a , b , 2 , 2 , GLUT_RGBA, type = GL_INT , array = None ) 
                    #print "pixel colour: ", str1[0]
                    X_AXIS = X_AXIS + (a/10)
                    Y_AXIS = Y_AXIS + (b/10)
                
    	except:
    		a=0
    		b=0
    		c=0
                glColor3f(0.0,0.0,0.0)
    	for x in xrange(circleSections):X_AXIS = X_AXIS + ((a-a_temp)/100)
                        Y_AXIS = Y_AXIS + ((b-b_temp)/100)
    		angle = 2 * numpy.pi * x / circleSections
    		glVertex2f(a+numpy.cos(angle)*(c/float(2)), b+numpy.sin(angle)*(c/float(2)))
        glEnd()
        
        if c < 10 and c > -10:
                    print "It's not just you."
                    global X_AXIS,Y_AXIS,Z_AXIS
                    global DIRECTION
                    #str1 =  glReadPixels( a , b , 1 , 1 , GL_RGBA, type = GL_FLOAT , array = None ) 
                    #print "pixel colour: ", str1[0]
                    currentColor=(GLuint * 1)(0)
                    glReadPixels(a,b,1,1,GL_RGB,GL_UNSIGNED_INT,currentColor)
                    print "Cureent color is: ", currentColor
                    #print " value is : ", currentColor
                    if currentColor[0] != 0:
                        if inct%20 == 0:
                            a_temp = a
                            b_temp = b
                        X_AXIS = X_AXIS + ((a-a_temp)/100)
                        Y_AXIS = Y_AXIS + ((b-b_temp)/100)
    	'''
    if clockwiseness == "clockwise" :
        #print 'its working babz.'
        if inct%100 == 0:
            a_temp = a
            b_temp = b
            c_temp = c
        X_AXIS = X_AXIS + ((a-a_temp)/100)
        Y_AXIS = Y_AXIS + ((b-b_temp)/100)
        print ' value of ex',X_AXIS



    global inct
    inct += 1
    if inct%100 == 0 :
        print "the increment is: ", inct
    if inct > 1000:
        inct = 0
    # ToDo draw rectangle
    glutSwapBuffers()                                  # important fordouble buffering

# initialization
'''
        global X_AXIS,Y_AXIS,Z_AXIS
        global DIRECTION
        # If escape is pressed, kill everything.
        if args[0] == ESCAPE:
                sys.exit()
        elif args[0] == KEY_a:
                DIRECTION = 1
                X_AXIS = X_AXIS + 0.30
        elif args[0] == KEY_b:
                DIRECTION = 1
                Y_AXIS = Y_AXIS + 0.30
        elif args[0] == KEY_c:
                DIRECTION = 1
                Z_AXIS = Z_AXIS + 0.30
        elif args[0] == KEY_d:
                DIRECTION = -1
                X_AXIS = X_AXIS - 0.30
        elif args[0] == KEY_e:
                DIRECTION = -1
                Y_AXIS = Y_AXIS - 0.30
        elif args[0] == KEY_f:
                DIRECTION = -1
                Z_AXIS = Z_AXIS - 0.30
'''
def main():
	# Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    window = glutCreateWindow("Cube Interaction")              # create window with title
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # draw all the time
    #glutKeyboardFunc(keyPressed)						   # Register the function called when the keyboard is pressed. 
    glutMainLoop()                                         # start everything



    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

if __name__ == "__main__":
        main() 
