import os


os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.properties import ObjectProperty
from kivy.animation import Animation

from time import sleep

from datetime import datetime
from kivy.uix.widget import Widget
from threading import Thread


time = datetime



MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'

import spidev
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)


class ProjectNameGUI(App):
    def build(self):
        return SCREEN_MANAGER
Window.clearcolor = (1, 1, 1, 1)

class MainScreen(Screen):
    def start_stepper(self):
        s0.go_until_press(0, self.amongus_slider.value*6400)
    def change(self):
        s0.go_until_press(1, self.amongus_slider.value*6400)
    def slide_speed(self):
        self.amongus_slider
        self.label_slider
        s0.set_speed(self.amongus_slider.value)
    def queso(self):
        self.in_real_life_label.text = str(s0.get_position_in_units())
        s0.set_speed(1)
        s0.start_relative_move(-15)
        while s0.is_busy():
            sleep(1)
        self.in_real_life_label.text = str(s0.get_position_in_units())
        print("Starting to Sleep")
        sleep(10)
        print("Finished Sleeping")
        s0.set_speed(5)
        s0.start_relative_move(-10)
        while s0.is_busy():
            sleep(1)
        self.in_real_life_label.text = str(s0.get_position_in_units())
        print("Starting to Sleep 2")
        sleep(8)
        print("Finished Sleeping 2")
        s0.goHome()
        print("Starting to Sleep 3")
        sleep(30)
        print("Finished Sleeping 3")
        self.in_real_life_label.text = str(s0.get_position_in_units())
        s0.set_speed(8)
        s0.start_relative_move(100)
        while s0.is_busy():
            sleep(1)
        self.in_real_life_label.text = str(s0.get_position_in_units())
        print("Starting to Sleep 4")
        sleep(10)
        print("Finished Sleeping 4")
        s0.goHome()
        self.in_real_life_label.text = str(s0.get_position_in_units())



    def queso_thread(self):
        Thread(target=self.queso, daemon=True).start()



    def stop_stepper(self):
        s0.softStop()

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()