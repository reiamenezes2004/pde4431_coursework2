from robodk import *
from robodk.robolink import *
from robodk.robomath import *
import time

# creating a connection to robodk
RDK = Robolink()
robot = RDK.Item('Epson VT6')

# programs for gripper operations - opening and closing
open_gripper_mechanism_program = RDK.Item('open_gripper_mechanism', ITEM_TYPE_PROGRAM)
close_gripper_mechanism_program = RDK.Item('close_gripper_mechanism', ITEM_TYPE_PROGRAM)
attach_cone = RDK.Item('attach_cone', ITEM_TYPE_PROGRAM)
detach_cone = RDK.Item('detach_cone', ITEM_TYPE_PROGRAM)
home = RDK.Item('home')  # home position of the robot

# define positions for picking the cones from the first station
cone_pick_1 = RDK.Item('cone_pick_1')  # first cone position
cone_pick_2 = RDK.Item('cone_pick_2')  # second cone position
cone_pick_3 = cone_pick_1.Pose() * transl(0, 0, -120)  # third cone position
cone_pick_4 = cone_pick_2.Pose() * transl(0, 0, -120)  # fourth cone position
cone_pick_5 = cone_pick_1.Pose() * transl(0, 0, -240)  # fifth cone position
cone_pick_6 = cone_pick_2.Pose() * transl(0, 0, -240)  # sixth cone position
approach_point = RDK.Item('approach_point')  # approach position for picking cones from the first station

# define positions for ice cream filling
approach_icecream_machine_point = RDK.Item('approach_icecream_machine_point')  # approach to ice cream machine
starting_icecream = RDK.Item('starting_icecream')  # initial ice cream machine position
fill_down_flavor1 = RDK.Item('fill_down_flavor1')  # position for first flavor filling
fill_down_flavor2 = RDK.Item('fill_down_flavor2')  # position for second flavor filling

# define fill positions with downward and upward transformations
fill_1_go_down = fill_down_flavor1.Pose() * transl(0, 0, -30)  # move down for first flavor
fill_1_go_up = fill_1_go_down * transl(0, 0, 30)  # move back up for first flavor
fill_2_go_down = fill_down_flavor2.Pose() * transl(0, 0, -30)  # move down for second flavor
fill_2_go_up = fill_2_go_down * transl(0, 0, 30)  # move back up for second flavor
completed_icecream_machine = RDK.Item('completed_icecream_machine')  # final position at ice cream machine - completed

# define positions for dropping cones
cone_drop_1 = RDK.Item('cone_drop_1')  # first cone drop position
cone_drop_2 = RDK.Item('cone_drop_2')  # second cone drop position
cone_drop_3 = RDK.Item('cone_drop_3')  # third cone drop position
cone_drop_4 = RDK.Item('cone_drop_4')  # fourth cone drop position
cone_drop_5 = RDK.Item('cone_drop_5')  # fifth cone drop position
cone_drop_6 = RDK.Item('cone_drop_6')  # sixth cone drop position

# define approach drop positions with adjusted transformations
approach_drop_cone1 = cone_drop_1.Pose() * transl(-50, 0, 50)  # approach position for cone 1 drop
approach_drop_cone2 = cone_drop_2.Pose() * transl(-50, 0, 50)  # approach position for cone 2 drop
approach_drop_cone3 = cone_drop_3.Pose() * transl(-50, 0, 50)  # approach position for cone 3 drop
approach_drop_cone4 = cone_drop_4.Pose() * transl(-20, 0, 20)  # approach position for cone 4 drop (adjusted) - too close for the robot target reach
approach_drop_cone5 = cone_drop_5.Pose() * transl(-50, 0, 50)  # approach position for cone 5 drop
approach_drop_cone6 = cone_drop_6.Pose() * transl(-50, 0, 50)  # approach position for cone 6 drop

# create arrays for cone positions
pick_cone_positions = [cone_pick_1, cone_pick_2, cone_pick_3, cone_pick_4, cone_pick_5, cone_pick_6]
approach_cone_drop_positions = [approach_drop_cone1, approach_drop_cone2, approach_drop_cone3, approach_drop_cone4, approach_drop_cone5, approach_drop_cone6]
drop_cone_positions = [cone_drop_1, cone_drop_2, cone_drop_3, cone_drop_4, cone_drop_5, cone_drop_6]

# created a loop for picking, filling, and dropping cones
for i in range(6):
    try:
        print(f"starting sequence for cone {i+1}")
        robot.MoveJ(home)  # move to home position
        open_gripper_mechanism_program.RunProgram()  # open gripper
        robot.MoveJ(approach_point)  # move to approach point
        robot.MoveL(pick_cone_positions[i])  # move to pick position
        close_gripper_mechanism_program.RunProgram()  # close gripper
        attach_cone.RunProgram()  # attach cone to gripper
        robot.MoveL(approach_point)  # return to approach point
        robot.MoveJ(approach_icecream_machine_point)  # move to ice cream machine
        robot.MoveL(starting_icecream)  # move to starting position at machine

        # filling process
        robot.setSpeed(50)  # set slower speed for filling
        robot.setSpeedJoints(25)
        robot.MoveL(fill_down_flavor1)  # move to first flavor position
        robot.MoveL(fill_1_go_down)  # move down to fill
        robot.MoveL(fill_1_go_up)  # move up after filling
        robot.MoveL(fill_down_flavor2)  # move to second flavor position
        robot.MoveL(fill_2_go_down)  # move down to fill
        robot.MoveL(fill_2_go_up)  # move up after filling
        robot.MoveL(completed_icecream_machine)  # move to completed position
        robot.setSpeed(500)  # restore normal speed
        robot.setSpeedJoints(150)

        # dropping process
        print(f"dropping cone {i+1}")
        robot.MoveL(approach_cone_drop_positions[i])  # move to approach drop position
        robot.MoveL(drop_cone_positions[i])  # move to drop position
        detach_cone.RunProgram()  # detach cone from gripper
        open_gripper_mechanism_program.RunProgram()  # open gripper
        robot.MoveL(approach_cone_drop_positions[i])  # return to approach drop position
    except Exception as e:
        print(f"error during sequence for cone {i+1}: {e}")
        continue

# return to home position
print("all cones have been filled with ice cream. returning the robot to home position.")
robot.MoveJ(home)
