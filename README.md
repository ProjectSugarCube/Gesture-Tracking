Gesture-Tracking
================

A few alternate methods for gesture based interaction using Python


This project contains implementations of a few tracking algorithms for interaction.

LEAP_fingers_opengl.py: (Python+OpenGL+LeapSDK) Python code that uses the LeapSDK for tracking fingers. The fingers can be used to rotate a cube created using OpenGL. (Requires the LEAP Motion Controller)

LEAP_palm_VTK.py: (Python+VTK+LeapSDK) Python code that uses the LeapSDK for performing palm tracking. Palm position can be tracked in 3D space, and this can be used to change the view within the virtual environment, created by VTK. (Requires the LEAP Motion Controller)

LEAP_palm_opengl: (Python+OpenGL+LeapSDK) Python code that uses the LeapSDK for performing palm tracking. Palm movement is tracked and can be used to rotate a cube created using OpenGL. This code uses a gesture for enabling/disabling rotation of the cube. A clockwise rotation of the palm enables movement of the cube, whereas anti-clockwise rotation of the palm disables movement of the cube. (Requires the LEAP Motion Controller)

skin_tracking.py: (Python+OpenCV) Python code that performs skin color detection and tracking. This module was developed with the intent of performing hand tracking and hand gesture detection. Skin color detection is performed using HSV color filtering by isolating the range of skin colors.

camshift_mod.py: (Python+OpenCV) Python code that performs color based tracking of objects. This code can be used for performing marker based tracking. This code is a modified version of the CAMSHIFT (Continuously Adaptive Meanshift) algorithm. Works well with objects that have a distinct and uniform color.
