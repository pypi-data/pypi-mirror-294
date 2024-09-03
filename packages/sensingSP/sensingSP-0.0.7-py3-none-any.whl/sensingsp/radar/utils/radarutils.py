import bpy
import numpy as np
from mathutils import Vector

LightSpeed = 299792458  # Speed of light in m/s

import numpy as np

def calculate_n_from_beamwidth(beamwidth):
    """
    Calculate the exponent n based on the beamwidth.
    A smaller beamwidth corresponds to a larger n.
    
    Parameters:
    beamwidth (float): Beamwidth in degrees.
    
    Returns:
    float: The calculated exponent n.
    """
    # n is inversely proportional to the beamwidth
    # This is an empirical relationship, adjust as needed for specific antennas
    n = 2 / (beamwidth / 60) ** 2
    return n

def antenna_gain_from_beamwidth(azimuth_angle, elevation_angle, max_gain, azimuth_beamwidth, elevation_beamwidth,antennaType):
    """
    Calculate the antenna gain based on input azimuth and elevation angles, using beamwidths.
    
    Parameters:
    azimuth_angle (float or np.array): The azimuth angle in degrees from the boresight.
    elevation_angle (float or np.array): The elevation angle in degrees from the boresight.
    max_gain (float): The maximum gain at 0 degrees, 0 degrees.
    azimuth_beamwidth (float): The azimuth beamwidth in degrees.
    elevation_beamwidth (float): The elevation beamwidth in degrees.
    
    Returns:
    float or np.array: The antenna gain at the given azimuth and elevation angles in dBi.
    """
    
    # Convert angles to radians
    azimuth_angle_rad = np.radians(azimuth_angle)
    # print(azimuth_angle)
    elevation_angle_rad = np.radians(elevation_angle)
    
    if antennaType=='Directional-Sinc':
        norm_azimuth = azimuth_angle_rad / np.radians(azimuth_beamwidth / 2)
        norm_elevation = elevation_angle_rad / np.radians(elevation_beamwidth / 2)
        
        gain_factor_azimuth = np.sinc(norm_azimuth / np.pi)
        gain_factor_elevation = np.sinc(norm_elevation / np.pi)
    else:
        # Calculate n for both azimuth and elevation based on beamwidths
        n_azimuth = calculate_n_from_beamwidth(azimuth_beamwidth)
        n_elevation = calculate_n_from_beamwidth(elevation_beamwidth)
        # Calculate the gain factors based on the angles and n values
        gain_factor_azimuth = np.abs(np.cos(azimuth_angle_rad)) ** n_azimuth
        gain_factor_elevation = np.abs(np.cos(elevation_angle_rad)) ** n_elevation
    
    # Total gain is the product of the gain factors and the maximum gain
    gain = np.abs(max_gain * gain_factor_azimuth * gain_factor_elevation)
    
    return gain

# # Example usage
# azimuth_angle = 10  # Example azimuth angle in degrees
# elevation_angle = 5  # Example elevation angle in degrees
# max_gain = 15  # Example maximum gain in dBi
# azimuth_beamwidth = 60  # Example azimuth beamwidth in degrees
# elevation_beamwidth = 30  # Example elevation beamwidth in degrees

# gain = antenna_gain_from_beamwidth(azimuth_angle, elevation_angle, max_gain, azimuth_beamwidth, elevation_beamwidth)
# print(f"Antenna Gain at ({azimuth_angle}°, {elevation_angle}°): {gain:.2f} dBi")


def predefined_array_configs_TI_Cascade_AWR2243(isuite, iradar, location, rotation, f0=70e9):  # 3 x 4
    Lambda = LightSpeed / f0
    Suitename = f'SuitePlane_{isuite}'
    Suite_obj = bpy.data.objects[Suitename]

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'RadarPlane_{isuite}_{iradar}_{0}'
    empty.parent = Suite_obj
    empty = setDefaults(empty,f0)

    s = 0.05
    Type = 'SPOT'

    tx_positions = [
        (0, 0),
        (-4, 0),
        (-8, 0),
        (-9, 1),
        (-10, 4),
        (-11, 6),
        (-12, 0),
        (-16, 0),
        (-20, 0),
        (-24, 0),
        (-28, 0),
        (-32, 0)
    ]

    for i, pos in enumerate(tx_positions):
        bpy.ops.object.light_add(type=Type, radius=1, location=(pos[0]*Lambda/2, pos[1]*Lambda/2, 0))
        tx = bpy.context.object
        tx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        tx.name = f'TX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        tx.parent = empty

    bx0 = -17
    bx = bx0
    by = 34
    s = 1

    rx_positions = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (11, 0),
        (11+1, 0),
        (11+2, 0),
        (11+3, 0),
        (46, 0),
        (46+1, 0),
        (46+2, 0),
        (46+3, 0),
        (53-3, 0),
        (53-2, 0),
        (53-1, 0),
        (53, 0)
    ]

    for i, pos in enumerate(rx_positions):
        bpy.ops.object.camera_add(location=( -(bx+pos[0])*Lambda/2, (by+pos[1])*Lambda/2, 0), rotation=(0, 0, 0))
        rx = bpy.context.object
        rx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        rx.name = f'RX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        rx.parent = empty
        rx.data.lens = 10
    return empty



