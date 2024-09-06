import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter


class mechanism1:
    def __init__(self, settings):
        self.settings = settings
        self.ani = None
        pass 

    @staticmethod
    def calculate_radius2(radius1, gear1_angle):
        radius2 = (gear1_angle * radius1) / (2 * np.pi - gear1_angle)
        return radius2
    
    @staticmethod
    def Settings(options, center_distance = 0, fig = None, ax = None, grid=False, rotations = 1, speed = 0.5):
        """
        Populate the settings dictionary with values from the options dictionary.

        Parameters:
        options (dict): A dictionary containing options and their values.

        Returns:
        dict: A dictionary containing the populated settings.
        """
        
        displacements = []
        radii_2 = []
        num_instances = len(options)
        origins = []
        phase_diff = 2*np.pi/num_instances
        for index, instance in enumerate(options):
            # if instance.get('offset_angle_degrees'):
            #     instance["offset_angle"] = np.radians(instance.get('offset_angle_degrees'))
            instance["offset_angle"] = np.radians(-90)
            offset_angle = instance.get('offset_angle')
            return_speed = instance.get('return_speed')
            return_angle = 2 * np.pi * 1/(return_speed + 1)
            forward_angle = 2 * np.pi - return_angle
            instance["forward_angle"] = forward_angle
            instance["phase"] = phase_diff * (index -1)
            instance["gear1_angle"] = forward_angle
            instance["start_angle_1"] = offset_angle + (2 * np.pi - forward_angle) / 2
            instance["stop_angle_1"] = instance.get('start_angle_1') + forward_angle
            instance["start_angle_2"] =  offset_angle + (np.pi - return_angle / 2)
            instance["stop_angle_2"] =  offset_angle + (np.pi + return_angle / 2)

            instance["radius2"] = mechanism1.calculate_radius2(instance.get('radius1', 0), forward_angle)
            radii_2.append(instance["radius2"])
            displacements.append(forward_angle * instance.get('radius1', 0))
            instance["displacement"] = forward_angle * instance.get('radius1', 0)
            instance["x_limit"] = instance["displacement"]+10
            if center_distance == 0:
                center_distance = 2 * np.pi * instance.get('radius1', 0) * 2 
            origins.append(index * center_distance)

            

        settings = {"instances": options}
        if fig:
            settings['fig'] = fig 
        else:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
        settings['fig'] = fig 
        settings['ax'] = ax 

        # x_limit = sum(displacements) + (len(displacements) - 1) * center_distance
        x_limit = (len(options)) * center_distance + 10
        y_limit = 2 * max(radii_2) + 10

        settings["x_limit"] = x_limit
        settings["y_limit"] = y_limit


        ax.set_xlim(-x_limit/2, x_limit/2)
        ax.set_ylim(-y_limit/2, y_limit/2)
        ax.set_aspect('equal')

        if grid:
            plt.grid(True)

        if origins:
            mid_value = (max(origins) + min(origins)) / 2
            origins = [o - mid_value for o in origins]

        # Assign origins to each instance
        for index, instance in enumerate(options):
            instance["origin"] = origins[index]

        settings["rotations"] = rotations
        settings["speed"] = speed

        return settings

    def create_circle_section(self, r, num_points=100, start_angle=0, end_angle=2 * np.pi, phase=0):
        theta = np.linspace(start_angle+phase, end_angle+phase, num_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    def rack_displacement(self, angle, forward_angle, radius1, radius2):
        return_angle = 2 *np.pi  - forward_angle
        if angle <= forward_angle / 2:
            displacement = -angle * radius1
        elif angle <= forward_angle / 2 + return_angle:
            last_position = -(forward_angle / 2)* radius1
            displacement = last_position + (angle - forward_angle / 2) * radius2
        else:
            last_position = (forward_angle / 2)* radius1
            displacement = last_position - (angle - (forward_angle / 2 + return_angle)) * radius1
        
        return displacement

    def plot(self, instance_number=None):
        fig = self.settings['fig']
        ax = self.settings['ax']

        if instance_number is not None:
            # Filter instances to only include the specified instance_number
            instances = [self.settings['instances'][instance_number]]
        else:
            # Plot all instances
            instances = self.settings['instances']

        for inst in instances:
            radius1 = inst.get('radius1', 0)
            forward_angle = inst.get('forward_angle', 0)
            start_angle_1 = inst.get('start_angle_1', 0)
            stop_angle_1 = inst.get('stop_angle_1', 0)
            start_angle_2 = inst.get('start_angle_2', 0)
            stop_angle_2 = inst.get('stop_angle_2', 0)
            origin = inst.get('origin', 0)
            x_limit = inst.get("x_limit")
            phase = inst.get("phase")

            # Plot the larger circle section
            x1, y1 = self.create_circle_section(radius1, start_angle=start_angle_1, end_angle=stop_angle_1, phase=phase)
            ax.plot(x1 + origin, y1, label=f'Larger Circle Section (Origin {origin})', color='blue', linestyle='--')

            # Plot the smaller circle section
            radius2 = inst.get('radius2', 0)
            x2, y2 = self.create_circle_section(radius2, start_angle=start_angle_2, end_angle=stop_angle_2, phase=phase)
            ax.plot(x2 + origin, y2, label=f'Smaller Circle Section (Origin {origin})', color='red', linestyle='--')

            angle = phase % (2 * np.pi)
            x_end_circle1 = radius1 * np.cos(stop_angle_1 + angle)+origin
            y_end_circle1 = radius1 * np.sin(stop_angle_1 + angle)
            x_start_circle1 = radius1 * np.cos(start_angle_1 + angle)+origin
            y_start_circle1 = radius1 * np.sin(start_angle_1 + angle)

            x_end_circle2 = radius2 * np.cos(stop_angle_2 + angle)+origin
            y_end_circle2 = radius2 * np.sin(stop_angle_2 + angle)
            x_start_circle2 = radius2 * np.cos(start_angle_2 + angle)+origin
            y_start_circle2 = radius2 * np.sin(start_angle_2 + angle)

            ax.plot([x_end_circle2, x_start_circle1], [y_end_circle2, y_start_circle1], color='black', linestyle='-')
            ax.plot([x_start_circle2, x_end_circle1], [y_start_circle2, y_end_circle1], color='black', linestyle='-')
            ax.plot([x_start_circle1, x_end_circle1], [y_start_circle1, y_end_circle1], color='black', linestyle='-')

            # the rack
            rack_displacement = self.rack_displacement(angle, forward_angle, radius1, radius2)

            # Add dashed horizontal lines
            ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [radius1, radius1], color='blue', linestyle='--', label='Line at radius1')
            ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius2, -radius2], color='red', linestyle='--', label='Line at -radius2')

            # Connect the starts and ends of the lines
            ax.plot([-x_limit/2 + origin+rack_displacement, -x_limit/2 + origin+rack_displacement], [radius1, -radius2], color='black', linestyle='-', label='Connection Start')
            ax.plot([x_limit/2+origin+rack_displacement, x_limit/2+origin+rack_displacement], [radius1, -radius2], color='black', linestyle='-', label='Connection End')


            # Add center dot
            ax.plot(origin, 0, 'ko')  # 'ko' stands for black color and circle marker

        # Set plot settings
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f'Mechanism 1 (n={len(instances)})')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        ax.axis('off')
        
        

        return self


    def show(self):
        plt.show()
        return self
    
    def save(self, fileName):
        if self.ani is not None:
            writer = PillowWriter(fps=25)
            self.ani.save(f"{fileName}.gif", writer=writer)
        else:
            plt.savefig(f"{fileName}.png")
        return self
    
    def update(self, interval=100, frames=100):
        fig = self.settings['fig']
        ax = self.settings['ax']

        rotation = self.settings.get('rotation', 2 * np.pi)  # Default to 360 degrees (full rotation)
        speed = self.settings.get('speed', 1)  # Default speed factor

        # Calculate the total number of frames needed for the given rotation
        total_frames = int((rotation / (2 * np.pi)) * frames / speed)
        
        def animate(frame):
            ax.clear()  # Clear the current plot
            for inst in self.settings['instances']:
                radius1 = inst.get('radius1', 0)
                radius2 = inst.get('radius2', 0)
                forward_angle = inst.get('forward_angle', 0)
                start_angle_1 = inst.get('start_angle_1', 0)
                stop_angle_1 = inst.get('stop_angle_1', 0)
                start_angle_2 = inst.get('start_angle_2', 0)
                stop_angle_2 = inst.get('stop_angle_2', 0)
                origin = inst.get('origin', 0)
                # angle = frame * np.pi / 180
                phase = inst.get("phase")+ (frame * rotation / total_frames) # (2 * np.pi / frames)

                # Update phase
                # inst["phase"] = phase + (2 * np.pi / frames)

                # Redraw the plot with the updated phase
                x1, y1 = self.create_circle_section(radius1, start_angle=start_angle_1, end_angle=stop_angle_1, phase=phase)
                ax.plot(x1 + origin, y1, color='blue', linestyle='--')

                x2, y2 = self.create_circle_section(radius2, start_angle=start_angle_2, end_angle=stop_angle_2, phase=phase)
                ax.plot(x2 + origin, y2, color='red', linestyle='--')

                # Replot the rack and lines
                angle = phase % (2*np.pi)
                x_end_circle1 = radius1 * np.cos(stop_angle_1 + angle) + origin
                y_end_circle1 = radius1 * np.sin(stop_angle_1 + angle)
                x_start_circle1 = radius1 * np.cos(start_angle_1 + angle) + origin
                y_start_circle1 = radius1 * np.sin(start_angle_1 + angle)

                x_end_circle2 = radius2 * np.cos(stop_angle_2 + angle) + origin
                y_end_circle2 = radius2 * np.sin(stop_angle_2 + angle)
                x_start_circle2 = radius2 * np.cos(start_angle_2 + angle) + origin
                y_start_circle2 = radius2 * np.sin(start_angle_2 + angle)

                ax.plot([x_end_circle2, x_start_circle1], [y_end_circle2, y_start_circle1], color='black', linestyle='-')
                ax.plot([x_start_circle2, x_end_circle1], [y_start_circle2, y_end_circle1], color='black', linestyle='-')
                ax.plot([x_start_circle1, x_end_circle1], [y_start_circle1, y_end_circle1], color='black', linestyle='-')

                rack_displacement = self.rack_displacement(angle, forward_angle, radius1, radius2)

                ax.plot([-inst["x_limit"] / 2 + origin + rack_displacement, inst["x_limit"] / 2 + origin + rack_displacement], [radius1, radius1], color='blue', linestyle='--')
                ax.plot([-inst["x_limit"] / 2 + origin + rack_displacement, inst["x_limit"] / 2 + origin + rack_displacement], [-radius2, -radius2], color='red', linestyle='--')
                ax.plot([-inst["x_limit"] / 2 + origin + rack_displacement, -inst["x_limit"] / 2 + origin + rack_displacement], [radius1, -radius2], color='black', linestyle='-')
                ax.plot([inst["x_limit"] / 2 + origin + rack_displacement, inst["x_limit"] / 2 + origin + rack_displacement], [radius1, -radius2], color='black', linestyle='-')

                ax.plot(origin, 0, 'ko')

            ax.set_aspect('equal', adjustable='box')
            ax.set_title(f'Mechanism 1 (n={len(self.settings["instances"])})')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.grid(True)
            x_limit = self.settings["x_limit"]
            y_limit = self.settings["y_limit"]
            self.settings["x_limit"] = x_limit
            self.settings["y_limit"] = y_limit


            ax.set_xlim(-x_limit/2, x_limit/2)
            ax.set_ylim(-y_limit/2, y_limit/2)
            ax.axis('off')

        self.ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=interval, repeat=True)
        return self
    
    @staticmethod
    def info():
        description = (
            "Mechanism Description:\n"
            "-----------------------\n"
            "This mechanism is a reciprocating linear motion system featuring constant velocity and a quick return mechanism. "
            "It is constructed using two racks and two pinions, designed to convert rotary motion into linear motion with specific characteristics:\n"
            "\n"
            "- **Constant Velocity:** The mechanism ensures a uniform linear speed during the forward stroke, providing smooth and consistent motion.\n"
            "- **Quick Return:** It incorporates a quick return feature, which means the return stroke (or reverse movement) is faster than the forward stroke. This is achieved by utilizing a specific gear ratio and mechanical design to reduce the time taken for the return phase.\n"
            "- **Adjustable Parameters:** Key parameters such as the radius of the pinions, the gear ratios, and the center distance between the racks can be adjusted to suit different applications and performance requirements.\n"
            "\n"
            "This mechanism is a modified version of Mechanism 114 from the classic reference [507 Mechanical Movements](https://507movements.com/mm_114.html). The original Mechanism 114 does not feature the quick return functionality, whereas this modified version includes it to enhance the performance and efficiency of the reciprocating motion.\n"
            "\n"
            "**Disadvantage**:\n"
            "One notable disadvantage of this mechanism is the potential for shock loading. This occurs due to the instantaneous change in speed at the ends of the strokes, where the mechanism transitions from forward to return motion and vice versa. This sudden change in speed can result in mechanical stress and vibrations, which may lead to wear and tear or reduced longevity of the components if not properly managed.\n"
            "\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development of clamp-on self-actuated long-range linear motion mechanisms.\n"
        )
        return description