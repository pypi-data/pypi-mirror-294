import sensingsp as ssp
from ..environment import BlenderSuiteFinder
from ..radar.utils import MIMO_Functions
import os
import sys
import bpy
import numpy as np
from mathutils import Vector
import bmesh
def delete_all_objects():
    view_layer = bpy.context.view_layer
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.name in view_layer.objects.keys():
            view_layer.objects.active = obj
            obj.select_set(True)
    if "Simulation Settings" in bpy.data.objects:
      bpy.data.objects["Simulation Settings"].select_set(False)
    bpy.ops.object.delete()
def save_Blender(folder="",file="save_frompython.blend"):
  if folder == "":
    folder = ssp.config.temp_folder

  bpy.ops.wm.save_as_mainfile(filepath = os.path.join(folder, file))
  print(os.path.join(folder, file))
  
def getRadarSpecs():
  return ssp.RadarSpecifications

def useCUDA():
    bpy.data.objects["Simulation Settings"]["CUDA SignalGeneration Enabled"] = True
def set_frame_start_end(start=1,end=2):
    
    bpy.context.scene.frame_start   =   start
    bpy.context.scene.frame_end     =   end
def increaseCurrentFrame(step=1):
    ssp.config.CurrentFrame += step
    c= sys.executable.lower()
    if "blender" in c:
      bpy.context.view_layer.update()
      bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def total_paths(path_d_drate_amp):
  N=0
  for isrx,suiteRX_d_drate_amp in path_d_drate_amp.items():
    for irrx,radarRX_d_drate_amp in suiteRX_d_drate_amp.items():
      for irx,RX_d_drate_amp in radarRX_d_drate_amp.items():
        for istx,suiteTX_d_drate_amp in RX_d_drate_amp.items():
          for irtx,radarTX_d_drate_amp in suiteTX_d_drate_amp.items():
            for itx,TX_d_drate_amp in radarTX_d_drate_amp.items():
              N+=len(TX_d_drate_amp)
  return N
def force_zeroDoppler_4Simulation(path_d_drate_amp):
  d=[]
  for isrx,suiteRX_d_drate_amp in path_d_drate_amp.items():
    for irrx,radarRX_d_drate_amp in suiteRX_d_drate_amp.items():
      for irx,RX_d_drate_amp in radarRX_d_drate_amp.items():
        for istx,suiteTX_d_drate_amp in RX_d_drate_amp.items():
          for irtx,radarTX_d_drate_amp in suiteTX_d_drate_amp.items():
            for itx,TX_d_drate_amp in radarTX_d_drate_amp.items():
              for d_drate_amp in TX_d_drate_amp:
                d_drate_amp[1]=0
                d.append(d_drate_amp[0])
  return np.array(d)