def predefined_array_configs_LinearArray(isuite, iradar, location, rotation, f0=2.447e9,
                                         LinearArray_TXPos =[0],
                                         LinearArray_RXPos =[.56,.84,.98]):
    Lambda = LightSpeed / f0
    Suitename = f'SuitePlane_{isuite}'
    Suite_obj = bpy.data.objects[Suitename]

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'RadarPlane_{isuite}_{iradar}_{0}'
    empty.parent = Suite_obj
    empty = setDefaults(empty,f0)
    s = 0.05
    Type = 'SPOT'
    for i, pos in enumerate(LinearArray_TXPos):
        bpy.ops.object.light_add(type=Type, radius=1, location=(pos, 0, 0))
        tx = bpy.context.object
        tx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        tx.name = f'TX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        tx.parent = empty


    bx0 = 0
    bx = bx0
    by = 0
    s = 1

    rx_positions = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0)
    ]

    for i, pos in enumerate(LinearArray_RXPos):
        bpy.ops.object.camera_add(location=( pos, 0, 0), rotation=(0, 0, 0))
        rx = bpy.context.object
        rx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        rx.name = f'RX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        rx.parent = empty
        rx.data.lens = 10
    return empty

def predefined_array_configs_TI_IWR6843(isuite, iradar, location, rotation, f0=70e9):  # 3 x 4
    Lambda = LightSpeed / f0
    Suitename = f'SuitePlane_{isuite}'
    Suite_obj = bpy.data.objects[Suitename]

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'RadarPlane_{isuite}_{iradar}_{0}'
    empty.parent = Suite_obj
    empty = setDefaults(empty,f0)
    s = 0.05
    Type = 'SPOT'
    tx_positions = [
        (0, 0),
        (-4, 1),
        (-8, 0)
    ]

    for i, pos in enumerate(tx_positions):
        bpy.ops.object.light_add(type=Type, radius=1, location=(pos[0]*Lambda/2, pos[1]*Lambda/2, 0))
        tx = bpy.context.object
        tx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        tx.name = f'TX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        tx.parent = empty


    bx0 = -6
    bx = bx0
    by = 0
    s = 1

    rx_positions = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0)
    ]

    for i, pos in enumerate(rx_positions):
        bpy.ops.object.camera_add(location=( -(bx+pos[0])*Lambda/2, (by+pos[1])*Lambda/2, 0), rotation=(0, 0, 0))
        rx = bpy.context.object
        rx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        rx.name = f'RX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        rx.parent = empty
        rx.data.lens = 10
    return empty    
def predefined_array_configs_TI_IWR6843_az(isuite, iradar, location, rotation, f0=70e9):  # 3 x 4
    Lambda = LightSpeed / f0
    Suitename = f'SuitePlane_{isuite}'
    Suite_obj = bpy.data.objects[Suitename]

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'RadarPlane_{isuite}_{iradar}_{0}'
    empty.parent = Suite_obj
    empty = setDefaults(empty,f0)
    s = 0.05
    Type = 'SPOT'
    tx_positions = [
        (0, 0),
        (-4, 0),
        (-8, 0)
    ]

    for i, pos in enumerate(tx_positions):
        bpy.ops.object.light_add(type=Type, radius=1, location=(pos[0]*Lambda/2, pos[1]*Lambda/2, 0))
        tx = bpy.context.object
        tx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        tx.name = f'TX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        tx.parent = empty


    bx0 = -6
    bx = bx0
    by = 0
    s = 1

    rx_positions = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0)
    ]

    for i, pos in enumerate(rx_positions):
        bpy.ops.object.camera_add(location=( -(bx+pos[0])*Lambda/2, (by+pos[1])*Lambda/2, 0), rotation=(0, 0, 0))
        rx = bpy.context.object
        rx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        rx.name = f'RX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        rx.parent = empty
        rx.data.lens = 10
    return empty    

