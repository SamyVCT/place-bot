"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import Type

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.gui_sr import GuiSR
from place_bot.gui_map.map_abstract import MapAbstract


class MyRobotKeyboard(RobotAbstract):
    def control(self):
        command = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyMapKeyboard(MapAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS MAP
        self._size_area = (600, 600)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        self._robot_pos = ((0, 0), 0)
        self._playground.add(robot, self._robot_pos)


def print_keyboard_man():
    print("How to use the keyboard to direct the robot?")
    print("\t- up / down key : forward and backward")
    print("\t- left / right key : turn left / right")
    print("\t- l key : display (or not) the lidar sensor")
    print("\t- q key : exit the program")
    print("\t- r key : reset")


if __name__ == '__main__':
    print_keyboard_man()
    my_robot = MyRobotKeyboard()
    my_map = MyMapKeyboard(robot=my_robot)

    # draw_lidar : enable the visualization of the lidar rays
    gui = GuiSR(the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                )
    gui.run()