def trimUserInputs():
    current_working_directory = os.getcwd()
    if "Simulation Settings" in bpy.data.objects:
        sim_axes = bpy.data.objects["Simulation Settings"]
        RenderBlenderFrames = bpy.data.objects["Simulation Settings"]["Render Blender Frames"]
        video_directory = bpy.data.objects["Simulation Settings"]["Video Directory"]
        open_output_folder = bpy.data.objects["Simulation Settings"]["Open Output Folder"]
    else:
        RenderBlenderFrames = True
        video_directory = current_working_directory
        open_output_folder = True
    RadarSpecifications = []
    suite_information = BlenderSuiteFinder().find_suite_information()
    
    ssp.suite_information = suite_information
    # suite_information= finder.find_suite_information()
    mimo_Functions = MIMO_Functions()
    for isuite,suiteobject in enumerate(suite_information):
      radarSpecifications=[]
      for iradar,radarobject in enumerate(suiteobject['Radar']):
        specifications={}

        # empty["Transmit_Power_dBm"] = 12
        # empty["Center_Frequency_GHz"] = f0/1e9
        # empty['Fs_MHz']=5
        # empty['FMCW_ChirpTime_us'] = 60 automatically set to = N_ADC * Ts

        specifications['PRI']=radarobject['GeneralRadarSpec_Object']['PRI_us']*1e-6
        specifications['Ts']=radarobject['GeneralRadarSpec_Object']['Ts_ns']*1e-9
        specifications['NPulse'] = radarobject['GeneralRadarSpec_Object']['NPulse']
        specifications['N_ADC']  = radarobject['GeneralRadarSpec_Object']['N_ADC']
        specifications['Lambda']=radarobject['GeneralRadarSpec_Object']['Lambda_mm']*1e-3
        specifications['RadarMode']=radarobject['GeneralRadarSpec_Object']['RadarMode']
        specifications['PulseWaveform']=radarobject['GeneralRadarSpec_Object']['PulseWaveform']
        specifications['FMCW_Bandwidth']=radarobject['GeneralRadarSpec_Object']['FMCW_Bandwidth_GHz']*1e9
        specifications['Tempreture_K']=radarobject['GeneralRadarSpec_Object']['Tempreture_K']
        specifications['FMCW_ChirpSlobe'] = radarobject['GeneralRadarSpec_Object']['FMCW_ChirpSlobe_MHz_usec']*1e12
        # specifications['PrecodingMatrix'] = np.eye(len(Suite_Position[isuite]['Radar'][iradar]['TX-Position']),dtype=np.complex128)
        specifications['M_TX'] = len(radarobject['TX'])
        specifications['N_RX'] = len(radarobject['RX'])
        specifications['MIMO_Tech'] = 'TDM'
        specifications['RangeFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['RangeFFT_OverNextP2']
        specifications['Range_Start'] = radarobject['GeneralRadarSpec_Object']['Range_Start']
        specifications['Range_End'] = radarobject['GeneralRadarSpec_Object']['Range_End']
        specifications['CFAR_RD_guard_cells'] = radarobject['GeneralRadarSpec_Object']['CFAR_RD_guard_cells']
        specifications['CFAR_RD_training_cells'] = radarobject['GeneralRadarSpec_Object']['CFAR_RD_training_cells']
        specifications['CFAR_RD_false_alarm_rate'] = radarobject['GeneralRadarSpec_Object']['CFAR_RD_false_alarm_rate']
        specifications['STC_Enabled'] = radarobject['GeneralRadarSpec_Object']['STC_Enabled']
        specifications['MTI_Enabled'] = radarobject['GeneralRadarSpec_Object']['MTI_Enabled']
        specifications['DopplerFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['DopplerFFT_OverNextP2']
        specifications['AzFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['AzFFT_OverNextP2']
        specifications['ElFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['ElFFT_OverNextP2']
        specifications['CFAR_Angle_guard_cells'] = radarobject['GeneralRadarSpec_Object']['CFAR_Angle_guard_cells']
        specifications['CFAR_Angle_training_cells'] = radarobject['GeneralRadarSpec_Object']['CFAR_Angle_training_cells']
        specifications['CFAR_Angle_false_alarm_rate'] = radarobject['GeneralRadarSpec_Object']['CFAR_Angle_false_alarm_rate']
        specifications['PrecodingMatrix'] = mimo_Functions.AD_matrix(NPulse=specifications['NPulse'],
                                                                    M=len(radarobject['TX']),
                                                                    tech=specifications['MIMO_Tech'])
        specifications['ADC_peak2peak'] = radarobject['GeneralRadarSpec_Object']['ADC_peak2peak']
        specifications['ADC_levels'] = radarobject['GeneralRadarSpec_Object']['ADC_levels']
        specifications['ADC_ImpedanceFactor'] = radarobject['GeneralRadarSpec_Object']['ADC_ImpedanceFactor']
        specifications['ADC_LNA_Gain'] = 10**(radarobject['GeneralRadarSpec_Object']['ADC_LNA_Gain_dB']/10)
        specifications['ADC_SaturationEnabled'] = radarobject['GeneralRadarSpec_Object']['ADC_SaturationEnabled']
        specifications['RF_NoiseFiguredB'] = radarobject['GeneralRadarSpec_Object']['RF_NoiseFiguredB']
        specifications['RF_AnalogNoiseFilter_Bandwidth'] = radarobject['GeneralRadarSpec_Object']['RF_AnalogNoiseFilter_Bandwidth_MHz']*1e6
        k=0
        global_location_Center = Vector((0,0,0))
        global_location_TX = []
        for itx,txobj in enumerate(radarobject['TX']):
          global_location, global_rotation, global_scale = txobj.matrix_world.decompose()
          global_location_TX.append(global_location)
          global_location_Center += global_location
          k+=1
        global_location_RX = []
        for irx,rxobj in enumerate(radarobject['RX']):
          global_location, global_rotation, global_scale = rxobj.matrix_world.decompose()
          global_location_RX.append(global_location)
          global_location_Center += global_location
          k+=1
        global_location_Center /= k
        specifications['global_location_TX_RX_Center'] = [global_location_TX,global_location_RX,global_location_Center]
        azindex = []
        elindex = []
        for itx,txobj in enumerate(radarobject['TX']):
          # global_location, global_rotation, global_scale = txobj.matrix_world.decompose()
          local_location, local_rotation, local_scale = txobj.matrix_local.decompose()
          local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000)* 2
          azTx=round(local_location_HW.x)
          elTx=round(local_location_HW.y)
          # print("itx,local_location:",itx,local_location,txobj.name)
          for irx,rxobj in enumerate(radarobject['RX']):
              local_location, local_rotation, local_scale = rxobj.matrix_local.decompose()
              local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000) * 2
              azRx=round(local_location_HW.x)
              elRx=round(local_location_HW.y)
              # print(iradar,azTx+azRx,elRx+elTx)
              azindex.append(azTx+azRx)
              elindex.append(elTx+elRx)
        #       print("irx,local_location:",irx,local_location,rxobj.name)
        # print("azindex:",azindex)
        # print("elindex:",elindex)


        azindex = azindex - np.min(azindex)+1
        elindex = elindex - np.min(elindex)+1
        antennaIndex2VAx = np.zeros((len(radarobject['TX']),len(radarobject['RX'])))
        antennaIndex2VAy = np.zeros((len(radarobject['TX']),len(radarobject['RX'])))
        k=0
        for itx in range(antennaIndex2VAx.shape[0]):
          for irx in range(antennaIndex2VAx.shape[1]):
            antennaIndex2VAx[itx,irx] = azindex[k]-1
            antennaIndex2VAy[itx,irx] = elindex[k]-1
            k+=1

        specifications['MIMO_AntennaIndex2VA']=[antennaIndex2VAx,antennaIndex2VAy,np.max(elindex),np.max(azindex)]
        antenna_Pos0_Wavelength_TX=[]
        for itx,txobj in enumerate(radarobject['TX']):
          local_location, local_rotation, local_scale = txobj.matrix_local.decompose()
          local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000)
          antenna_Pos0_Wavelength_TX.append(local_location_HW)
        antenna_Pos0_Wavelength_RX=[]
        for irx,rxobj in enumerate(radarobject['RX']):
              local_location, local_rotation, local_scale = rxobj.matrix_local.decompose()
              local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000)
              antenna_Pos0_Wavelength_RX.append(local_location_HW)
        specifications['antenna_Pos0_Wavelength']=[antenna_Pos0_Wavelength_TX,antenna_Pos0_Wavelength_RX]


        PosIndex = []
        for itx,txobj in enumerate(radarobject['TX']):
          # global_location, global_rotation, global_scale = txobj.matrix_world.decompose()
          local_location, local_rotation, local_scale = txobj.matrix_local.decompose()
          local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000)* 2
          azTx=local_location_HW.x
          elTx=local_location_HW.y
          # print("itx,local_location:",itx,local_location,txobj.name)
          for irx,rxobj in enumerate(radarobject['RX']):
              local_location, local_rotation, local_scale = rxobj.matrix_local.decompose()
              local_location_HW = local_location / (radarobject['GeneralRadarSpec_Object']['Lambda_mm']/1000) * 2
              azRx=local_location_HW.x
              elRx=local_location_HW.y
              PosIndex.append([azTx+azRx,elTx+elRx,itx,irx])
        specifications['Local_location_TXplusRX_Center'] = PosIndex

        # x = np.zeros((np.max(elindex),np.max(azindex)))
        # for itx,txobj in enumerate(radarobject['TX']):
        #   for irx,rxobj in enumerate(radarobject['RX']):
        #     x[int(antennaIndex2VAy[itx,irx]),int(antennaIndex2VAx[itx,irx])]=1

        # print(iradar,azindex,elindex,np.max(azindex),np.max(elindex),x)
        # specifications['RangePulseRX']= np.zeros((specifications['N_ADC'],specifications['NPulse'],len(Suite_Position[isuite]['Radar'][iradar]['RX-Position'])),dtype=np.complex128)
        
        specifications['RadarTiming'] = RadarTiming(t_start_radar=radarobject['GeneralRadarSpec_Object']['t_start_radar'], 
                                                    t_start_manual_restart_tx=0,
                                                    t_last_pulse=0.0,
                                                    t_current_pulse=0, 
                                                    pri_sequence=[specifications['PRI']], 
                                                    n_pulse=0,
                                                    n_last_cpi=0)
        specifications['CPI_Buffer']=[]
        specifications['SaveSignalGenerationTime']=radarobject['GeneralRadarSpec_Object']['SaveSignalGenerationTime']
        specifications['MaxRangeScatter']=radarobject['GeneralRadarSpec_Object']['MaxRangeScatter']
        specifications['continuousCPIsTrue_oneCPIpeerFrameFalse']=radarobject['GeneralRadarSpec_Object']['continuousCPIsTrue_oneCPIpeerFrameFalse']

        
        radarSpecifications.append(specifications)
      RadarSpecifications.append(radarSpecifications)
      

    
    # if os.path.exists('frames'):
    #     shutil.rmtree('frames')
    # os.makedirs('frames')
    ssp.RadarSpecifications = RadarSpecifications

