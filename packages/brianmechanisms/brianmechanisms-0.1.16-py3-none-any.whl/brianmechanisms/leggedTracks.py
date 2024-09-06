import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation, PillowWriter


class Settings():
    def __init__(self, radius, center_distance, leg_height, leg_length, num_legs, fig=None, ax=None) -> None:
        self.position = 0
        self.radius = radius 
        self.center_distance = center_distance
        self.leg_height = leg_height # vertical
        self.leg_length = leg_length # horizontal
        self.num_legs = num_legs

        self.endPerimeter = endPerimeter = np.pi * radius
        self.chainPerimeter = 2 * (self.endPerimeter + center_distance)

        self.legPositions = [self.chainPerimeter/self.num_legs * i for i in range(self.num_legs)]
        self.legPositionsStop = [pos + self.leg_length for pos in self.legPositions]
        self.head_starts = [pos for pos in self.legPositions]
        self.full_leg_height = self.radius + self.leg_height

        self.checkPoints = [
            center_distance / 2,  # Quadrant 1
            center_distance / 2 + endPerimeter,  # Quadrant -1
            center_distance / 2 + endPerimeter + center_distance / 2,  # Quadrant 2
            center_distance / 2 + endPerimeter + center_distance,  # Quadrant 3
            center_distance / 2 + endPerimeter + center_distance + endPerimeter,  # Quadrant -2
            center_distance / 2 + endPerimeter + center_distance + endPerimeter + center_distance / 2  # Quadrant 4
        ]

        self.fig = fig
        self.ax = ax

        if ax is not None:
            ax.set_xlim(-1.5*self.full_leg_height-0.5*center_distance, 1.5*self.full_leg_height+0.5*center_distance)
            height = 1.5*self.full_leg_height+radius
            ax.set_ylim(-height, height)
            ax.set_aspect('equal')

            fig.suptitle('Legged Tracks', fontsize=14)
            ax.set_title(f"r={radius}, d={center_distance}, n={num_legs}, l={leg_length}", fontsize=10)
            # ax.axis('off')
            ax.grid(True)

        colours = [
            ['k', 'r', 'g', 'b'],  # Set 1
            ['c', 'm', 'y', 'k'],  # Set 2
            ['m', 'y', 'b', 'g'],  # Set 3
            ['r', 'g', 'b', 'c'],  # Set 4
            ['y', 'b', 'g', 'k'],  # Set 5
            ['k', 'c', 'r', 'm'],  # Set 6
            ['g', 'y', 'c', 'b'],  # Set 7
            ['b', 'k', 'y', 'r'],  # Set 8
            ['m', 'c', 'k', 'g'],  # Set 9
            ['r', 'y', 'm', 'b']   # Set 10
        ]
        
        # Assign colors based on num
        self.colours = [colours[i % 10] for i in range(num_legs)] 
        

        pass


