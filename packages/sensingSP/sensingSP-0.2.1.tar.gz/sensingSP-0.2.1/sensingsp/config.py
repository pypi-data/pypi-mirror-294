import bpy
from matplotlib import pyplot as plt
from numba import cuda
import os
import platform
import subprocess
import tempfile
from . import visualization
class Config():
    def __init__(self):
        self.CUDA_is_available = cuda.is_available()
        self.system_type = self.get_system_type()
        self.latex = self.check_latex_installed()
        if not self.latex and self.system_type == 'Google Colab':
            print("use ssp.config.install_latex_in_colab() to install latex")
            self.latex = self.check_latex_installed()
        if self.latex:
            plt.rcParams['text.usetex'] = True
        else:
            plt.rcParams['text.usetex'] = False
        self.ui_available = self.check_ui_available()
        self.temp_folder = self.create_temp_folder('SensingSP')
        self.Paths = []
        self.CurrentFrame = 1
        self.CurrentTime  = 0
        self.StartTime  = 0
        
        
        self.RadarSpecifications = []
        self.suite_information = []
        
        self.directReceivefromTX = False

        self.Detection_Parameters_xyz_start=[-.5, -2, -.2]
        self.Detection_Parameters_xyz_N=[10, 4, 5]
        self.Detection_Parameters_gridlen=.1
        self.DopplerProcessingMethod_FFT_Winv = 1
        self.ax = None
        # self.suite_information_finder = self.environment.BlenderSuiteFinder()
        # self.geocalculator = self.raytracing.BlenderGeometry.BlenderGeometry()
        # self.rayTracingFunctions = self.raytracing.ra.RayTracingFunctions()
    def release_videofigures(self):
        for video in self.Video_videos:
            video.release()
    def define_videofigures(self, N = 4, width_in_pixels = 1920 , height_in_pixels = 1080, dpi = 300, Video_fps = 30 ,video_directory = '.'):
        self.Video_Figs = []
        self.Video_Axes = []
        width_in_inches = width_in_pixels / dpi
        height_in_inches = height_in_pixels / dpi
        for _ in range(N):
            fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)
            self.Video_Figs.append(fig)
            self.Video_Axes.append(ax)
            plt.close(fig) 
        self.Video_images=[]
        for fig in self.Video_Figs:
            self.Video_images.append(visualization.captureFig(fig=fig))
        self.Video_video_directory = video_directory
        self.Video_fps = Video_fps
        self.Video_videos,self.Video_videos_WH=visualization.firsttime_init_GridVideoWriters(self.Video_images,self.Video_video_directory,self.Video_fps)

    def define_axes(self,option = 1):
        if option == 1:
            fig, self.ax = plt.subplots(3,4)
            self.ax[2, 2] = fig.add_subplot(3, 4, 9 + 2 , projection='3d')
            self.ax[2, 3] = fig.add_subplot(3, 4, 9 + 3 , projection='3d')
        elif option == 2:
            fig, self.ax = plt.subplots(3,3)
            self.ax[2, 1] = fig.add_subplot(3, 3, 6 + 2 , projection='3d')
            self.ax[2, 2] = fig.add_subplot(3, 3, 6 + 3 , projection='3d')
            self.ax[1,2] = fig.add_subplot(3, 3, 3 + 3 , polar=True)
            self.ax[2,0] = fig.add_subplot(3, 3, 6 + 1 , polar=True)
        elif option == 3:
            self.Video_Figs = []
            self.Video_Axes = []
            width_in_pixels = 1920
            height_in_pixels = 1080
            dpi = 300
            width_in_inches = width_in_pixels / dpi
            height_in_inches = height_in_pixels / dpi
            for _ in range(4):
                fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)
                self.Video_Figs.append(fig)
                self.Video_Axes.append(ax)
            self.Video_images=[]
            for fig in self.Video_Figs:
                self.Video_images.append(visualization.captureFig(fig=fig))
            self.Video_video_directory = '.'
            self.Video_fps = 30
            self.Video_videos,self.Video_videos_WH=visualization.firsttime_init_GridVideoWriters(self.Video_images,self.Video_video_directory,self.Video_fps)

        
        # if os.name=='nt':
        #     figManager = plt.get_current_fig_manager()
        #     figManager.window.showMaximized()
    def setDopplerProcessingMethod_FFT_Winv(self,method):
        self.DopplerProcessingMethod_FFT_Winv = method
    def restart(self):
        self.CurrentFrame = bpy.context.scene.frame_start
        self.CurrentFrame = 1
        self.StartTime  = 0
        # self.CurrentTime  += float(bpy.context.scene.render.fps)
        self.CurrentTime  = self.StartTime + (self.CurrentFrame-1) / float(bpy.context.scene.render.fps)
        self.NextTime  = self.StartTime + (self.CurrentFrame+0) / float(bpy.context.scene.render.fps)
        self.PreTime  = self.StartTime + (self.CurrentFrame-2) / float(bpy.context.scene.render.fps)
    def run(self):
        self.CurrentTime  = self.StartTime + (self.CurrentFrame-1) / float(bpy.context.scene.render.fps)
        self.NextTime  = self.StartTime + (self.CurrentFrame+0) / float(bpy.context.scene.render.fps)
        self.PreTime  = self.StartTime + (self.CurrentFrame-2) / float(bpy.context.scene.render.fps)
        if self.CurrentFrame + 1 > bpy.context.scene.frame_end:
            return False
        return True
    def get_system_type(self):
        if 'COLAB_GPU' in os.environ or 'COLAB_TPU' in os.environ:
            return 'Google Colab'
        system = platform.system()
        if system == 'Windows':
            return 'Windows'
        elif system == 'Darwin':
            return 'macOS'
        elif system == 'Linux':
            if os.path.isfile('/etc/lsb-release'):
                with open('/etc/lsb-release') as f:
                    if 'Ubuntu' in f.read():
                        return 'Ubuntu'
            return 'Linux'
        else:
            return 'Unknown'
    def check_latex_installed(self):
        try:
            # Run the command 'pdflatex --version' to check if LaTeX is installed
            subprocess.run(['pdflatex', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    def install_latex_in_colab(self):
        print("Installing LaTeX in Google Colab...")
        subprocess.run(['apt-get', 'update'], check=True)
        subprocess.run(['apt-get', 'install', '-y', 'texlive', 'texlive-latex-extra', 'texlive-xetex', 'latexmk'], check=True)
    def check_ui_available(self):
        try:
            import matplotlib.pyplot as plt
            if 'DISPLAY' not in os.environ and platform.system() != 'Windows':
                # No display variable and not on Windows
                plt.switch_backend('Agg')  # Use a non-interactive backend
                return False
            else:
                # Try to use a backend that requires a display
                # plt.figure()
                return True
        except Exception:
            return False
    def create_temp_folder(self,folder_name):
        temp_dir = tempfile.gettempdir()
        folder_path = os.path.join(temp_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path