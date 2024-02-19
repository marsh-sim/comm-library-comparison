# MAVLink communication

When allowing address reuse, multiple programs can listen on the same port, but still only one will get the data.

Multicast works well between multiple Python scripts, but in Simulink requires real-time mode, as described in [block documentation](https://it.mathworks.com/help/releases/R2023a/slrealtime/io_ref/udpmulticastreceive.html):

> The UDP Multicast Receive block operates in a real-time application running on a target computer. The block does not operate in a model simulation on a development computer.

This seems to be a huge complicated process, requiring a [Real-Time kernel installation](https://it.mathworks.com/help/sldrt/getting-started-with-real-time-windows-target.html)
