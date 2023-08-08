#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
LeftMotors_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
LeftMotors_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
LeftMotors = MotorGroup(LeftMotors_motor_a, LeftMotors_motor_b)
RightMotors_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
RightMotors_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
RightMotors = MotorGroup(RightMotors_motor_a, RightMotors_motor_b)


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration

ARM_PID_KP = 10
ARM_PID_TP = 50

drivetrain = DriveTrain(LeftMotors, RightMotors, 319.19, 295, 40, MM, 1)

lVel = 0
RVel = 0

voltMultiplier = 12
speedMultiplier = 1

cAxisDrive = 0
cAxisTurn = 0

isSwingDriving = True

# BLUE=TRUE, RED=FALSE
alliance = True

def setupAddonMotor(motorobj, controllerbutton1, controllerbutton2):

    def newmotorbutton1():
        motorobj.spin(FORWARD)
        while controllerbutton1.pressing():
            wait(10, MSEC)
        motorobj.stop()

    def newmotorbutton2():
        motorobj.spin(REVERSE)
        while controllerbutton2.pressing():
            wait(10, MSEC)
        motorobj.stop()

    controllerbutton1.pressed(newmotorbutton1)
    controllerbutton2.pressed(newmotorbutton2)

# Code to select the autonomous task

def selectSettings():

    global isSwingDriving, speedMultiplier

    # Configure swing driving

    brain.screen.clear_screen()

    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(0, 0, 240, 272 - 40)

    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(240, 0, 240, 272 - 40)

    brain.screen.set_fill_color(Color.WHITE)
    brain.screen.draw_rectangle(0, 272 - 40, 240, 40)

    brain.screen.set_cursor(0, 0)
    brain.screen.print("Press Blue to turn on Swing Drive. Press Red to turn off Swing Drive.")
    brain.screen.next_row()

    while not brain.screen.pressing():
        wait(10, MSEC)
    
    if (not brain.screen.y_position() > 272 - 40) and brain.screen.x_position() > 240:
        isSwingDriving = False

    # Configure speed multiplier

    brain.screen.clear_screen()

    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(0, 0, 240, 272)

    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(240, 0, 240, 272)

    brain.screen.set_fill_color(Color.WHITE)
    brain.screen.draw_rectangle(0, 272 - 40, 240, 40)

    brain.screen.set_cursor(0, 0)
    brain.screen.print("Press Blue to increase speed. Press Red to decrease speed.")
    brain.screen.next_row()

    while not brain.screen.y_position() > 272 - 40:

        while not brain.screen.pressing():
            wait(15, MSEC)
    
        if brain.screen.x_position() > 240:
            speedMultiplier -= 0.1
        else:
            speedMultiplier += 0.1

        while brain.screen.pressing():
            wait(15, MSEC)

def selectTeam():

    global alliance

    brain.screen.clear_screen()

    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(0, 0, 240, 272 - 40)

    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(240, 0, 240, 272 - 40)

    brain.screen.set_fill_color(Color.WHITE)
    brain.screen.draw_rectangle(0, 272 - 40, 240, 40)

    brain.screen.set_cursor(0, 0)
    brain.screen.print("Select team. Press White to choose settings.")
    brain.screen.next_row()

    while not brain.screen.pressing():
        wait(10, MSEC)
    
    if brain.screen.y_position() > 272 - 40:
        selectSettings()
        return False
    elif brain.screen.x_position() > 240:
        alliance = False

    return True

def brainUserInterface():

    while (not selectTeam()):
        selectTeam()

# DRIVING ---------------------------------------------------------

def handledrivetrainDriving():
    if cAxisDrive > 0.1:
        drivetrain.drive(FORWARD)
    if cAxisDrive < -0.1:
        drivetrain.drive(REVERSE)

def handledrivetrainTurning():
    if cAxisTurn > 0.1:
        drivetrain.turn(RIGHT)
    if cAxisTurn < -0.1:
        drivetrain.turn(LEFT)

def handleSwingDriving():
    global RVel, lVel
    # Driving
    if cAxisDrive > 0:
        lVel += 1
        RVel += 1
    if cAxisDrive < 0:
        lVel -= 1
        RVel -= 1

def setVars():
    global cAxisDrive, cAxisTurn, lVel, RVel
    # Variable updates
    lVel = 0
    RVel = 0
    cAxisDrive = controller_1.axis3.position()
    cAxisTurn = controller_1.axis1.position()

def handleSwingTurning():
    global lVel, RVel
    # Turning
    if (not math.fabs(cAxisDrive) < 0.1):
        turnRad = -1 * math.fabs(cAxisTurn)
        if cAxisTurn > 0:
            RVel += turnRad
        if cAxisTurn < 0:
            lVel += turnRad
    else:
        if cAxisTurn > 0:
            RVel -= 1
            lVel += 1
        if cAxisTurn < 0:
            RVel += 1
            lVel -= 1

# CONTROL FUNCTIONS ----------------------------------------------

def addonControl():

    while (True):
        wait(10, MSEC)

def movementControl():

    while (True):

        setVars()

        if isSwingDriving:
            handleSwingDriving()
            handleSwingTurning()

            # Apply 
            LeftMotors.spin(FORWARD, lVel * voltMultiplier * speedMultiplier, VOLT)
            RightMotors.spin(FORWARD, RVel * voltMultiplier * speedMultiplier, VOLT)
        else:
            handledrivetrainDriving()
            handledrivetrainTurning()

            # If both of the controller sticks are in the neutral position, stop moving.
            if (cAxisTurn < 0.1 and cAxisTurn > -0.1 and cAxisDrive > -0.1 and cAxisDrive < 0.1):
                drivetrain.stop()

        wait(10, MSEC)

# MAIN FUNCTIONS --------------------------------------------------

def autonomous():
    # Autonomous
    pass

def main():

    RightMotors.set_velocity(100, PERCENT)
    LeftMotors.set_velocity(100, PERCENT)

    drivetrain.set_drive_velocity(100 * speedMultiplier, PERCENT)
    drivetrain.set_turn_velocity(100 * speedMultiplier, PERCENT)
    drivetrain.set_stopping(COAST)

    brainUserInterface()

# SETUP -------------------------------------------------------------

def auton_wrap():
    
    auton_thread = Thread(autonomous)
    
    while(competition.is_autonomous() and competition.is_enabled()):
        wait(10, MSEC)
    
    auton_thread.stop()

def driver_wrap():
    
    driver_thread = Thread(movementControl)
    addon_thread = Thread(addonControl)
    

    while(competition.is_driver_control() and competition.is_enabled()):
        wait(10, MSEC)
    
    driver_thread.stop()
    addon_thread.stop()

competition = Competition(driver_wrap, auton_wrap)

main()

# Activates after user interface is done.

if brain.battery.capacity() < 70:
    controller_1.rumble("----")
    controller_1.screen.print("Battery!")
    controller_1.screen.next_row()
