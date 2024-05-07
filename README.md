# Gstreamer with AI : Intro 

This repository serves as an introductory demo for leveraging **Gstreamer** for Computer Vision. For more "advanced" stuff, please refer to [CPP_Gstreamer_Template](https://github.com/byermekov/CPP_Gstreamer_Template/tree/main)

In this demo we will be looking at **Python** implementation of **Gstreamer**(Gst). 
Python bindings for GStreamer are implemented on top of the GStreamer C API. The GStreamer framework itself is written in **C**. For me, Gst-Python is much more beginner-friendly. However, there are prominent [reasons](#limitation) on why it is recommended to go with Gst-C.


## Installation (Windows 10):

Gstreamer installation might be tedious 😢. Hence, if you are on Windows, it is recommended to use **MSYS2** for installing **Gstreamer**

[MSYS2](https://www.msys2.org/wiki/MSYS2-introduction/) is software distribution and a building platform for Windows. It provides a Unix-like environment, a command-line interface and a software repository making it easier to install, use, build and port software on Windows.


You may take a look at following instructions:
* Download **MSYS2** : from [here](https://github.com/msys2/msys2-installer/releases) 
* Run the following commands in **MSYS2 MINGW64** and you're good to go :
    * ```pacman -Syu```
    * ```pacman -S mingw-w64-x86_64-gstreamer mingw-w64-x86_64-gst-devtools mingw-w64-x86_64-gst-plugins-{base,good,bad,ugly} mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject```

# What is GStreamer?

-   Wikipedia description:

*GStreamer* is a [pipeline](https://en.wikipedia.org/wiki/Pipeline_(computing))-based [multimedia framework](https://en.wikipedia.org/wiki/Multimedia_framework) that links together a wide variety of media processing systems to complete complex workflows. For instance, GStreamer can be used to build a system that reads files in one format, processes them, and exports them in another. The formats and processes can be changed in a plug and play fashion.

-   Can process video & audio data

### Architecture:

#### Central concept : *Gstreamer pipeline (can be referred to as a linked list)*

-   Contains input source (src)
-   Contains output endpoint (sink)
-   Blocks are called pads/elements
  
![image](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/75485711-3d24-4eef-b418-9ecb527ac5bd)

![image](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/847e9273-0619-485d-851d-70f96597cf5f)

### Elements

-   SRC (source) elements : file readers `filesrc`, network elements (http, rtsp) `rtspsrc`, capture elements (video, audio) `autovideosrc` (Mac OS) `ksvideosrc` (Windows)
-   SINK (output) elements : `appsink` `autovideosink` `filesink`
-   OTHER elements : `decodebin` `tee` `mux` `demux` `queue` etc.

### Example pipeline:

Pipeline can be passed to our program using string where each element is separated by `!` mark:

Example with demo:

`ksvideosrc ! decodebin ! videoconvert ! autovideosink`

[gstreamer1.webm](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/04811fff-9504-4068-9faa-cf60025046e5)

### More examples to play around with Gstreamer pipeline:

-   Adding `edgetv` to include `Edge detection filter` step for the pipeline:

`ksvideosrc ! decodebin ! videoconvert ! edgetv ! videoconvert ! autovideosink`

[gstreamer2.webm](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/09ac5c10-c629-40ec-b6e5-271459de7561)


-   Adding `rippletv` to include `Ripple filter` for the pipeline

`ksvideosrc ! decodebin ! videoconvert ! rippletv ! videoconvert ! autovideosink`

[gsteamer3.webm](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/810dcef7-25bd-4e3a-96ef-0f7218e909bf)


### appsink:

Can be used to manipulate data in the pipeline:

[gstreamer_app.webm](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/1e5b7e77-f94c-465d-8461-c22a356c9730)


## Why Gstreamer?

Gstreamer pipeline can have *multiple source pads* as well as *multiple sink pads*. Additionally, it supports network frame transfer with `rtspsrc` element.

It comes handy when we have multiple IP Cameras that transfer frames with Real-Time Streaming Protocol (RTSP) such that we apply AI inference to multiple frames at the same time. (please refer to [This repository](https://github.com/byermekov/CPP_Gstreamer_Template/tree/main))

## Example of using AI with Gstreamer:

[gst_face.webm](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/0330a0a8-fc4b-4df5-a64d-260c6efd09f3)


Remarks:
Following pipeline was constructed:

`ksvideosrc ! decodebin ! videoconvert ! video/x-raw,format=RGB ! tee name=mytee ! queue ! appsink name=sink mytee. ! queue ! autovideosink`

`tee` element is used for splitting our pipeline to 2 sinks:

-   `appsink` - to apply our AI inference
-   `autovideosink` - to display the frames
-   also `queue` might be necessary for preventing potential deadlocks.

![image](https://github.com/byermekov/Gstreamer_Intro/assets/90006738/a2f0cfd0-24b6-46d3-95ea-55d2f837d01e)

<a name="limitation"></a>
### Limitation
As it may be already observable that:
* Objects are detected but not tracked (i.e. no rectangles surrounding the object displayed). 
* We obtain frames(buffer) only at the point when it reaches `appsink`. 

This is the main reason it is recommended to use Gstreamer C API. It is **not** possible make [buffer writable](https://gstreamer.freedesktop.org/documentation/additional/design/buffer.html?gi-language=c) in Python Gst API. 

### Remedy 
##### In order to successfully track objects, we need to take following steps:
* Add [**probe**](https://gstreamer.freedesktop.org/documentation/additional/design/probes.html?gi-language=c) to the pipeline elements : we must be able to manipulate buffers/frames before reaching the sink
* We need [**writable buffers**](https://gstreamer.freedesktop.org/documentation/additional/design/buffer.html?gi-language=c)  to be able to "draw rectangles"

These steps are easily reproducible and you can refer to [C++ implementation](https://github.com/byermekov/CPP_Gstreamer_Template/tree/main)

# Thank you!

[https://gstreamer.freedesktop.org/](https://gstreamer.freedesktop.org/)

[https://en.wikipedia.org/wiki/GStreamer](https://en.wikipedia.org/wiki/GStreamer)

[https://www.msys2.org/wiki/MSYS2-introduction/](https://www.msys2.org/wiki/MSYS2-introduction/)