def predefined_array_configs_SISO(isuite, iradar, location, rotation, f0=70e9,Pulse1FMCW0=0):
    Lambda = LightSpeed / f0
    Suitename = f'SuitePlane_{isuite}'
    Suite_obj = bpy.data.objects[Suitename]

    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location, rotation=rotation, scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'RadarPlane_{isuite}_{iradar}_{0}'
    empty.parent = Suite_obj
    empty = setDefaults(empty,f0)
    if Pulse1FMCW0 == 1 :
        empty['RadarMode']='Pulse'
        empty['PulseWaveform']='WaveformFile.txt'
        
        empty['Fs_MHz']=1500
        empty['Ts_ns']=1000/empty['Fs_MHz']
        empty['Range_End']=100
        
    
    s = 0.05
    Type = 'SPOT'
    tx_positions = [
        (0, 0)
    ]

    for i, pos in enumerate(tx_positions):
        bpy.ops.object.light_add(type=Type, radius=1, location=(pos[0]*Lambda/2, pos[1]*Lambda/2, 0))
        tx = bpy.context.object
        tx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        tx.name = f'TX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        tx.parent = empty


    bx0 = -1
    bx = bx0
    by = 0
    s = 1

    rx_positions = [
        (0, 0)
    ]

    for i, pos in enumerate(rx_positions):
        bpy.ops.object.camera_add(location=( -(bx+pos[0])*Lambda/2, (by+pos[1])*Lambda/2, 0), rotation=(0, 0, 0))
        rx = bpy.context.object
        rx.scale = (s*Lambda/2, s*Lambda/2, s*Lambda/2)
        rx.name = f'RX_{isuite}_{iradar}_{1}_{0}_{i+1:05}'
        rx.parent = empty
        rx.data.lens = 10
    return empty
    
def setDefaults(empty,f0):
    empty["Transmit_Power_dBm"] = 12
    empty["Transmit_Antenna_Element_Pattern"] = "Omni"
    empty["Transmit_Antenna_Element_Gain_db"] = 3
    empty["Transmit_Antenna_Element_Azimuth_BeamWidth_deg"] = 120
    empty["Transmit_Antenna_Element_Elevation_BeamWidth_deg"] = 120
    empty["Receive_Antenna_Element_Gain_db"] = 0
    empty["Receive_Antenna_Element_Pattern"] = "Omni"
    empty["Receive_Antenna_Element_Azimuth_BeamWidth_deg"] = 120
    empty["Receive_Antenna_Element_Elevation_BeamWidth_deg"] = 120
    empty["Center_Frequency_GHz"] = f0/1e9
    empty['PRI_us']=70
    empty['Fs_MHz']=5
    empty['Ts_ns']=1000/empty['Fs_MHz']
    empty['NPulse'] = 3 * 64
    empty['N_ADC']  = 256
    empty['RangeWindow']  = 'Hamming'
    empty['DopplerWindow']  = 'Hamming'
    # empty['N_FFT_ADC']  = 128
    # empty['N_FFT_Doppler']  = 128
    empty['Lambda_mm']=1000*LightSpeed/empty["Center_Frequency_GHz"]/1e9
    empty['FMCW_ChirpTime_us'] = 60
    empty['FMCW_Bandwidth_GHz'] = 1
    empty['Tempreture_K'] = 290
    empty['FMCW_ChirpSlobe_MHz_usec'] = 1000*empty['FMCW_Bandwidth_GHz']/empty['FMCW_ChirpTime_us']
    empty['RangeFFT_OverNextP2'] = 2
    empty['Range_Start']=0
    empty['Range_End']=100
    empty['CFAR_RD_guard_cells']=2
    empty['CFAR_RD_training_cells']=10
    empty['CFAR_RD_false_alarm_rate']=1e-3
    empty['STC_Enabled']=False #
    empty['MTI_Enabled']=False #
    empty['DopplerFFT_OverNextP2']=3
    empty['AzFFT_OverNextP2']=2
    empty['ElFFT_OverNextP2']=3
    empty['CFAR_Angle_guard_cells']=1
    empty['CFAR_Angle_training_cells']=3
    empty['CFAR_Angle_false_alarm_rate']=.1
    empty["FMCW"] = True
    empty['ADC_peak2peak']=2
    empty['ADC_levels']=256
    empty['ADC_ImpedanceFactor']=300
    empty['ADC_LNA_Gain_dB']=50
    empty['RF_NoiseFiguredB']=5
    empty['RF_AnalogNoiseFilter_Bandwidth_MHz']=10
    empty['ADC_SaturationEnabled']=False
    empty['RadarMode']='FMCW'# 'Pulse' 'CW'
    empty['PulseWaveform']='WaveformFile.txt'
    
    empty['t_start_radar']=0
    empty['MaxRangeScatter']=1e12
    empty['SaveSignalGenerationTime']=True
    empty['continuousCPIsTrue_oneCPIpeerFrameFalse']=False
    # empty['t_start_radar']=0
    
    
    
    # empty['Timing'] = RadarTiming(t_start_radar=0.0, t_start_manual_restart_tx=1.0, t_last_pulse=10.0,
    #                 t_current_pulse=5.0, pri_sequence=[0.1, 0.2, 0.15], n_pulse=7, n_last_cpi=1024)

    
    return empty
    # , levels,,,

def rangeResolution_and_maxUnambigiousRange(radar):
    if radar['RadarMode']=='FMCW':
        BW = radar['FMCW_ChirpSlobe_MHz_usec']*1e12*radar['N_ADC']*radar['Ts_ns']*1e-9
        Res=3e8/(2*BW)
        MaxR =  radar['N_ADC']*Res
        return Res,MaxR
    return None