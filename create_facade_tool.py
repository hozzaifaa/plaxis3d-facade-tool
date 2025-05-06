"""
PLAXIS 3D Tool – Create Simplified Building Facade

This version:
- Uses fixed values for building and footing geometry
- Creates facade with windows, doors, lintels, and interfaces
- No material assignment
- Simple GUI with a "Create" button

Author: Hozaifa
"""

import easygui
import plxscripting.easy as easy
from plxscripting.plx_scripting_exceptions import PlxScriptingError

def main():
    s_i, g_i = easy.new_server()


    # User inputs
    input_fields = [
        "x_offset (m)", "y_offset (m)", "z_offset (m)", "rotation (theta, degrees)",
        "building_thickness (m)", "footing_thickness (m)", "foot_d (m)", "footing_height (m)",
        "building_length (m)", "building_height (m)"
    ]
    default_values = ["0", "0", "0", "0", "0.4", "1.0", "0.5", "0.5", "40", "8"]
    title = "PLAXIS 3D - Set Parameters"
    msg = "Enter building geometry and offset parameters:"
    values = easygui.multenterbox(msg, title, input_fields, default_values)

    if values is None:
        return #User cancelled

    # Checkbox for optional elements
    choice_msg = "Select optional components to include:"
    include_windows = easygui.boolbox("Include windows and lintels?", "Optional Elements", ["Yes", "No"])
    include_interfaces = easygui.boolbox("Include interfaces?", "Optional Elements", ["Yes", "No"])


    try:
        # Assign parameters
        x_offset = float(values[0])
        y_offset = float(values[1])
        z_offset = float(values[2])
        theta = float(values[3])

        building_thickness = float(values[4])
        footing_thickness = float(values[5])
        foot_d = float(values[6])
        footing_height = float(values[7])
        footing_depth = footing_height + foot_d

        building_length = float(values[8])
        building_height = float(values[9])

        # Fixed constants
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

        
        material_lintel = g_i.soilmat(
            "Identification", "Lintel",
            "SoilModel", "Linear Elastic",
            "DrainageType", "Non-porous",
            "gammaUnsat", 19.62,
            "ERef", 2E6,
            "nu", 0.2
        )
        material_NL = g_i.soilmat(
            "Identification","NL4",
            "Soilmodel","User-defined",
            "DllFile", "iso_jrmc64.dll",
            "ModelInDll", "<model1>",
            "DrainageType","Non-porous",
            "gammaUnsat", 19.62,             #   gamma_unsat: 19.62 kN/m³
            "EoedInter", 2.0E6,              #   E_oed: 2.0E6 kN/m²
            "CInter",1000,                   #   C_ref_inter: 1000 kN/m²
            "User1",1,                       #1: iSet (1..100): 1
            "User2",3,                       #2: 2D / 3D (2 or 3)): 3
            "User3",830.0E3,                 #3: G: 830.0E3 kN/m²
            "User4",0.2,                   #4: nu: 0.295 
            "User5",1000,                    #5: C_mc: 1000 kN/m²
            "User6",40,                      #6: phi_mc: 40 °
            "User7",0,                       #7: psi_mc: 0 °
            "User8",1000,                    #8: tens_mc: 1000 kN/m²
            "User9",2,                       #9: nPlanes (2 or 3): 2 
            "User10",0.636,                  #10: SF_beta: 0.636 
            "User11",90,                     #11: 1:alpha_1: 90 °
            "User12",90,                     #12: 1:alpha_2: 90 °
            "User13",200,                    #13: C_1: 200 kN/m²
            "User14",23.27,                  #14: phi_1: 23.27 °
            "User15",0,                      #15: psi_1: 0 °
            "User16",200,                    #16: tens_1: 200 kN/m²
            "User17",0,                      #17: 2:alpha_1: 0 °
            "User18",0,                      #18: 2:alpha_0: 0 °  
            "User19",200,                    #19: C_2: 200 kN/m²
            "User20",23.27,                  #20: phi_2: 23.27 °
            "User21",0,                      #21: psi_2 0 °
            "User22",200                    #22: tens_2: 200 kN/m²
        )
        material_EL = g_i.soilmat(
            "Identification", "EL",
            "SoilModel", "Linear Elastic",
            "DrainageType", "Non-porous",
            "gammaUnsat", 19.62,
            "nu", 0.2, 
            "ERef", 2.0E6
        )
        material_footing = g_i.soilmat(
            "Identification", "Footing",
            "SoilModel", "Linear Elastic",
            "DrainageType", "Non-porous",
            "gammaUnsat", 19.62,
            "nu", 0.2, 
            "ERef", 2.0E6
        )

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
        z1 = ground_level - footing_depth + footing_height + z_offset
        x2 = x_offset + (building_length) / 2
        y2 = y_offset + (building_thickness) / 2
        z2 = building_height + z_offset

        g_i.surface((x1, y1, z1), (x1, y1, z2), (x2, y1, z2), (x2, y1, z1))

        if include_windows:
            # === Create windows and doors on the ground floor ===
            win_z = ground_level + window_bottom + z_offset
            win_z2 = ground_level + window_bottom + window_height + 2.0 + z_offset
            door_z = ground_level + z_offset

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
            #g_i.delete(*g_i.Volumes[10:20]) 
            #g_i.delete(*g_i.Volumes[21:31])
        g_i.extrude(g_i.Surfaces[:], 0, building_thickness, 0)
        if include_windows:
            g_i.delete(*g_i.Volumes[10:20])
            g_i.delete(*g_i.Volumes[21:31])     
        g_i.delete(*g_i.Surfaces[:])

        # Footing surface and interfaces
        foot_z = -footing_depth + z_offset
        
        
        
        if include_interfaces:
            surface_foot1 = g_i.surface(x1, y_offset - (footing_thickness)/2, -footing_depth,
                                        x1, y_offset - (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset - (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset - (footing_thickness)/2, -footing_depth)
            surface_foot2 = g_i.surface(x1, y_offset + (footing_thickness)/2, -footing_depth,
                                        x1, y_offset + (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset + (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset + (footing_thickness)/2, -footing_depth)
            surface_foot3 = g_i.surface(x1, y_offset - (footing_thickness)/2, -footing_depth, 
                                        x1, y_offset - (footing_thickness)/2, -footing_depth+footing_height,
                                        x1, y_offset + (footing_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset + (footing_thickness)/2, -footing_depth)
            surface_foot4 = g_i.surface(x2, y_offset - (footing_thickness)/2, -footing_depth, 
                                        x2, y_offset - (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset + (footing_thickness)/2, -footing_depth+footing_height, 
                                        x2, y_offset + (footing_thickness)/2, -footing_depth)
            surface_foot5 = g_i.surface(x1, y_offset - (footing_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset - (building_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset - (building_thickness)/2, -footing_depth+footing_height, 
                                        x2, y_offset - (footing_thickness)/2, -footing_depth+footing_height)
            surface_foot6 = g_i.surface(x1, y_offset + (building_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset + (footing_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset + (footing_thickness)/2, -footing_depth+footing_height, 
                                        x2, y_offset + (building_thickness)/2, -footing_depth+footing_height)
            surface_foot7 = g_i.surface(x1, y_offset - (building_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset - (building_thickness)/2, 0,
                                        x2, y_offset - (building_thickness)/2, 0, 
                                        x2, y_offset - (building_thickness)/2, -footing_depth+footing_height)
            surface_foot8 = g_i.surface(x1, y_offset + (building_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset + (building_thickness)/2, 0,
                                        x2, y_offset + (building_thickness)/2, 0, 
                                        x2, y_offset + (building_thickness)/2, -footing_depth+footing_height)
            surface_foot9 = g_i.surface(x1, y_offset - (building_thickness)/2, -footing_depth+footing_height, 
                                        x1, y_offset - (building_thickness)/2, 0,
                                        x1, y_offset + (building_thickness)/2, 0, 
                                        x1, y_offset + (building_thickness)/2, -footing_depth+footing_height)
            surface_foot10 = g_i.surface(x2, y_offset -(building_thickness)/2, -footing_depth+footing_height,
                                        x2, y_offset -(building_thickness)/2, 0,
                                        x2, y_offset +(building_thickness)/2, 0, 
                                        x2, y_offset +(building_thickness)/2, -footing_depth+footing_height)
            surface_foot = g_i.surface(
                x1, y_offset - (footing_thickness)/2, foot_z,
                x1, y_offset + (footing_thickness)/2, foot_z,
                x2, y_offset + (footing_thickness)/2, foot_z,
                x2, y_offset - (footing_thickness)/2, foot_z
            )
            interface_g = g_i.neginterface(surface_foot1)
            interface_g = g_i.posinterface(surface_foot2)
            interface_g = g_i.posinterface(surface_foot3)
            interface_g = g_i.neginterface(surface_foot4)
            interface_g = g_i.neginterface(surface_foot5)
            interface_g = g_i.neginterface(surface_foot6)
            interface_g = g_i.neginterface(surface_foot7)
            interface_g = g_i.posinterface(surface_foot8)
            interface_g = g_i.posinterface(surface_foot9)
            interface_g = g_i.neginterface(surface_foot10)
            interface_g = g_i.posinterface(surface_foot)

        g_i.extrude(surface_foot, 0, 0, footing_height)

        
        #g_i.rotate(g_i.Surfaces[:], (x_offset, y_offset, 0), 0, 0, -theta)
        g_i.rotate(g_i.Volumes[:], (x_offset, y_offset, 0), 0, 0, -theta)
        # Set material for soils
        for i in range(22):
            g_i.Soils[i].Material = material_EL if i == 10 else material_lintel
        g_i.Soils[21].Material = material_footing

        easygui.msgbox("Simplified facade created successfully.", "PLAXIS 3D")

    except PlxScriptingError as e:
        easygui.msgbox(f"PLAXIS scripting error:\n{str(e)}", "PLAXIS 3D - Error")
    except Exception as ex:
        easygui.msgbox(f"Unexpected error:\n{str(ex)}", "PLAXIS 3D - Error")

if __name__ == "__main__":
    main()
