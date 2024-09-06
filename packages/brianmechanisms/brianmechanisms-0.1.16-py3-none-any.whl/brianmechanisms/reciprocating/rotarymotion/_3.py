import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter


class mechanism3:
    def __init__(self, settings):
        self.settings = settings
        self.ani = None
        pass 

    @staticmethod
    def calculate_radius2(radius1, gear1_angle):
        radius2 = (gear1_angle * radius1) / (2 * np.pi - gear1_angle)
        return radius2
    
    @staticmethod
    def Settings(options, center_distance = 0, fig = None, ax = None, grid=False, rotations = 1, speed = 0.5, n=3):
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
            n = instance.get('n',n)
            instance["n"] = n
            speed = instance.get('speed',speed)
            instance["speed"] = speed
            segment_angle = 2*np.pi / n
            instance["segment_angle"] = segment_angle
            # instance["offset_angle"] = (-segment_angle/2-np.pi/2 + 2*np.pi) % (2*np.pi)
            # instance["offset_angle"] = (-segment_angle + 2*np.pi) % (2*np.pi)
            instance["offset_angle"] = (-np.pi/2 + 2*np.pi) % (2*np.pi)
            instance["start_angle_1"] = instance["offset_angle"]
            instance["stop_angle_1"] = instance.get('start_angle_1') + segment_angle

            # instance["radius2"] = mechanism3.calculate_radius2(instance.get('radius1', 0), forward_angle)
            radii_2.append(instance["radius1"]) ## fix
            displacements.append(segment_angle * instance.get('radius1', 0))
            instance["displacement"] = segment_angle * instance.get('radius1', 0)
            instance["x_limit"] = instance["displacement"]+10
            if center_distance == 0:
                center_distance =2*segment_angle * instance.get('radius1', 0)+10
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
        y_limit = 2 * max(radii_2) *5

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

    def rack_displacement(self, angle, radius1, segment_angle):
        # angle = angle %(2*np.pi)
        # reversing_angle = angle
        # if angle <= segment_angle:
        #     displacement = -angle * radius1
            
        # elif angle <= 2 * segment_angle:
        #     last_position = -segment_angle * radius1
        #     displacement = last_position + (angle - segment_angle) * radius1 
        #     reversing_angle *= -1
        # elif angle <= 3 * segment_angle:
        #     last_position = 0
        #     displacement = last_position - (angle - 2*segment_angle) * radius1 
        # else:
        #     last_position = -segment_angle * radius1
        #     displacement = last_position + (angle - 3*segment_angle) * radius1
        #     reversing_angle *= -1
        angle = angle % (2 * np.pi)  # Normalize angle
        reversing_angle = angle
        displacement = 0
        last_position = 0

        # Iterate through segments
        num_segments = int(np.ceil((2 * np.pi) / segment_angle))
        for i in range(num_segments):
            # Calculate the start and end angle of the current segment
            start_angle = i * segment_angle
            end_angle = (i + 1) * segment_angle
            # Update last_position for the next segment
            if i % 2 == 0:
                last_position = 0 #start_angle * radius1
            else:
                last_position = -segment_angle * radius1 #start_angle * radius1 - segment_angle * radius1

            if angle <= end_angle:
                # Calculate displacement for the current segment
                if i % 2 == 0:
                    # displacement = last_position - (angle - 2*segment_angle) * radius1
                    displacement = last_position - (angle - start_angle) * radius1
                else:
                    displacement = last_position + (angle - start_angle) * radius1
                    reversing_angle = -1 * angle

                break

            
        
        displacement *= -1
        return (displacement,reversing_angle)

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
            radius2 = inst.get('radius2', 0)
            start_angle_1 = inst.get('start_angle_1', 0)
            stop_angle_1 = inst.get('stop_angle_1', 0)
            origin = inst.get('origin', 0)
            x_limit = inst.get("x_limit")
            offset_angle = inst.get("offset_angle")
            segment_angle = inst.get("segment_angle")

            section_colors = ["blue", "red"]
            # for i in range(self.settings["n"]):
            for i in range(inst.get("n")):
                color_index = i%len(section_colors)
                x1, y1 = self.create_circle_section(radius1, start_angle=start_angle_1+i*segment_angle, end_angle=stop_angle_1+i*segment_angle)
                ax.plot(x1 + origin, y1, label=f'Larger Circle Section (Origin {origin})', color=section_colors[color_index], linestyle='--')

                stop_angle = (stop_angle_1 +i*segment_angle)%(2*np.pi)
                start_angle = (start_angle_1 +i*segment_angle)%(2*np.pi)
                x_end_circle1 = radius1 * np.cos(stop_angle)
                y_end_circle1 = radius1 * np.sin(stop_angle)
                x_start_circle1 = radius1 * np.cos(start_angle)
                y_start_circle1 = radius1 * np.sin(start_angle)

                ax.plot([0+ origin, x_end_circle1+ origin], [0, y_end_circle1], color='black', linestyle='-')
            ax.plot(origin, 0, 'ko')

            # pinion 2
            x1, y1 = self.create_circle_section(radius2, start_angle=0, end_angle=2*np.pi)
            ax.plot(x1 + origin, y1-radius1-radius2, color="blue", linestyle='--')
            ax.plot(origin, -radius1-radius2, 'ko')

            # # # Add dashed horizontal lines
            rack_displacement = 0
            ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1, -radius1], color='red', linestyle='--')
            ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1-radius2*2, -radius1-radius2*2], color='blue', linestyle='--')
            ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1-radius2*4, -radius1-radius2*4], color='black', linestyle='--')

            # # # Connect the starts and ends of the lines
            ax.plot([-x_limit/2 + origin+rack_displacement, -x_limit/2 + origin+rack_displacement], [-radius1, -radius1-radius2*4], color='black', linestyle='-')
            ax.plot([x_limit/2+origin+rack_displacement, x_limit/2+origin+rack_displacement], [-radius1, -radius1-radius2*4], color='black', linestyle='-')

            x1, y1 = self.create_circle_section(radius1, start_angle=0, end_angle=2*np.pi)
            ax.plot(x1 + origin, y1-radius1*2-radius2*4, color="black", linestyle='--')
            ax.plot(origin, -radius1*2-radius2*4, 'ko')

            ax.plot([0+ origin, 0+ origin], [-radius1*2-radius2*4, -radius1*3-radius2*4], color='black', linestyle='-')


        # Set plot settings
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f'Mechanism 3')
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
                phase = (frame * rotation / total_frames)

                radius1 = inst.get('radius1', 0)
                radius2 = inst.get('radius2', 0)
                start_angle_1 = inst.get('start_angle_1', 0)
                stop_angle_1 = inst.get('stop_angle_1', 0)
                origin = inst.get('origin', 0)
                x_limit = inst.get("x_limit")
                offset_angle = inst.get("offset_angle")
                segment_angle = inst.get("segment_angle")

                section_colors = ["blue", "red"]
                for i in range(inst["n"]):
                    color_index = i%len(section_colors)
                    x1, y1 = self.create_circle_section(radius1, start_angle=start_angle_1+i*segment_angle, end_angle=stop_angle_1+i*segment_angle, phase=phase)
                    ax.plot(x1 + origin, y1, label=f'Larger Circle Section (Origin {origin})', color=section_colors[color_index], linestyle='--')

                    stop_angle = (stop_angle_1 +i*segment_angle+phase)%(2*np.pi)
                    start_angle = (start_angle_1 +i*segment_angle+phase)%(2*np.pi)
                    x_end_circle1 = radius1 * np.cos(stop_angle)
                    y_end_circle1 = radius1 * np.sin(stop_angle)
                    x_start_circle1 = radius1 * np.cos(start_angle)
                    y_start_circle1 = radius1 * np.sin(start_angle)

                    ax.plot([0+ origin, x_end_circle1+ origin], [0, y_end_circle1], color='black', linestyle='-')
                ax.plot(origin, 0, 'ko')

                rack_displacement,reverse_angle = self.rack_displacement(phase, radius1, inst.get("segment_angle"))
                # pinion 2
                x1, y1 = self.create_circle_section(radius2, start_angle=0, end_angle=2*np.pi,phase=reverse_angle*inst["n"])
                ax.plot(x1 + origin, y1-radius1-radius2, color="blue", linestyle='--')
                ax.plot(origin, -radius1-radius2, 'ko')

                # # # # Add dashed horizontal lines
                # rack_displacement = 0
                ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1, -radius1], color='red', linestyle='--')
                ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1-radius2*2, -radius1-radius2*2], color='blue', linestyle='--')
                ax.plot([-x_limit/2 + origin+rack_displacement, x_limit/2 + origin+rack_displacement], [-radius1-radius2*4, -radius1-radius2*4], color='black', linestyle='--')

                # # # Connect the starts and ends of the lines
                ax.plot([-x_limit/2 + origin+rack_displacement, -x_limit/2 + origin+rack_displacement], [-radius1, -radius1-radius2*4], color='black', linestyle='-')
                ax.plot([x_limit/2+origin+rack_displacement, x_limit/2+origin+rack_displacement], [-radius1, -radius1-radius2*4], color='black', linestyle='-')

                x1, y1 = self.create_circle_section(radius1, start_angle=0, end_angle=2*np.pi, phase=reverse_angle*-1)
                ax.plot(x1 + origin, y1-radius1*2-radius2*4, color="black", linestyle='--')
                ax.plot(origin, -radius1*2-radius2*4, 'ko')


                max_displacement,_ = self.rack_displacement(inst.get("segment_angle"), radius1, inst.get("segment_angle"))
                output_angle = -1*(rack_displacement/max_displacement * inst.get("segment_angle")) +1.5* np.pi
                # if output_angle > 0:
                #     output_angle = -output_angle
                x_end_circle1 = radius1 * np.cos((output_angle)%(2*np.pi))
                y_end_circle1 = radius1 * np.sin((output_angle)%(2*np.pi))
                ax.plot([0+ origin, x_end_circle1+ origin], [-radius1*2-radius2*4, y_end_circle1-radius1*2-radius2*4], color='black', linestyle='-')

            ax.set_aspect('equal', adjustable='box')
            ax.set_title(f'Mechanism 3')
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
            "This mechanism is a for converting constant velocity rotary input to oscillating rotary output. "
            "It is constructed using a compound mangled pinion, 2 full pinions and 2 racks:\n"
            "\n"
            "Use with { n ∈ ℤ ∣ n is even and n > 2 }"
            "\n"
            "- **Constant Velocity:** The mechanism ensures a uniform linear speed during the forward stroke, providing smooth and consistent motion.\n"
            "- **Quick Return:** It incorporates a quick return feature, which means the return stroke (or reverse movement) is faster than the forward stroke. This is achieved by utilizing a specific gear ratio and mechanical design to reduce the time taken for the return phase.\n"
            "- **Adjustable Parameters:** Key parameters such as the radius of the pinions, the gear ratios, and the center distance between the racks can be adjusted to suit different applications and performance requirements.\n"
            "\n"
            "**Disadvantage**:\n"
            "One notable disadvantage of this mechanism is the potential for shock loading. This occurs due to the instantaneous change in direction at the ends of the strokes, where the mechanism transitions from forward to return motion and vice versa. This sudden change in speed can result in mechanical stress and vibrations, which may lead to wear and tear or reduced longevity of the components if not properly managed.\n"
            "\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development levelling systems for rimless wheels.\n"
        )
        return description