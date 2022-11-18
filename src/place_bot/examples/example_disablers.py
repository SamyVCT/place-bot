"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import List, Type

from spg.utils.definitions import CollisionTypes

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.entities.rescue_center import RescueCenter, wounded_rescue_center_collision
from spg_overlay.entities.sensor_disablers import NoGpsZone, NoComZone, KillZone, srdisabler_disables_device
from spg_overlay.entities.wounded_person import WoundedPerson
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.gui_sr import GuiSR
from spg_overlay.gui_map.map_abstract import MapAbstract
from spg_overlay.utils.misc_data import MiscData


class MyRobotDisablers(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def define_message_for_all(self):
        """
        Here, we don't need communication...
        """
        msg_data = (self.identifier,
                    (self.measured_gps_position(), self.measured_compass_angle()))
        return msg_data

    def control(self):
        """
        We only send a command to do nothing
        """
        command = {"forward": 0.0,
                   "lateral": 0.0,
                   "rotation": 0.0,
                   "grasper": 0}
        return command


class MyMapDisablers(MapAbstract):

    def __init__(self):
        super().__init__()

        # PARAMETERS MAP
        self._size_area = (600, 600)

        self._rescue_center = RescueCenter(size=(100, 100))
        self._rescue_center_pos = ((0, 100), 0)

        self._no_com_zone = NoComZone(size=(150, 150))
        self._no_com_zone_pos = ((-150, 0), 0)

        self._no_gps_zone = NoGpsZone(size=(150, 150))
        self._no_gps_zone_pos = ((150, 0), 0)

        self._kill_zone = KillZone(size=(150, 150))
        self._kill_zone_pos = ((0, -200), 0)

        self._wounded_persons_pos = [(200, 0), (-200, 0), (200, -200), (-200, -200)]
        self._number_wounded_persons = len(self._wounded_persons_pos)
        self._wounded_persons: List[WoundedPerson] = []

        self._number_robots = 1
        self._robots_pos = [((0, 0), 0)]
        self._robots = []

    def construct_playground(self, robot_type: Type[RobotAbstract]):
        playground = ClosedPlayground(size=self._size_area)

        # RESCUE CENTER
        playground.add_interaction(CollisionTypes.GEM,
                                   CollisionTypes.ACTIVABLE_BY_GEM,
                                   wounded_rescue_center_collision)

        playground.add(self._rescue_center, self._rescue_center_pos)

        # DISABLER ZONES
        playground.add_interaction(CollisionTypes.DISABLER,
                                   CollisionTypes.DEVICE,
                                   srdisabler_disables_device)

        playground.add(self._no_com_zone, self._no_com_zone_pos)
        playground.add(self._no_gps_zone, self._no_gps_zone_pos)
        playground.add(self._kill_zone, self._kill_zone_pos)

        # POSITIONS OF THE WOUNDED PERSONS
        for i in range(self._number_wounded_persons):
            wounded_person = WoundedPerson(rescue_center=self._rescue_center)
            self._wounded_persons.append(wounded_person)
            pos = (self._wounded_persons_pos[i], 0)
            playground.add(wounded_person, pos)

        # POSITIONS OF THE ROBOTS
        misc_data = MiscData(size_area=self._size_area,
                             number_robots=self._number_robots)
        for i in range(self._number_robots):
            robot = robot_type(identifier=i, misc_data=misc_data)
            self._robots.append(robot)
            playground.add(robot, self._robots_pos[i])

        return playground


def main():
    my_map = MyMapDisablers()
    playground = my_map.construct_playground(robot_type=MyRobotDisablers)

    # enable_visu_noises : to enable the visualization. It will show also a demonstration of the integration
    # of odometer values, by drawing the estimated path in red. The green circle shows the position of robot according
    # to the gps sensor and the compass.
    gui = GuiSR(playground=playground,
                the_map=my_map,
                print_messages=True,
                use_keyboard=True,
                enable_visu_noises=True,
                )
    gui.run()


if __name__ == '__main__':
    main()
