import numpy as np
import pandas as pd
from civilpy.general import units
from civilpy.structural.arema import CooperE80

soil_unit_weight = 117.7 * units('lbf/ft^3')
soil_angle_int_friction = 29.8 * units('degrees')
angle_back_wall_with_horizontal = 0 * units('degrees')
angle_of_wall_friction_delta = 0 * units('degrees')
angle_of_wall_friction_gamma = 90 * units('degrees')
load_scale = 2.9059 * units('kips/ft')
wall_height = 19.5
soil_height_above_wall = 4.4
num_slices = 19
total_length = 38
track_offset = 2

cooper_e80 = CooperE80()

def find_key_for_value_in_tuple_range(data, number):
    """
    Find the key in a dictionary where the number falls between the first two values of the tuple.

    Parameters:
    data (dict): Dictionary containing lists of tuples.
    number (float): The number to search for within the tuple ranges.

    Returns:
    key: The key in the dictionary whose tuple contains the number, or None if not found.
    """
    for key, values in data.items():
        if len(values) >= 2 and values[0].magnitude <= number <= values[1].magnitude:
            return key
    return None

# Coordinates
coordinates_list = {
    # "A": (0, wall_height, find_key_for_value_in_tuple_range(cooper_e80.linear_loads, 0)), # See Excel comment - overridden to match sheet
    "A": (0, 23.9, find_key_for_value_in_tuple_range(cooper_e80.linear_loads, 0)),
    "B": (0, 0, None),
}

# Build a list of C values based on the user input
for x in range(0, num_slices):
    coordinates_list[f"C_{x+1}"] = (
        x * (total_length/num_slices) + track_offset,
        wall_height + soil_height_above_wall,
        find_key_for_value_in_tuple_range(cooper_e80.linear_loads, x * total_length/num_slices)
    )

