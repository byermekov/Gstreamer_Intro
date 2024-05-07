from threading import Thread
import time
from time import sleep
import gi
import numpy as np
import cv2

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GLib, GstApp


_ = GstApp

Gst.init()


# def on_new_sample(app_sink):

#     sample = app_sink.pull_sample()
#     caps = sample.get_caps()

#     # Extract the width and height info from the sample's caps
#     height = caps.get_structure(0).get_value("height")
#     width = caps.get_structure(0).get_value("width")

#     # Get the actual data
#     buffer = sample.get_buffer()
#     print(caps,"buffer size ",buffer.get_size())
#     # Get read access to the buffer data
#     success, map_info = buffer.map(Gst.MapFlags.READ)

#     if not success:
#         raise RuntimeError("Could not map buffer data!")

#     numpy_frame = np.ndarray(
#         shape=(height, width, 3),
#         dtype=np.uint8,
#         buffer=map_info.data)

#     buffer.unmap(map_info)
#     print('Success!')

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

# pipeline = Gst.parse_launch("ksvideosrc ! decodebin ! videoconvert ! autovideosink")
# # pipeline = Gst.parse_launch("ksvideosrc ! decodebin ! videoconvert ! rippletv ! "
# #                             "videoconvert ! appsink")
# pipeline = Gst.parse_launch("ksvideosrc ! decodebin ! videoconvert ! video/x-raw,format=RGB ! videoconvert ! appsink name=sink")
pipeline = Gst.parse_launch("ksvideosrc ! decodebin ! videoconvert ! video/x-raw,format=RGB ! tee name=mytee ! queue ! appsink name=sink mytee. ! queue ! autovideosink")
appsink = pipeline.get_by_name("sink")

pipeline.set_state(Gst.State.PLAYING)


try:
    while True:
        sample = appsink.try_pull_sample(Gst.CLOCK_TIME_NONE)
        if sample is None:
            continue
        caps = sample.get_caps()


        height = caps.get_structure(0).get_value("height")
        width = caps.get_structure(0).get_value("width")

        buffer = sample.get_buffer()

        success, map_info = buffer.map(Gst.MapFlags.READ)

        if not success:
            raise RuntimeError("Could not map buffer data!")

        numpy_frame = np.ndarray(
            shape=(height, width, 3),
            dtype=np.uint8,
            buffer=map_info.data)

        buffer.unmap(map_info)

        face_cascade = cv2.CascadeClassifier('C:/msys64/mingw64/share/opencv4/haarcascades/haarcascade_frontalface_default.xml') # may use relative path as well

        bgr_image = cv2.cvtColor(numpy_frame, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            print("FACE DETECTED!")
        else:
            print('NO FACE DETECTED!')
        
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()