"""
PLAXIS 3D Tool – Create Simplified Building Facade

This version:
- Uses fixed values for building and footing geometry
- Creates facade with windows, doors, lintels, and interfaces
- No material assignment
- Simple GUI with a "Create" button

Author: Unina Automation
"""

import easygui
import plxscripting.easy as easy
from plxscripting.plx_scripting_exceptions import PlxScriptingError

def main():
    s_i, g_i = easy.new_server()

    # Ask user for offsets
    input_fields = ["x_offset (m)", "y_offset (m)", "rotation"]
    default_values = ["0", "0","0"]
    title = "PLAXIS 3D - Set Offset"
    msg = "Enter offsets from facade center to model main axis:"
    values = easygui.multenterbox(msg, title, input_fields, default_values)

    # GUI confirmation


    try:
        # Constants
        ymax = 80
        xmax = 80
        x_offset = float(values[0])
        y_offset = float(values[1])

        building_thickness = 0.4
        footing_thickness = 1.0
        foot_d = 0.5
        footing_height = 0.5
        footing_depth = footing_height + foot_d

        building_length = 40
        building_height = 8

        window_width = 1.5
        window_height = 2.0
        door_width = 2.0
        door_height = 3.0
        window_bottom = 1.0
        window_lintel_height = 0.4
        window_lintel_extra_width = 0.4
        door_lintel_height = 0.4
        door_lintel_extra_width = 0.4
        door_offset = 0.25
        ground_level = 0
        theta = float(values[2])

        # Helper functions
        def create_window(x, y, z, w, h):
            return g_i.surface((x, y, z), (x, y, z+h), (x+w, y, z+h), (x+w, y, z))

        def create_lintel(x, y, z, w, lh, extra):
            return g_i.surface((x-extra, y, z), (x-extra, y, z+lh),
                               (x+w+extra, y, z+lh), (x+w+extra, y, z))

        g_i.gotostructures()
        [g_i.delete(s) for s in g_i.Surfaces]
        [g_i.delete(v) for v in g_i.Volumes]

        # Main building face
        x1 = x_offset - (building_length) / 2
        y1 = y_offset - (building_thickness) / 2
        z1 = ground_level - footing_depth + footing_height
        x2 = x_offset + (building_length) / 2
        y2 = y_offset + (building_thickness) / 2
        z2 = building_height

        g_i.surface((x1, y1, z1), (x1, y1, z2), (x2, y1, z2), (x2, y1, z1))
        # === Create windows and doors on the ground floor ===
        win_z = ground_level + window_bottom
        win_z2 = ground_level + window_bottom + window_height + 2.0
        door_z = ground_level

        # Room (1) window
        win_x = x1 + 2.25
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (2) window
        win_x = x1 + 2.25 + 1.5 + 1.5
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (3) door
        door_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.5
        create_window(door_x, y1, door_z, door_width, door_height)
        create_lintel(door_x, y1, door_z + door_height, door_width, door_lintel_height, door_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)


        # Room (4) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (5) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (6) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 +2.25
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (7) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2.25 + 1.5 + 1.5
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (8) door
        door_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2.25 + 1.5 + 1.5 + 1.5 + 2.5
        create_window(door_x, y1, door_z, door_width, door_height)
        create_lintel(door_x, y1, door_z + door_height, door_width, door_lintel_height, door_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (9) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Room (10) window
        win_x = x1 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2.25 + 1.5 + 1.5 + 1.5 + 2.25 + 2 + 2.25 + 1.5 + 1.5
        create_window(win_x, y1, win_z, window_width, window_height)
        create_lintel(win_x, y1, win_z + window_height, window_width, window_lintel_height, window_lintel_extra_width)
        create_window(win_x, y1, win_z2, window_width, window_height)
        create_lintel(win_x, y1, win_z2 + window_height, window_width, window_lintel_height, window_lintel_extra_width)

        # Intersect and extrude full structure
        g_i.intersect(*g_i.Surfaces[:])
        g_i.extrude(g_i.Surfaces[:], 0, building_thickness, 0)
        g_i.delete(*g_i.Surfaces[:])
        g_i.delete(*g_i.Volumes[10:20])
        g_i.delete(*g_i.Volumes[21:31])

        # Footing surface and interfaces
        foot_z = -footing_depth
        surface_foot = g_i.surface(
            x1, y_offset - (footing_thickness)/2, foot_z,
            x1, y_offset + (footing_thickness)/2, foot_z,
            x2, y_offset + (footing_thickness)/2, foot_z,
            x2, y_offset - (footing_thickness)/2, foot_z
        )
        g_i.extrude(surface_foot, 0, 0, footing_height)
        g_i.rotate(g_i.Surfaces[:], (x_offset, y_offset, 0), 0, 0, -theta)
        g_i.rotate(g_i.Volumes[:], (x_offset, y_offset, 0), 0, 0, -theta)

        easygui.msgbox("Simplified facade created successfully.", "PLAXIS 3D")

    except PlxScriptingError as e:
        easygui.msgbox(f"PLAXIS scripting error:\n{str(e)}", "PLAXIS 3D - Error")
    except Exception as ex:
        easygui.msgbox(f"Unexpected error:\n{str(ex)}", "PLAXIS 3D - Error")

if __name__ == "__main__":
    main()
