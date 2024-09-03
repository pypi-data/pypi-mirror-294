import sensingsp as ssp
import numpy as np
from mathutils import Vector
# import matplotlib
# matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import cv2

def make_simple_scenario():
    predefine_movingcube_6843()
def run_simple_chain():
    processing_1()
def predefine_movingcube_6843(interpolation_type='LINEAR'):
    #     Blender provides several interpolation types, and as of recent versions, there are 6 main interpolation options:

    # CONSTANT ('CONSTANT')
    # The value remains constant between keyframes, resulting in a stepped change at each keyframe.
    # LINEAR ('LINEAR')
    # The value changes linearly between keyframes, resulting in a straight transition between the keyframe points.
    # BEZIER ('BEZIER')
    # The value follows a bezier curve between keyframes, allowing for smooth transitions with adjustable handles for fine control over the curve.
    # SINE ('SINE')
    # The value follows a sine curve between keyframes, creating smooth, wave-like transitions.
    # QUAD ('QUAD')
    # The value follows a quadratic curve, which can create an accelerating or decelerating effect.
    # CUBIC ('CUBIC')
    # The value follows a cubic curve between keyframes, providing a slightly more complex smooth transition than quadratic.
    ssp.utils.delete_all_objects()
    ssp.utils.define_settings()
    cube = ssp.environment.add_cube(location=Vector((0, 0, 0)), direction=Vector((1, 0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
    cube["RCS0"]=1
    cube.location = (3,0,0)
    cube.keyframe_insert(data_path="location", frame=1)
    cube.location = (3, 3,0)
    cube.keyframe_insert(data_path="location", frame=30)
    cube.location = (3, -3,0)
    cube.keyframe_insert(data_path="location", frame=100)
    for fcurve in cube.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = interpolation_type
    ssp.integratedSensorSuite.define_suite(0, location=Vector((0, 0, 0)), rotation=Vector((0, 0, 0)))
    
    
    radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843_az(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_LinearArray(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9,LinearArray_TXPos=[0],LinearArray_RXPos=[i*3e8/70e9/2 for i in range(30)])
    
    
    
    # radar['RF_AnalogNoiseFilter_Bandwidth_MHz']=0
    
    ssp.utils.set_frame_start_end(start=1,end=100)
    ssp.utils.useCUDA()
    # print(f"rangeResolution maxUnambigiousRange = {ssp.radar.utils.rangeResolution_and_maxUnambigiousRange(radar)}")

def processing_1():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
    # plt.ion() 
    fig, FigsAxes = plt.subplots(2,3)
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        alld = []
        m = path_d_drate_amp[0][0][0][0][0][0][0][3]
        for itx in range(len(path_d_drate_amp[0][0][0][0][0])):
            for irx in range(len(path_d_drate_amp[0][0])):
                for d_drate_amp in path_d_drate_amp[0][0][irx][0][0][itx]:
                    # if d_drate_amp[3]==m:
                    alld.append(d_drate_amp[0:3])
        alld = np.array(alld)
        fig.suptitle(f'Frame: {ssp.config.CurrentFrame}')
        FigsAxes[0,2].cla()
        FigsAxes[1,2].cla()
        FigsAxes[0,2].plot(alld[:,0],'.')
        FigsAxes[1,2].plot(alld[:,1],'.')
        FigsAxes[0,2].set_xlabel('scatter index')
        FigsAxes[0,2].set_ylabel('d (m)')
        FigsAxes[1,2].set_xlabel('scatter index')
        FigsAxes[1,2].set_ylabel('dr (m/s)')
    
        # ssp.utils.force_zeroDoppler_4Simulation(path_d_drate_amp)
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration_frame(path_d_drate_amp)
        ssp.integratedSensorSuite.SensorsSignalProccessing_Chain_RangeProfile_RangeDoppler_AngleDoppler(Signals,FigsAxes,fig)
        ssp.utils.increaseCurrentFrame()
    # plt.ioff() 
    plt.show()
    
def processing_2():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
    fig, FigsAxes = plt.subplots(2,3)
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        # ssp.utils.force_zeroDoppler_4Simulation(path_d_drate_amp)
        # Channel_d_fd_amp = ssp.visualization.visualize_radar_path_d_drate_amp(path_d_drate_amp,1)
        radar_path_d_drate_amp(path_d_drate_amp,[fig,FigsAxes])
        ssp.utils.increaseCurrentFrame()
    # plt.show()
    

def radar_path_d_drate_amp(path_d_drate_amp,FigsAxes):
    alld = []
    m = path_d_drate_amp[0][0][0][0][0][0][0][3]
    for itx in range(len(path_d_drate_amp[0][0][0][0][0])):
        for irx in range(len(path_d_drate_amp[0][0])):
            for d_drate_amp in path_d_drate_amp[0][0][irx][0][0][itx]:
                if d_drate_amp[3]==m:
                    alld.append(d_drate_amp[0:3])
    alld = np.array(alld)
    FigsAxes[1][0,0].plot(alld[:,0])
    FigsAxes[1][0,1].plot(alld[:,1])
    FigsAxes[1][1,0].plot(alld[:,2])
    FigsAxes[1][1,1].plot(np.diff(alld[:,0]))
    FigsAxes[1][1,2].plot(np.diff(np.diff(alld[:,0])))
    image=ssp.visualization.captureFig(FigsAxes[0])
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('d drate ', image)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        return

    
    # plt.draw() 
    # plt.pause(0.1)

