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

        self.points_on_curve = []

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
        # self.points_on_curve = [] For some reason this only works when defined in settings and not here

    def createPaths(self):
        self.createChain(self.radius, "-", curvePoints=True)
        self.createChain(self.full_leg_height, "--", False)

    def createChain(self, radius, dashed, gearDots = True, curvePoints= False):

        # Define the points for the horizontal sides
        x1 = -self.center_distance / 2
        x2 = self.center_distance / 2
        y = radius

        ax = self.ax

        center_distance = self.center_distance

        # Draw the flat horizontal sides
        ax.plot([x1, x2], [y, y], f'k{dashed}')  # Top side
        ax.plot([x1, x2], [-y, -y], f'k{dashed}')  # Bottom side
        if curvePoints:
            num_points = 10000
        else:
            num_points = 100

        # Draw the semicircles
        theta_left = np.linspace(0.5*np.pi, 1.5* np.pi, num_points)
        theta_right = np.linspace(-0.5*np.pi, 0.5* np.pi, num_points)
        semicircle_left = [(-self.center_distance / 2 + radius * np.cos(theta_left)),radius * np.sin(theta_left)]
        semicircle_right_side_of_left = [(-self.center_distance / 2 + radius * np.cos(theta_right)),radius * np.sin(theta_right)]
        semicircle_right = [(self.center_distance / 2 + radius * np.cos(theta_right)),radius * np.sin(theta_right)]
        semicircle_left_side_of_right = [(self.center_distance / 2 + radius * np.cos(theta_left)),radius * np.sin(theta_left)]

        ax.plot(semicircle_left[0], semicircle_left[1], f'k{dashed}')
        ax.plot(semicircle_right[0], semicircle_right[1], f'k{dashed}')
        if curvePoints:
            ax.plot(semicircle_right_side_of_left[0], semicircle_right_side_of_left[1], f'k{dashed}')
            ax.plot(semicircle_left_side_of_right[0], semicircle_left_side_of_right[1], f'k{dashed}')

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



         # Define the number of points along each horizontal line

        # Create points for horizontal lines
        x_horizontal = np.linspace(x1, x2, num_points)
        y_top = np.full_like(x_horizontal, y)
        y_bottom = np.full_like(x_horizontal, -y)

        if curvePoints:
            self.points_on_curve = (
                list(zip(semicircle_left[0], semicircle_left[1])) +
                list(zip(semicircle_right[0], semicircle_right[1])) +
                list(zip(x_horizontal, y_top)) +
                list(zip(x_horizontal, y_bottom)) +
                [(x1, y), (x2, y), (x1, -y), (x2, -y)]
            )
            positive_y_points = [(x, y) for x, y in self.points_on_curve if y >= 0]
            negative_y_points = [(x, y) for x, y in self.points_on_curve if y < 0]

            # Sort positive y points:
            # 1. First take values for x from 0 to the least x
            first_positive_y_points = sorted([p for p in positive_y_points if p[0] <= 0], key=lambda p: p[0], reverse=True)
            # 2. Then take values for x from greatest x to 0
            second_positive_y_points = sorted([p for p in positive_y_points if p[0] > 0], key=lambda p: p[0], reverse=True)

            # Sort negative y points from least x to greatest x
            sorted_negative_y_points = sorted(negative_y_points, key=lambda p: p[0])

            # Combine all points in the desired order
            sorted_points = first_positive_y_points + sorted_negative_y_points + second_positive_y_points 

            # Update points on curve
            self.points_on_curve = sorted_points
    def find_leg_theta(self, current_point, L, debug=False):
        x, y = current_point
        start_index = None
        min_distance = float('inf')
        
        # Find the index of the point on the curve that maps to the current point
        # for i, (px, py) in enumerate(self.points_on_curve):
        #     if np.isclose(px, x, atol=1e-3) and np.isclose(py, y, atol=1e-3):
        #         start_index = i
        #         break

        # Find the index of the closest point on the curve to the current point
        for i, (px, py) in enumerate(self.points_on_curve):
            distance = np.hypot(px - x, py - y)
            
            if distance < min_distance:
                if debug:
                    print("is less:", distance, min_distance)
                # print(distance)
                min_distance = distance
                start_index = i

        
        if start_index is None:
            if debug:
                print("is None", x,y, len(self.points_on_curve))
            return None, None
        

        # Search for points after the current point index
        for i in range(start_index + 1, len(self.points_on_curve)):
            px, py = self.points_on_curve[i]
            dx = px - x
            dy = py - y
            distance = np.hypot(dx, dy)
            if np.isclose(distance, L, atol=1e-3):
                theta = np.arctan2(dy, dx)
                return theta, (px, py)

        # Wrap around and search from the beginning up to the current point index
        for i in range(0, start_index):
            px, py = self.points_on_curve[i]
            dx = px - x
            dy = py - y
            distance = np.hypot(dx, dy)
            if np.isclose(distance, L, atol=1e-3):
                theta = np.arctan2(dy, dx)
                return theta, (px, py)

        return None, None


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


                leg_theta,pos = self.find_leg_theta(pos, self.leg_length)
                # print(leg_theta)
                # _,_,pos = self.setPosition(index, self.leg_length)
                x1 = pos[0]
                y1 = pos[1]
                # x1 = x + self.leg_length * np.cos(leg_theta)
                # y1 = y + self.leg_length * np.sin(leg_theta)
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
                                 color=self.colours[index][0], linestyle='--')
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

            #  _,armAngle,pos = self.setPosition(index)
            #     x = pos[0]
            #     y = pos[1]

            # _, _, pos = self.setPosition(index, self.leg_length)
            leg_theta,pos = self.find_leg_theta(pos, self.leg_length, debug=False)
            if pos is None:
                continue
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
