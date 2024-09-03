"""_summary_
sensing sp 
"""
from .constants import *
from . import integratedSensorSuite
from . import utils
from . import environment
from . import radar
from . import camera
from . import lidar
from . import ris
from . import probe
from . import raytracing
from . import visualization
from .config import Config
config = Config()

# import sensingsp as ssp
# import bpy

# from matplotlib import pyplot as plt
# from numba import cuda

# sspconfig.CUDA_is_available = cuda.is_available()

# ssp.Paths = []
# ssp.CurrentFrame = 1
# ssp.RadarSpecifications = []
# ssp.suite_information = []

# ssp.Detection_Parameters_xyz_start=[-.5, -2, -.2]
# ssp.Detection_Parameters_xyz_N=[10, 4, 5]
# ssp.Detection_Parameters_gridlen=.1

# # ssp.suite_information_finder = ssp.environment.BlenderSuiteFinder()
# # ssp.geocalculator = ssp.raytracing.BlenderGeometry.BlenderGeometry()
# # ssp.rayTracingFunctions = ssp.raytracing.ra.RayTracingFunctions()


# def define_axes(option = 1):
#     if option == 1:
#         fig, ssp.ax = plt.subplots(3,4)
#         ssp.ax[2, 2] = fig.add_subplot(3, 4, 9 + 2 , projection='3d')
#         ssp.ax[2, 3] = fig.add_subplot(3, 4, 9 + 3 , projection='3d')
#     elif option == 2:
#         fig, ssp.ax = plt.subplots(3,3)
#         ssp.ax[2, 1] = fig.add_subplot(3, 3, 6 + 2 , projection='3d')
#         ssp.ax[2, 2] = fig.add_subplot(3, 3, 6 + 3 , projection='3d')
#         ssp.ax[1,2] = fig.add_subplot(3, 3, 3 + 3 , polar=True)
#         ssp.ax[2,0] = fig.add_subplot(3, 3, 6 + 1 , polar=True)
#     elif option == 3:
#         ssp.Video_Figs = []
#         ssp.Video_Axes = []
#         width_in_pixels = 1920
#         height_in_pixels = 1080
#         dpi = 300
#         width_in_inches = width_in_pixels / dpi
#         height_in_inches = height_in_pixels / dpi
#         for _ in range(4):
#             fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)
#             ssp.Video_Figs.append(fig)
#             ssp.Video_Axes.append(ax)
#         ssp.Video_images=[]
#         for fig in ssp.Video_Figs:
#             ssp.Video_images.append(ssp.visualization.captureFig(fig=fig))
#         ssp.Video_video_directory = '.'
#         ssp.Video_fps = 30
#         ssp.Video_videos,ssp.Video_videos_WH=ssp.visualization.firsttime_init_GridVideoWriters(ssp.Video_images,ssp.Video_video_directory,ssp.Video_fps)

    
#     if os.name=='nt':
#         figManager = plt.get_current_fig_manager()
#         figManager.window.showMaximized()
# def setDopplerProcessingMethod_FFT_Winv(method):
#     ssp.DopplerProcessingMethod_FFT_Winv = method
# def restart():
#     ssp.CurrentFrame = bpy.context.scene.frame_start
    
# def run():
#     if ssp.CurrentFrame + 1 > bpy.context.scene.frame_end:
#         return False
#     return True
    
    