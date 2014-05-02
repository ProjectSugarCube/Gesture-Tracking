import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import vtk
import time

f_x=0
f_y=0
f_z=0
i=1
o_x=0
o_y=0
o_z=0
a = 1

# create polygonal cube geometry
#   here a procedural source object is used,
#   a source can also be, e.g., a file reader
cube = vtk.vtkCubeSource()
cube.SetBounds(-0.8,0.8,-0.8,0.8,-0.8,0.8)
cube.SetCenter(0,0,-4)



# map to graphics library
#   a mapper is the interface between the visualization pipeline
#   and the graphics model
mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(cube.GetOutput()); # connect source and mapper


# an actor represent what we see in the scene,
# it coordinates the geometry, its properties, and its transformation
aCube = vtk.vtkActor()
aCube.SetMapper(mapper);
aCube.GetProperty().SetColor(0,1,0); # cube color green



# a renderer and render window
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1);

# an interactor
#iren = vtk.vtkRenderWindowInteractor()
#iren.SetRenderWindow(renWin);

cube1 = vtk.vtkCubeSource()
cube1.SetBounds(-0.5,0.5,-0.5,0.5,-0.5,0.5)
cube1.SetCenter(0,0,0)
mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInput(cube1.GetOutput());
bCube = vtk.vtkActor()
bCube.SetMapper(mapper1);
bCube.GetProperty().SetColor(0,1,1); # cube color green

# add the actor to the scene
ren1.AddActor(aCube);
ren1.AddActor(bCube);
ren1.LightFollowCameraOn();
ren1.SetBackground(1,1,1); # Background color white
i=0

## ----------- MORE CAMERA SETTINGS -----------------
## Initialize camera
cam = ren1.GetActiveCamera()
cam.SetFocalPoint(1,0,0)
cam.SetViewUp(0.,1.,0.);

## This is added so that it gives time to set
## no border in the OpenGL window and other stuff
## like minimizing other windows. 

renWin.Render()
t = 0.0
i = 1
j=0

cam.SetPosition(5,5,5)
#time.sleep(0.1)
cam.SetFocalPoint(0,0,0)

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

  
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        o_x=0
        o_y=0
        o_z=0
        '''
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        
         
        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]
            i = round(frame.id/10)
            # Get the hand's sphere radius and palm position
            '''
            print " palm position: %s" % (
                   hand.palm_position)
            '''
            f_x = hand.palm_position[0]
            f_y = hand.palm_position[1]-150
            f_z = hand.palm_position[2]
            print" i ", i
            print "x is: ", f_x
            print "y is: ", f_y
            print "z is: ", f_z
            if i%10== 0:
                o_x=f_x
                o_y=f_y
                o_z=f_z
            if (f_x != o_x):
                a = (f_x-o_x)/float(500)
                round(a)
                #print a
                cam.Azimuth(a)
            if (f_y != o_y):
                a = (f_y-o_y)/float(500)
                round(a)
                #print a
                cam.Elevation(a)
            if (f_z != o_z):
                a = (f_z-o_z)/float(1000)
                a = a/100
                round(a)
                a=1+a
                print a
                cam.Zoom(a)
            ren1.ResetCameraClippingRange()
            renWin.Render()
            i += 1
            if(i > 100):
                i=1

            '''
            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)
            '''

                    

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