class CulmansMethod:
    def __init__(
            self,
            soil_unit_weight = 117.7 * units('lbf/ft^3'),
            soil_angle_int_friction = 29.8 * units('degrees'),
            angle_back_wall_with_horizontal = 0 * units('degrees'),
            angle_of_wall_friction_delta = 0 * units('degrees'),
            angle_of_wall_friction_gamma = 90 * units('degrees'),
            load_scale = 2.9059 * units('kips/ft'),
            wall_height = 19.5 * units('ft'),
            soil_height_above_wall = 4.4 * units('ft'),
            num_slices = 19,
            total_length = 38 * units('ft'),
            track_offset = 2 * units('ft')
    ):
        self.soil_unit_weight = soil_unit_weight
        self.soil_angle_int_friction = soil_angle_int_friction
        self.angle_back_wall_with_horizontal = angle_back_wall_with_horizontal
        self.angle_of_wall_friction_delta = angle_of_wall_friction_delta
        self.angle_of_wall_friction_gamma = angle_of_wall_friction_gamma
        self.load_scale = load_scale
        self.wall_height = wall_height
        self.soil_height_above_wall = soil_height_above_wall
        self.num_slices = num_slices
        self.total_length = total_length
        self.track_offset = track_offset

    def calculate_a_i(x_val, y_val):
        """Calculate a_i (ft) based on the current coordinates."""
        result = np.sqrt((x_val * units.ft) ** 2 + (y_val * units.ft) ** 2)
        return result.to(units.ft).round(4)

    def calculate_c_i(current_key, keys, coordinates_list):
        """Calculate c_i (ft) based on the previous coordinates. If first point, refer to point 'A'."""
        if current_key == 'C_1':
            prev_x_val, prev_y_val, _ = coordinates_list['A']
        else:
            prev_x_val, prev_y_val, _ = coordinates_list[keys[keys.index(current_key) - 1]]
        result = np.sqrt((prev_x_val * units.ft) ** 2 + (prev_y_val * units.ft) ** 2)
        return result.to(units.ft).round(4)

    def calculate_b_i(current_key, keys, coordinates_list, x_val, y_val):
        """Calculate b_i (ft) using the previous point's coordinates."""
        if current_key == 'C_1':
            prev_x_val, prev_y_val, _ = coordinates_list['A']
        else:
            prev_key = keys[keys.index(current_key) - 1]
            prev_x_val, prev_y_val, _ = coordinates_list[prev_key]
        result = np.sqrt(((x_val - prev_x_val) * units.ft) ** 2 + ((y_val - prev_y_val) * units.ft) ** 2)
        return result.to(units.ft).round(4)

    def calculate_s_i(a_i, b_i, c_i):
        """Calculate s_i (ft) as the semi-perimeter of the triangle."""
        result = (a_i + b_i + c_i) / 2
        return result.to(units.ft).round(4)

    def calculate_A_i(s_i, a_i, b_i, c_i):
        """Calculate area A_i (ft^2) using the formula provided."""
        try:
            area = np.sqrt(s_i * (s_i - a_i) * (s_i - b_i) * (s_i - c_i))
        except ValueError:
            area = 0 * units.ft ** 2  # Set to 0 if there is a math domain error
        return area.to(units.ft ** 2).round(4)

    def calculate_x_cgi(x_val, next_x_val):
        """Calculate x_{cgi} (ft) as the center of gravity x-coordinate."""
        result = ((x_val + next_x_val) / 3) * units.ft
        return result.to(units.ft).round(4)

    def calculate_y_cgi(y_val, next_y_val):
        """Calculate y_{cgi} (ft) as the center of gravity y-coordinate."""
        result = ((y_val + next_y_val) / 3) * units.ft
        return result.to(units.ft).round(4)

    def calculate_running_total(values):
        """Calculate running total (ft) for a list of values."""
        total = 0 * units.ft
        running_totals = []
        for value in values:
            total += value
            running_totals.append(total.to(units.ft))
        return running_totals

    def calculate_w_i(A_i, soil_unit_weight):
        """Calculate w_i (lbf/ft) as the incremental weight of the triangle per unit length."""
        volume = A_i * units.ft  # The height of each wedge in 3D space would be 1 ft for consistency
        result = (volume * soil_unit_weight / units.ft).to(units.lbf / units.ft)
        return result.to_compact().round(4)

    def calculate_cumulative_weights(values):
        """Calculate cumulative weights (lbf/ft) for a list of values."""
        total = 0 * units.lbf / units.ft
        cumulative_weights = []
        for value in values:
            total += value
            cumulative_weights.append(total.to(units.lbf / units.ft).round(4))
        return cumulative_weights


    def calculate_columns(self, coordinates_list, soil_unit_weight):
        results = []
        keys = list(coordinates_list.keys())
        x_cgi_list = []
        y_cgi_list = []
        w_i_list = []

        for i in range(len(keys)):
            key = keys[i]
            if key in ['A', 'B']:
                continue

            x_val, y_val, _ = coordinates_list[key]

            a_i = self.calculate_a_i(x_val, y_val)
            c_i = self.calculate_c_i(key, keys, coordinates_list)
            b_i = self.calculate_b_i(key, keys, coordinates_list, x_val, y_val)
            s_i = self.calculate_s_i(a_i, b_i, c_i)
            A_i = self.calculate_A_i(s_i, a_i, b_i, c_i)

            # Calculate x_{cgi} and y_{cgi}
            if key == 'C_1':
                prev_x_val, prev_y_val, _ = coordinates_list['A']
            else:
                prev_x_val, prev_y_val, _ = coordinates_list[keys[i - 1]]

            x_cgi = self.calculate_x_cgi(prev_x_val, x_val)
            y_cgi = self.calculate_y_cgi(prev_y_val, y_val)

            x_cgi_list.append(x_cgi)
            y_cgi_list.append(y_cgi)

            w_i = self.calculate_w_i(A_i, soil_unit_weight)
            w_i_list.append(w_i)

            row_data = {
                'c_i (ft)': c_i,
                'a_i (ft)': a_i,
                'b_i (ft)': b_i,
                's_i (ft)': s_i,
                'A_i (ft^2)': A_i,
                'x_{cgi} (ft)': x_cgi,
                'y_{cgi} (ft)': y_cgi,
                'w_i (lbf)': w_i.to('lbf/ft').round(4)
            }
            results.append(row_data)

        # Calculate running totals for x_{ccgi}, y_{ccgi}, and W_i
        x_ccgi_list = self.calculate_running_total(x_cgi_list)
        y_ccgi_list = self.calculate_running_total(y_cgi_list)
        W_i_list = self.calculate_cumulative_weights(w_i_list)

        for i in range(len(results)):
            results[i]['x_{ccgi} (ft)'] = x_ccgi_list[i].round(4)
            results[i]['y_{ccgi} (ft)'] = y_ccgi_list[i].round(4)
            results[i]['W_i (lbf)'] = W_i_list[i].round(4)

        df = pd.DataFrame(results)
        df.index += 1
        df.index.name = 'Wedge Number'

        # Reorder columns
        df = df[['c_i (ft)', 'a_i (ft)', 'b_i (ft)', 's_i (ft)', 'A_i (ft^2)',
                 'x_{cgi} (ft)', 'y_{cgi} (ft)', 'x_{ccgi} (ft)', 'y_{ccgi} (ft)',
                 'w_i (lbf)', 'W_i (lbf)']]

        return df