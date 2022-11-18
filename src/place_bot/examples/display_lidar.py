"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import Type

from spg.playground import Playground
from spg.utils.definitions import CollisionTypes

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maps.walls_complete_map_2 import add_walls, add_boxes
from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.gui_sr import GuiSR
from spg_overlay.gui_map.map_abstract import MapAbstract
from spg_overlay.utils.misc_data import MiscData


class MyRobotLidar(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def control(self):
        """
        We only send a command to do nothing
        """
        command = {"forward": 0.0,
                   "lateral": 0.0,
                   "rotation": 0.0,
                   "grasper": 0}
        return command


class MyMapLidar(MapAbstract):

    def __init__(self):
        super().__init__()

        # PARAMETERS MAP
        self._size_area = (1113, 750)

        self._number_robots = 1
        self._robots_pos = [((-50, 0), 0)]
        self._robots = []

    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        playground = ClosedPlayground(size=self._size_area)

        add_walls(playground)
        add_boxes(playground)

        # POSITIONS OF THE ROBOTS
        misc_data = MiscData(size_area=self._size_area,
                             number_robots=self._number_robots)
        for i in range(self._number_robots):
            robot = robot_type(identifier=i, misc_data=misc_data,
                               should_display_lidar=True,
                               should_display_touch=False)
            self._robots.append(robot)
            playground.add(robot, self._robots_pos[i])

        return playground


def main():
    my_map = MyMapLidar()
    playground = my_map.construct_playground(robot_type=MyRobotLidar)

    # draw_lidar : enable the visualization of the lidar rays
    # enable_visu_noises : to enable the visualization. It will show also a demonstration of the integration
    # of odometer values, by drawing the estimated path in red. The green circle shows the position of robot according
    # to the gps sensor and the compass
    gui = GuiSR(playground=playground,
                the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                enable_visu_noises=True,
                )
    gui.run()


if __name__ == '__main__':
    main()