def open_Blend(file):
  bpy.ops.wm.open_mainfile(filepath=file)
def applyDecimate(obj, decimateFactor):
    if obj.data.shape_keys is not None:
        bpy.context.view_layer.objects.active = obj 
        blocks = obj.data.shape_keys.key_blocks
        for ind in reversed(range(len(blocks))):
            obj.active_shape_key_index = ind
            bpy.ops.object.shape_key_remove()
    if len(obj.data.vertices) * decimateFactor > 10: 
        decimate_mod = obj.modifiers.new(type='DECIMATE', name='decimate')
        decimate_mod.ratio = decimateFactor
        decimate_mod.use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier='decimate')

def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if(m.type=="DECIMATE"):
            obj.modifiers.remove(modifier=m)

def mesh2triangles(mesh):
    out = []
    mesh.calc_loop_triangles()
    for tri in mesh.loop_triangles: 
        xyz0 = mesh.vertices[tri.vertices[0]].co.to_tuple()
        xyz1 = mesh.vertices[tri.vertices[1]].co.to_tuple()
        xyz2 = mesh.vertices[tri.vertices[2]].co.to_tuple()
        out.append([xyz0,xyz1,xyz2])
    return out
        

def exportBlenderTriangles():
  frame = ssp.config.CurrentFrame
  out = []
  bpy.context.scene.frame_set(frame)
  bpy.context.view_layer.update()
  for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
      depgraph = bpy.context.evaluated_depsgraph_get()
      bm = bmesh.new()
      bm.verts.ensure_lookup_table()
      bm.from_object(obj, depgraph)
      bm.transform(obj.matrix_world)
      mesh = bpy.data.meshes.new('new_mesh')
      bm.to_mesh(mesh)
      trianglesList=mesh2triangles(mesh)
      out.append(trianglesList)
  return out