### This class has a wrong algorith which will give wrong results.
class leggedTrack():
    def __init__(self,settings) -> None:
        for attr, value in vars(settings).items():
            setattr(self, attr, value)
        
        self.createPaths()
        self.createLegPoints()
        self.ani = None

    def createPaths(self):
        self.createChain(self.radius, "-")
        self.createChain(self.full_leg_height, "--", False)

    def createChain(self, radius, dashed, gearDots = True):

        # Define the points for the horizontal sides
        x1 = -self.center_distance / 2
        x2 = self.center_distance / 2
        y = radius

        ax = self.ax

        center_distance = self.center_distance

        # Draw the flat horizontal sides
        ax.plot([x1, x2], [y, y], f'k{dashed}')  # Top side
        ax.plot([x1, x2], [-y, -y], f'k{dashed}')  # Bottom side

        # Draw the semicircles
        theta = np.linspace(0, np.pi, 100)
        semicircle_top_left = [(-center_distance / 2 + radius * np.cos(theta)), radius * np.sin(theta)]
        semicircle_top_right = [(center_distance / 2 + radius * np.cos(theta)), radius * np.sin(theta)]
        semicircle_bottom_left = [(-center_distance / 2 + radius * np.cos(theta)), -radius * np.sin(theta)]
        semicircle_bottom_right = [(center_distance / 2 + radius * np.cos(theta)), -radius * np.sin(theta)]

        ax.plot(semicircle_top_left[0], semicircle_top_left[1], f'k{dashed}')
        ax.plot(semicircle_top_right[0], semicircle_top_right[1], f'k{dashed}')
        ax.plot(semicircle_bottom_left[0], semicircle_bottom_left[1], f'k{dashed}')
        ax.plot(semicircle_bottom_right[0], semicircle_bottom_right[1], f'k{dashed}')

        # Add dots at the centers of the semicircles
        center_top_left = (-center_distance / 2, 0)
        center_top_right = (center_distance / 2, 0)

        ax.plot(center_top_left[0], center_top_left[1], 'ko')  # Center of left semicircle
        ax.plot(center_top_right[0], center_top_right[1], 'ko')  # Center of right semicircle

        if gearDots:
            # Add small dots at the circumference of the semicircles
            self.gear_dot_left, = ax.plot(center_top_left[0] + radius, 0, 'ro')  # Starting position for left semicircle
            self.gear_dot_right, = ax.plot(center_top_right[0] + radius, 0, 'ro')  # Starting position for right semicircle

            # Add lines from the center to the circumference dots
            self.gear_line_top_left, = ax.plot([center_top_left[0], center_top_left[0] + radius], [center_top_left[1], 0], 'r-')
            self.gear_line_top_right, = ax.plot([center_top_right[0], center_top_right[0] + radius], [center_top_right[1], 0], 'r-')

    def setPosition(self, pointIndex, addToPosition = 0):
        head_start = self.head_starts[pointIndex] + addToPosition
        position = self.position
        checkPoints = self.checkPoints
        chainPerimeter  = self.chainPerimeter
        center_distance = self.center_distance
        position+=head_start
        # Calculate the quadrant and remaining position

        remPosition = position % chainPerimeter
        position = remPosition
        for i, point in enumerate(checkPoints):
            if remPosition < point:
                rackQuadrant = i
                break

        armAngle = 0.5*np.pi  # degrees

        if rackQuadrant == 0:  # [0]
            pointPosition = -position  # a negative value
        elif rackQuadrant == 1:  # [1] # Dwell
            armAngle = np.radians(270 - 180 * (checkPoints[1] - position) / (checkPoints[1] - checkPoints[0]))
            pointPosition = -(center_distance / 2)  # negative value
        elif rackQuadrant == 2:  # [2]
            armAngle = 1.5*np.pi
            pointPosition = -(checkPoints[2] - position)  # negative value
        elif rackQuadrant == 3:  # [0]
            armAngle = 1.5*np.pi
            pointPosition = (center_distance / 2) - (checkPoints[3] - position)  # +ve value
        elif rackQuadrant == 4:  # Dwell
            armAngle = np.radians((360+90) - 180 * (checkPoints[4] - position) / (checkPoints[4] - checkPoints[3]))
            pointPosition = center_distance / 2
        else:  # rackQuadrant == 5
            pointPosition = checkPoints[5] - position  # +ve value

        
        x = pointPosition +  self.radius * np.cos(armAngle)
        y = self.radius * np.sin(armAngle)

        return pointPosition, armAngle, [x,y]
    
    def get_line_angle(self, x1, y1, x2, y2):
        # Calculate the angle in radians
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        
        # # Convert the angle from radians to degrees
        # angle_deg = math.degrees(angle_rad)
        
        return angle_rad#, angle_deg
    
    def createLegPoints(self):
        self.legPoints = []
        self.legEndPoints = []
        self.legBaseLines = []
        self.legVerticalLine1s = [ ]
        self.legVerticalLine2s = [ ]
        self.legFootPoints = [ ]
        try:
            self.position=1
            for index in range(len(self.head_starts)):
                _,armAngle,pos = self.setPosition(index)
                x = pos[0]
                y = pos[1]
                point, = self.ax.plot([x],[y], f"{self.colours[index][0]}o")
                self.legPoints.append(point)

                _,_,pos = self.setPosition(index, self.leg_length)
                x1 = pos[0]
                y1 = pos[1]
                pointEnd, = self.ax.plot([x1],[y1], f"{self.colours[index][0]}o")
                self.legEndPoints.append(pointEnd)

                armAngle = self.get_line_angle(x,y,x1,y1) - 0.5 * np.pi

                vLine1EndPoint = [x + self.leg_height * np.cos(armAngle), y + self.leg_height * np.sin(armAngle) ]
                vLine2EndPoint = [x1 + self.leg_height * np.cos(armAngle), y1 + self.leg_height * np.sin(armAngle) ]

                # a line connecting point and pointEnd
                line, = self.ax.plot([x,x1],
                                 [y,y1],
                                 color=self.colours[index][0])
                vLine1, = self.ax.plot([x,vLine1EndPoint[0]],
                                 [y,vLine1EndPoint[1]],
                                 color=self.colours[index][0])
                vLine2, = self.ax.plot([x1,vLine2EndPoint[0]],
                                 [y1,vLine2EndPoint[1]],
                                 color=self.colours[index][0])
                hLine, = self.ax.plot([vLine1EndPoint[0],vLine2EndPoint[0]],
                                 [vLine1EndPoint[1],vLine2EndPoint[1]],
                                 color=self.colours[index][0])
                
                self.legBaseLines.append(line)
                self.legVerticalLine1s.append(vLine1)
                self.legVerticalLine2s.append(vLine2)
                self.legFootPoints.append(hLine)

        except IndexError as e:
            print(f"Error: {e}. Ensure that all indices in self.head_starts are within the range of self.setPosition.")
            return

    def show(self):
        plt.show()
        
    def save(self, fileName):
        if self.ani is not None:
            writer = PillowWriter(fps=25)
            self.ani.save(f"{fileName}.gif", writer=writer)
        else:
            plt.savefig(f"{fileName}.png")
        return self

    def update_plots(self, position):
        self.position = position
        radius = self.radius
        center_distance = self.center_distance
        angle = self.position/radius
        center_top_left = (-center_distance / 2, 0)
        center_top_right = (center_distance / 2, 0)
        # Update the position of the dots
        self.gear_dot_left.set_data([center_top_left[0] + radius * np.cos(angle)], [radius * np.sin(angle)])
        self.gear_dot_right.set_data([center_top_right[0] + radius * np.cos(angle)], [radius * np.sin(angle)])
        # Update the position of the lines
        self.gear_line_top_left.set_data([center_top_left[0], center_top_left[0] + radius * np.cos(angle)], 
                               [center_top_left[1], radius * np.sin(angle)])
        self.gear_line_top_right.set_data([center_top_right[0], center_top_right[0] + radius * np.cos(angle)], 
                                [center_top_right[1], radius * np.sin(angle)])
        # return self.gear_dot_left,  self.gear_dot_right, self.gear_line_top_left, self.gear_line_top_right
        # Update leg points and lines
        for index in range(len(self.head_starts)):
            _, _, pos = self.setPosition(index)
            x = pos[0]
            y = pos[1]
            self.legPoints[index].set_data([x], [y])

            _, _, pos = self.setPosition(index, self.leg_length)
            x1 = pos[0]
            y1 = pos[1]
            self.legEndPoints[index].set_data([x1], [y1])

            self.legBaseLines[index].set_data([x, x1], [y, y1])

            armAngle = self.get_line_angle(x, y, x1, y1) - 0.5 * np.pi

            vLine1EndPoint = [x + self.leg_height * np.cos(armAngle), y + self.leg_height * np.sin(armAngle)]
            vLine2EndPoint = [x1 + self.leg_height * np.cos(armAngle), y1 + self.leg_height * np.sin(armAngle)]

            # # Update vertical lines
            self.legVerticalLine1s[index].set_data([x, vLine1EndPoint[0]], [y, vLine1EndPoint[1]])
            self.legVerticalLine2s[index].set_data([x1, vLine2EndPoint[0]], [y1, vLine2EndPoint[1]])

            # # Update horizontal line
            self.legFootPoints[index].set_data([vLine1EndPoint[0], vLine2EndPoint[0]], [vLine1EndPoint[1], vLine2EndPoint[1]])

        return (self.gear_dot_left, self.gear_dot_right,
                self.gear_line_top_left, self.gear_line_top_right
                 ,*self.legBaseLines,
                 *self.legPoints, *self.legEndPoints,
                *self.legVerticalLine1s, *self.legVerticalLine2s,
                *self.legFootPoints
                )

    def update(self, stopPosition, speed):
        if self.ani is not None:
            self.ani.event_source.stop()  # Stop previous animation if exists
        stopPosition = int(stopPosition)
        frames_forward = np.arange(0, stopPosition+1,speed)
        frames_backward = np.arange(stopPosition, -1, -speed)
        frames = np.concatenate((frames_forward, frames_backward))

        self.ani = FuncAnimation(self.fig, self.update_plots, frames=frames, blit=True, interval=100)
        return self
