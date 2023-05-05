import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk
import matplotlib.pyplot as plt
import os
from PupilParam import *
from tkinter import simpledialog
import sys
import datetime as time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

import pandas as pd

global SYSPARAMS
import tkinter.filedialog
import tkinter.messagebox
import traceback
import json
import scipy.io as sio
from pathlib import Path
import io

import base64

"""  displaying error messages in GUI"""
def exception_troubleshoot(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            traceback.print_exception(*sys.exc_info())
            tkinter.messagebox.showerror(message=str(e) + '\n (Full traceback printed in console.)')

    return wrapper


class ProjectorGUI:
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.geometry('900x600')
        self.tk_root.title('PupilVideoTrackingV2')
        self.type_pupil_file_name_prefix = ""
        self.pupil_param = None
        self.PupilTracker = None

        # Create top, left, middle, and right frames formatting
        top_frame = tk.Frame(self.tk_root, bg="orange")
        top_frame.pack(side="top", fill="both")
        self.make_top_frame(top_frame)

        # left
        left_frame = tk.Frame(self.tk_root, bg="blue")
        left_frame.pack(side="left", expand=True, fill='both')
        self.make_left_frame(left_frame)

        #middle
        middle_frame = tk.Frame(self.tk_root, bg="yellow")
        middle_frame.pack(side="left", expand=True, fill='both')
        self.make_middle_frame(middle_frame)

        # right
        right_frame = tk.Frame(self.tk_root,  bg="brown")
        right_frame.pack(side="left", expand=True, fill='both')
        self.make_right_frame(right_frame)

    def make_top_frame(self, top_frame):
        # top
        self.tk_quit_button = tk.Button(top_frame, text="Quit", command=self.tk_quit)
        self.tk_quit_button.pack(side='left', expand=True, fill='both')
        self.tk_start_video_button = tk.Button(top_frame, text="Start Video", command=self.tk_start_video)
        self.tk_start_video_button.pack(side='left', expand=True, fill='both')
        self.tk_set_reference_button = tk.Button(top_frame, text="Set Reference", command=self.tk_set_reference)
        self.tk_set_reference_button.pack(side='left', expand=True, fill='both')
        self.tk_load_reference_button = tk.Button(top_frame, text="Load Reference", command=self.tk_load_reference)
        self.tk_load_reference_button.pack(side='left', expand=True, fill='both')
        self.tk_disable_tracking_button = tk.Button(top_frame, text="Disable Tracking Button",
                                                    command=self.tk_disable_tracking)
        self.tk_disable_tracking_button.pack(side='left', expand=True, fill='both')
        self.tk_zoom_in_button = tk.Button(top_frame, text="Zoom In", command=self.tk_zoom_in)
        self.tk_zoom_in_button.pack(side='left', expand=True, fill='both')
        self.tk_draw_be_button = tk.Button(top_frame, text="Draw BE", command=self.tk_draw_be)
        self.tk_draw_be_button.pack(side='left', expand=True, fill='both')

    def make_left_frame(self, left_frame):

        # left
        self.tk_sync_save_button = tk.Button(left_frame, text="Sync Save", command=self.tk_sync_save)
        self.tk_sync_save_button.pack(expand=True)
        self.tk_save_video_button = tk.Button(left_frame, text="Save Video", command=self.tk_save_video)
        self.tk_save_video_button.pack(expand=True)

        ## save video settings
        save_video_frame = tk.Frame(left_frame, bg="orange", highlightbackground="black", highlightthickness=2)
        save_video_frame.pack(side="top", expand=True, fill='both')
        self.tk_save_video_settings_label = tk.Label(save_video_frame, text="Save Video Settings")
        self.tk_save_video_settings_label.pack(side="top")

        save_video_frame_left = tk.Frame(save_video_frame)
        save_video_frame_left.pack(side="left", expand=True, fill='both')
        save_video_frame_right = tk.Frame(save_video_frame)
        save_video_frame_right.pack(side="left", expand=True, fill='both')


        self.tk_secs_label = tk.Label(save_video_frame_left, text="Secs")
        self.tk_secs_label.pack(side='top', expand=True, fill='both')
        self.tk_secs_entry = tk.Entry(save_video_frame_right, textvariable=self.tk_secs)
        self.tk_secs_entry.pack(side='top', expand=True, fill='both')
        self.tk_fps_label = tk.Label(save_video_frame_left, text="FPS")
        self.tk_fps_label.pack(side='bottom', expand=True, fill='both')
        self.tk_fps_entry = tk.Entry(save_video_frame_right, textvariable=self.tk_FPS)
        self.tk_fps_entry.pack(side='bottom', expand=True, fill='both')


        # etc
        self.tk_save_pupil_tracking_button = tk.Button(left_frame, text="Save Pupil Tracking",
                                                       command=self.tk_save_pupil_tracking)
        self.tk_save_pupil_tracking_button.pack(expand=True)

        #fps label fram
        save_fps_label_frame = tk.Frame(left_frame)
        save_fps_label_frame.pack(side="top", expand=True, fill='both')

        self.tk_type_pupil_file_name_prefix_label = tk.Label(save_fps_label_frame, text="Type Pupil File Name Prefix")
        self.tk_type_pupil_file_name_prefix_label.pack(expand=True, fill='both')
        self.tk_type_pupil_file_name_prefix_entry = tk.Entry(save_fps_label_frame,
                                                              textvariable=self.tk_type_pupil_file_name_prefix)
        self.tk_type_pupil_file_name_prefix_entry.pack(side="bottom",expand=True,fill='both')

    def make_right_frame(self, right_frame):
        # right
        ##video camera settings
        video_camera_frame = tk.Frame(right_frame, bg="orange", highlightbackground="black", highlightthickness=2)
        video_camera_frame.pack(side="top", expand=True, fill='both')

        self.tk_video_camera_settings_label = tk.Label(video_camera_frame, text="Video Camera Settings")
        self.tk_video_camera_settings_label.pack(side="top", expand=True, fill='x')

        video_camera_frame_top = tk.Frame(video_camera_frame)
        video_camera_frame_top.pack(side="top", expand=True, fill='x')


        self.tk_auto_button = tk.Button(video_camera_frame_top, text="Auto", command=self.tk_auto)
        self.tk_auto_button.pack(side="left", expand=True, fill='x')
        self.tk_reset_button = tk.Button(video_camera_frame_top, text="Reset", command=self.tk_reset)
        self.tk_reset_button.pack(side="left", expand=True, fill='x')
        self.tk_save_settings_button = tk.Button(video_camera_frame_top, text="Save Settings", command=self.tk_save_settings)
        self.tk_save_settings_button.pack(side="left", expand=True, fill='x')
        self.tk_load_settings_button = tk.Button(video_camera_frame_top, text="Load Settings", command=self.tk_load_settings)
        self.tk_load_settings_button.pack(side="left", expand=True, fill='x')

        ##sliders

        video_camera_frame_left = tk.Frame(video_camera_frame)
        video_camera_frame_left.pack(side="left", expand=True, fill='both')
        video_camera_frame_right = tk.Frame(video_camera_frame)
        video_camera_frame_right.pack(side="left", expand=True, fill='both')


        self.tk_brightness_label = tk.Label(video_camera_frame_left, text="Brightness:")
        self.tk_brightness_label.pack()
        self.tk_brightness_slider = tk.Scale(video_camera_frame_right, from_=0, to=4095, tickinterval=0.1, orient='horizontal')
        self.tk_brightness_slider.pack(expand=True, fill='both')

        self.tk_gamma_label = tk.Label(video_camera_frame_left, text="Gamma:")
        self.tk_gamma_label.pack(expand=True, fill='both')
        self.tk_gamma_slider = tk.Scale(video_camera_frame_right, from_=0, to=5, tickinterval=0.1, orient='horizontal')
        self.tk_gamma_slider.pack(expand=True, fill='both')

        self.tk_exposure_label = tk.Label(video_camera_frame_left, text="Exposure:")
        self.tk_exposure_label.pack(expand=True, fill='both')
        self.tk_exposure_slider = tk.Scale(video_camera_frame_right, from_=0, to=4, tickinterval=0.0005, orient='horizontal')
        self.tk_exposure_slider.pack(expand=True, fill='both')

        self.tk_gain_label = tk.Label(video_camera_frame_left, text="Gain:")
        self.tk_gain_label.pack(expand=True, fill='both')
        self.tk_gain_slider = tk.Scale(video_camera_frame_right, from_=0, to=48, tickinterval=0.1, orient='horizontal')
        self.tk_gain_slider.pack(expand=True, fill='both')

        ##one stray button
        self.tk_enable_tca_correction_button = tk.Button(right_frame, text="Sync Save",
                                                         command=self.tk_enable_tca_correction)
        self.tk_enable_tca_correction_button.pack()



        ##calibration settings
        calibration_frame = tk.Frame(right_frame, bg="orange", highlightbackground="black", highlightthickness=2)
        calibration_frame.pack(side="top", expand=True, fill='both')

        self.tk_calibration_label = tk.Label(calibration_frame, text="Calibration Settings")
        self.tk_calibration_label.pack(side="top", expand=True)

        self.tk_show_focus_button = tk.Button(calibration_frame, text="Show Focus", textvariable=self.tk_show_focus)
        self.tk_show_focus_button.pack(side="right", expand=True, fill='both')

        calibration_frame_left = tk.Frame(calibration_frame)
        calibration_frame_left.pack(side="left", expand=True, fill='both')
        calibration_frame_right = tk.Frame(calibration_frame)
        calibration_frame_right.pack(side="left", expand=True, fill='both')

        self.tk_tollernc_mm_label = tk.Label(calibration_frame_left, text="tollernc.(mm)")
        self.tk_tollernc_mm_label.pack(side="top", expand=True, fill='both')
        self.tk_tollernc_mm_entry = tk.Entry(calibration_frame_right, textvariable=self.tk_tollernc_mm)
        self.tk_tollernc_mm_entry.pack()

        self.tk_TCA_XY_arcmin_mm_label = tk.Label(calibration_frame_left, text="TCA(X/Y)arcmin/mm")
        self.tk_TCA_XY_arcmin_mm_label.pack(side="top", expand=True, fill='both')
        self.tk_TCA_XY_arcmin_mm_entry = tk.Entry(calibration_frame_right, textvariable=self.tk_TCA_XY_arcmin_mm)
        self.tk_TCA_XY_arcmin_mm_entry.pack()


    def make_middle_frame(self, middle_frame):
        fig = matplotlib.Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = tk.FigureCanvasTkAgg(fig, master=middle_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = tk.NavigationToolbar2Tk(canvas, middle_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    ###top buttons###

    """ quits and exits program (button 1)
    if dataScn"""
    def tk_quit(self):
        self.set_PupilTracker(0);
        date_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        if PupilParam.get_DataSync() is not None:
            pupil_data = PupilParam.get_DataSync()
            file = open(f'./VideoAndRef/Trial_DataPupil_{self.get_type_pupil_file_name_prefix()}_{date_string}')
            file.write(pupil_data)
            file.close()
        self.tk_root.destroy()

    """ starts video"""
    def tk_start_video(self):
        return

    """sets refernce"""
    def tk_set_reference(self):

        """Get mouse coordinates then set reference to it"""
        def set_reference_helper(event):
            x, y = event.x, event.y
            reference_x1 = round(x)-30
            reference_x2 = round(x)+30
            reference_y1 = round(y)-30
            reference_y2 = round(y)-30
            
            PupilParam.set_x1(reference_x1)
            PupilParam.set_x2(reference_x2)
            PupilParam.set_y1(reference_y1)
            PupilParam.set_y2(reference_y2)
            # TODO: Save reference coordinates like matlab file

            # TODO: unset reference trigger

        
        self.middle_frame.bind('<Button-1>', set_reference_helper)
        return

    """loads refernce"""
    def tk_load_reference(self):
        self.tk_root.withdraw()

        file_name = tk.filedialog.askopenfilename(title='Select RefPupil file', initialdir=os.getcwd())

        if file_name:
            global PupilParam
            path, file = os.path.split(file_name)
            if file.startswith('RefPupil_'):
                reference_data = sio.loadmat(file_name)
                reference_x1 = reference_data['Refx1'][0][0]
                reference_x2 = reference_data['Refx2'][0][0]
                reference_y1 = reference_data['Refy1'][0][0]
                reference_y2 = reference_data['Refy2'][0][0]

                PupilParam.set_x1(reference_x1)
                PupilParam.set_x2(reference_x2)
                PupilParam.set_y1(reference_y1)
                PupilParam.set_y2(reference_y2)

                # TODO: unset reference trigger

                """"
               set(handles.pushbutton3, 'String', 'Unset Reference')"""
            else:
                print("Invalid file name. File must start with 'RefPupil_'")


        return

    """unsets reference"""
    def tk_unset_reference(self):
        return

    """disables tracking"""
    def tk_disable_tracking(self):
        return

    """zooms in"""
    def tk_zoom_in(self):
        return

    """draws BE"""
    def tk_draw_be(self):
        if PupilParam.get_BEFlag() == 0:
            PupilParam.set_BEFlag(1)
            #TODO: set(hObject,'String','Hide BE');
            self.tk_draw_be_button.config(text = 'Hide BE')
            self.tk_draw_be_button.pack()
        else:
            PupilParam.set_BEFlag(0)
            # TODO: set(hObject,'String','Draw BE');
            self.tk_draw_be_button.config(text='Draw BE')
            self.tk_draw_be_button.pack()

        return

    """sync save"""
    def tk_sync_save(self):
        return

    """save video"""
    def tk_save_video(self):
        if PupilParam.get_Video() == 1 and PupilParam.set_SavingVideo() == 0:
            PupilParam.set_SavingVideo(1)
        return

    """ """
    def tk_secs(self):
        return

    """ """
    def tk_FPS(self):
        return

    """ """
    def tk_save_pupil_tracking(self):
        return

    """ """
    def tk_type_pupil_file_name_prefix(self):
        return


    """"""
    def get_type_pupil_file_name_prefix(self):
        return self.type_pupil_file_name_prefix

    """ """
    def tk_auto(self):
        return

    """"""
    def tk_reset(self):
        return

    """ """
    def tk_save_settings(self):
        return

    """ """
    def tk_load_settings(self):
        return

    """"""
    def tk_enable_tca_correction(self):
        return

    """ """
    def tk_tollernc_mm(self):
        return

    """"""
    def tk_TCA_XY_arcmin_mm(self):
        return

    """ """
    def tk_show_focus(self):
        return

    "main loop functioning for intitlization"
    def main_loop(self):
        self.tk_root.mainloop()



# Getter and Setter methods for PupilTracker
    def get_PupilTracker(self):
        return self.PupilTracker

    def set_PupilTracker(self, value):
        self.PupilTracker = value

""" initializes and runs entirety of code"""
if __name__ == "__main__":
    tg = ProjectorGUI()
    tg.main_loop()