def decimate_scene(decimation_ratio = 0.5):
  for obj in bpy.context.selected_objects:
      if obj.type == 'MESH':
          # Add a Decimate modifier
          decimate_modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
          decimate_modifier.ratio = decimation_ratio
          
          # Apply the Decimate modifier
          bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)


def plot1D(ax,x,xlabel="",ylabel="",title="",ylim=[]):
  ax.cla()
  ax.plot(x)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  if len(ylim)==2:
    ax.set_ylim(ylim)
  ax.grid(True)
def plot2D(ax,x,xlabel="",ylabel="",title=""):
  ax.cla()
  ax.imshow(x)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  
  
class RadarTiming:
    def __init__(self, t_start_radar: float, t_start_manual_restart_tx: float, t_last_pulse: float,
                 t_current_pulse: float, pri_sequence: list, n_pulse: int, n_last_cpi: int):
        self.t_start_radar = np.float64(t_start_radar)
        self.t_start_manual_restart_tx = np.float64(t_start_manual_restart_tx)
        self.t_last_pulse = np.float64(t_last_pulse)
        self.t_current_pulse = np.float64(t_current_pulse)
        self.pri_sequence = np.array(pri_sequence, dtype=np.float64)
        self.n_pulse = n_pulse
        self.n_last_cpi = np.int64(n_last_cpi)
        self.Frame_PulseTimes = np.array([],dtype=np.float64)
        self.Started = False

    def update(self,currentTime,FPS): # [ )
      self.Frame_PulseTimes = np.array([],dtype=np.float64)
      T = 1/float(FPS) # 1/24 = 0.04167
      if self.t_start_radar >= currentTime+T:
        return
      if self.Started == False:
        if self.t_start_radar >= currentTime:
          self.Started = True
          self.t_current_pulse = self.t_start_radar
          self.n_pulse = 1
          self.Frame_PulseTimes = np.append(self.Frame_PulseTimes, self.t_current_pulse)
      if self.Started == False:
        return
        
      while 1:
        k=0
        CurrentPRI = self.pri_sequence[k]
        if self.t_current_pulse + CurrentPRI >= currentTime+T:
          break
        self.t_current_pulse += CurrentPRI
        self.n_pulse+=1
        self.Frame_PulseTimes = np.append(self.Frame_PulseTimes, self.t_current_pulse)
        
        
