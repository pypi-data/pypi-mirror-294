# import numpy as np
# import matplotlib.pyplot as plt
# import math
# from matplotlib.animation import FuncAnimation, PillowWriter

# class Settings:
#     def __init__(self, R1, R2, h, num_sets=1, fig=None, ax=None, speed = 0.5, displacement=10, return_fraction=0.5, grid=False):
#         self.R1 = R1
#         self.R2 = R2
#         self.h = h
#         self.num_sets = num_sets
#         if not fig:
#             fig, ax = plt.subplots()

#             ax.set_xlim(-150 * 3, 150 * 3)
#             ax.set_ylim(-150 - 2 * R1 - 5, 150 + 2 * R1 + 5)
#             ax.set_aspect('equal')
#             # ax.axis('off')
#         self.fig = fig 
#         self.ax = ax
#         if grid:
#             plt.grid(True)

#         interval = 50  # Interval between frames in milliseconds
#         self.speed = speed  # Frequency of the oscillation
#         self.num_teeth = 20  # Number of teeth on each gear
#         self.displacement = displacement
#         self.return_fraction = return_fraction



# class forward:
#     def __init__(self):
#         pass

# class reverse:
#     def __init__(self):
#         pass

# import matplotlib.pyplot as plt
# import numpy as np

# class displacement:
#     def __init__(self):
#         pass

#     def plot(self):
#         # Constants
#         self.Sp = 1  # Unit constant

#         # Generate values for R1/R2 from 0.5 to 2
#         self.R1_R2 = np.linspace(0.5, 5, 500)

#         # Calculate S_R (forward) using the formula S_R = Sp * (R1/R2 - 1)
#         self.S_R_forward = self.Sp * (self.R1_R2 - 1)

#         # Calculate S_R (return) using the formula S_R = Sp * (1 + R1/R2)
#         self.S_R_return = self.Sp * (1 + self.R1_R2)

#         # Calculate L_R using the formula L_R = S_R (forward) + Sp
#         self.L_R = self.S_R_forward + self.Sp

#         # Create a plot
#         self.figure, self.ax = plt.subplots(figsize=(8, 6))
        
#         # Plot S_R (forward)
#         self.ax.plot(self.R1_R2, self.S_R_forward, '--', label=r'$S_R (forward) = S_p \left(\frac{R_1}{R_2} - 1\right)$', color='red')
        
#         # Plot L_R
#         self.ax.plot(self.R1_R2, self.L_R, label=r'$L_R = S_R (forward) + S_p$')
        
#         # Plot S_R (return)
#         self.ax.plot(self.R1_R2, self.S_R_return, label=r'$S_R (return) = S_p \left(1 + \frac{R_1}{R_2}\right)$')
        
#         # Set labels and title
#         self.ax.set_xlabel(r'$\frac{R_1}{R_2}$')
#         self.ax.set_ylabel('Values')
#         self.ax.set_title(r'Plot of $S_R$ (forward), $S_R$ (return), and $L_R$ against $\frac{R_1}{R_2}$')
#         self.ax.grid(True)

#         # Add legend
#         self.ax.legend()
#         return self

#     def S_R_forward(self, S_p, R1, R2):
#         return S_p * (R1 / R2 - 1)

#     def L_forward(self, R1, R2):
#         return self.S_R_forward(self.Sp, R1, R2) + self.Sp


#     def show(self):
#         # Show the plot
#         plt.show()
#         return self

#     def save(self, imagePath):
#         # Save the plot to the specified image path
#         self.figure.savefig(imagePath)
#         return self
    

# class mechanism1:
#     def __init__(self, settings = None):
#         if settings:
#             self.settings = settings
#             self.ax = self.settings.ax
#             self.position = 0
        

#     def info(self):
#         return """
# This mechanism describes a theoretical reciprocating rectilinear gear system designed to achieve a quick return. It converts constant velocity continuous linear motion into reciprocating linear motion of constant velocity with (undesired) instantaneous change of direction.

# Since the input linear velocity is constant, an R1/R2 for the return gear set which gives an SR value which is less than that for the forward stroke is a quick return.
#         """
    
#     def plot(self):
#         self.draw_fixed_racks()
#         self.draw_mobile_rack()
#         return self

#     def draw_fixed_racks(self):
#         y1 = self.settings.h / 2
#         y2 = -self.settings.h / 2
#         x_min = -250
#         x_max = 250

#         # Draw the fixed racks
#         upper_rack_position = y1 + self.settings.R1 + 3 * self.settings.R2
#         lower_rack_position = y2 - self.settings.R1 - 3 * self.settings.R2
#         fixed_rack_upper = self.ax.plot([x_min, x_max], [upper_rack_position, upper_rack_position], 'k-')[0]
#         fixed_rack_lower = self.ax.plot([x_min, x_max], [lower_rack_position, lower_rack_position], 'k-')[0]

#     def draw_mobile_rack_section(self, set_number, stroke="forward/return"):
#         position = self.position
#         y1 = self.settings.h/2
#         ax = self.ax 
#         angle = self.settings.displacement/ self.settings.R2
#         len = angle * self.settings.R1
#         x_min = - len
#         x_max = 0

#         return_section_length = self.settings.displacement * self.settings.return_fraction
#         x_min = x_min if stroke == "forward" else x_max
#         x_max += 0 if stroke == "forward" else return_section_length
#         color = "k" if stroke == "forward" else 'b'
#         mobile_rack_top, = ax.plot([x_min, x_max], [y1, y1], f'{color}-')
#         mobile_rack_bottom, = ax.plot([x_min, x_max], [-y1, -y1], f'{color}-')
#         dotted_line_left, = ax.plot([x_min, x_min], [y1, -y1], f'{color}--')
#         dotted_line_right, = ax.plot([x_max, x_max], [y1, -y1],  f'{color}--')

#     def draw_mobile_rack(self, position=0):
#         num_sets = self.settings.num_sets
#         for i in range(0,num_sets):
#             print(i, num_sets)
#             self.draw_mobile_rack_section(i, stroke = "forward")
#             self.draw_mobile_rack_section(i, "return")
#         pass

#     def show(self):
#         plt.show()
#         return self


#     def save(self, fileName):
#         if self.ani is not None:
#             writer = PillowWriter(fps=25)
#             self.ani.save(f"{fileName}.gif", writer=writer)
#         else:
#             plt.savefig(f"{fileName}.png")
#         return self