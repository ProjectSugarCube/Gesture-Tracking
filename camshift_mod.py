#!/usr/bin/env python

import cv2
import cv2.cv as cv
import vtk
import time


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
matrix1 = [0 for x in xrange(2)]
trace_val=0
f_x=0
f_y=0
o_x=0
o_y=0
a=0


def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

class CamShiftDemo:

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow( "CamShiftDemo", cv2.WINDOW_NORMAL )
        cv.NamedWindow( "Histogram", 1 )
        cv.SetMouseCallback( "CamShiftDemo", self.on_mouse)

        self.drag_start = None      # Set to (x,y) when mouse starts drag
        self.track_window = None    # Set to rect when the mouse drag finishes

        print( "Keys:\n"
            "    ESC - quit the program\n"
            "    b - switch to/from backprojection view\n"
            "To initialize tracking, drag across the object with the mouse\n" )

    def hue_histogram_as_image(self, hist):
        """ Returns a nice representation of a hue histogram """

        histimg_hsv = cv.CreateImage( (320,200), 8, 3)

        mybins = cv.CloneMatND(hist.bins)
        cv.Log(mybins, mybins)
        (_, hi, _, _) = cv.MinMaxLoc(mybins)
        cv.ConvertScale(mybins, mybins, 255. / hi)

        w,h = cv.GetSize(histimg_hsv)
        hdims = cv.GetDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) / (w - 1)  # hue sweeps from 0-180 across the image
            val = int(mybins[int(hdims * x / w)] * h / 255)
            cv.Rectangle( histimg_hsv, (x, 0), (x, h-val), (xh,255,64), -1)
            cv.Rectangle( histimg_hsv, (x, h-val), (x, h), (xh,255,255), -1)

        histimg = cv.CreateImage( (320,200), 8, 3)
        cv.CvtColor(histimg_hsv, histimg, cv.CV_HSV2BGR)
        return histimg

    def on_mouse(self, event, x, y, flags, param):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
        if event == cv.CV_EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = self.selection
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)

    def run(self):
        hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
        backproject_mode = False
        i=1
        o_x=0
        o_y=0
        while True:
            frame = cv.QueryFrame( self.capture )

            # Convert to HSV and keep the hue
            hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
            cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
            self.hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
            cv.Split(hsv, self.hue, None, None, None)

            # Compute back projection
            backproject = cv.CreateImage(cv.GetSize(frame), 8, 1)

            # Run the cam-shift
            cv.CalcArrBackProject( [self.hue], backproject, hist )
            if self.track_window and is_rect_nonzero(self.track_window):
                crit = ( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 1)
                (iters, (area, value, rect), track_box) = cv.CamShift(backproject, self.track_window, crit)
                self.track_window = rect

            # If mouse is pressed, highlight the current selected rectangle
            # and recompute the histogram

            if self.drag_start and is_rect_nonzero(self.selection):
                sub = cv.GetSubRect(frame, self.selection)
                save = cv.CloneMat(sub)
                cv.ConvertScale(frame, frame, 0.5)
                cv.Copy(save, sub)
                x,y,w,h = self.selection
                cv.Rectangle(frame, (x,y), (x+w,y+h), (255,255,255))

                sel = cv.GetSubRect(self.hue, self.selection )
                cv.CalcArrHist( [sel], hist, 0)
                (_, max_val, _, _) = cv.GetMinMaxHistValue( hist)
                if max_val != 0:
                    cv.ConvertScale(hist.bins, hist.bins, 255. / max_val)
            elif self.track_window and is_rect_nonzero(self.track_window):
                cv.EllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 3, cv.CV_AA, 0 )
                #print track_box
                trace_val=track_box[0]
                f_x=trace_val[0]
                f_y=trace_val[1]
                print 'value1', f_x
                print 'value2', f_y
                if i%10 == 0:
                    o_x=f_x
                    o_y=f_y
                if (f_x != o_x):
                    a = (f_x-o_x)/float(10)
                    round(a)
                    cam.Azimuth(-a)
                if (f_y != o_y):
                    a = (f_y-o_y)/float(10)
                    round(a)
                    cam.Elevation(-a)
                ren1.ResetCameraClippingRange()
                renWin.Render()
                i += 1
                
                



            if not backproject_mode:
                cv.ShowImage( "CamShiftDemo", frame )
            else:
                cv.ShowImage( "CamShiftDemo", backproject)
            cv.ShowImage( "Histogram", self.hue_histogram_as_image(hist))

            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break
            elif c == ord("b"):
                backproject_mode = not backproject_mode

if __name__=="__main__":
    i=1
    demo = CamShiftDemo()
    demo.run()
    cv.DestroyAllWindows()
