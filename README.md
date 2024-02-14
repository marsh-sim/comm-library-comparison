# Communication Library Comparison

Minimal examples to check selected libraries from "Proposed options for simulator architecture" document

## Roadmap

- [x] MQTT
  - Industrial Communication Toolbox doesn't include any Simulink blocks, corroborated by existence of a [commercial option](https://www.speedgoat.com/products/mqtt-client)
- [x] Data Distribution Service
  - Multiple features fail without full RTI Connext installation. That doesn't meet our licensing requirements:
    > The RTI Connext for DDS Blockset includes a **short term** evaluation license
  - When just running the Simulink model it isn't detected by `ddsls` (unlike a Python subscriber), the model needs to be built and run with MATLAB Coder (if I understood right), [found example of a similar failure](https://ennerf.github.io/2017/06/25/Using-MATLAB-for-hardware-in-the-loop-prototyping-1-Message-Passing-Systems.html#_data_distribution_service_dds)
- [ ] ZeroMQ
  - Based on a [blog post by a MathWorks employee](https://blogs.mathworks.com/simulink/2018/05/01/communicating-with-an-external-application-for-co-simulation/)
- [ ] MAVLink

## Installation

_Optional, but recommended: create and activate Python virtual environment_

```bash
pip install -r requirements.txt
```

### MQTT

Windows installer for [Mosquitto](https://mosquitto.org/download/)

Add installation folder to `Path` environment variable, default `C:/Program Files/mosquitto`

Install "Industrial Communication Toolbox" in MATLAB

### DDS

To avoid compiling the [CycloneDDS](https://github.com/eclipse-cyclonedds) C library from source, you need to use a Python version for which there are [prebuilt binaries on pip](https://pypi.org/project/cyclonedds/#files) available.
At the time of writing this were CPython versions 3.7 to 3.10 (inclusive).

## Results for ZeroMQ

- The method for building `libzmq` in the post is deprecated, now CMake has to be used
- Generated project with CMake GUI for Visual Studio 2022
- Build initially failed, v143 build tools weren't detected, changed to v142 (for VS 2019) in each project properties
- After succeeded build, copied `/libs/libzmq/build/bin/Release/libzmq-v143-mt-4_3_6.dll` to some directory in system `Path` and renamed to `libzmq.dll`
- had to modify `SimulinkCoSimulationExample/utils/SetEnvVariable.m`, `buildCoSimExample.m` and `buildCommExample.m` because they hardcoded the path from deprecated build script
- `startCoSimServer` shortcut just opens empty command prompt
- The model opened with "Co-Simulation Client Example" errors with the following error.
  - The path in error message does contain a file compiled in one of the previous steps
  - As suggested by this [StackOverflow comment](https://stackoverflow.com/a/15339283/8531075), this can be an issue with any DLL not being found

```
=== Simulation (Elapsed: 2 sec) ===
    Error:Error while obtaining sizes from MEX S-function 'statcalsfcngateway' in 'clientModel/EWMA_97_CoSim'.
    Caused by:
        Invalid MEX-file 'C:\Workspace\My-Repos\comm-library-comparison\SimulinkCoSimulationExample\CoSimExample\sfun\statcalsfcngateway.mexw64': The specified module could not be found.
```

- Same error with different `.mexw64` files appears on running every model included in the example project
