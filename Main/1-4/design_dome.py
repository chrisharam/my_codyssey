import math

material = ""
diameter = 0
thickness = 1
area = 0
weight = 0
gravity_mars = 0.38

meterial_mapping = {
    "glass" : 2.4,
    "aluminum" : 2.7,
    "carbon" : 7.85
}

def sphere_area(material="glass", diameter=1, thickness=1):
    global area, weight
    
    r = diameter/2  #radious
    r_cm = r * 100  # radious in cm
    area = 2 * math.pi * (r_cm ** 2)  #area of half sphere

    density = meterial_mapping.get(material) #default is glass
    weight = area * thickness * density * gravity_mars / 1000

    area = round(area,3)
    weight = round(weight, 3)


try:
    material = input("Enter your material(glass/aluminum/carbon): ").strip()
    if material not in meterial_mapping:
        raise ValueError(f"Material '{material}' is not supported.")
    
    diameter = input("Enter your diamter(has to be positive float type): ").strip()
    diameter = float(diameter)
    if diameter <= 0:
        raise ValueError("Diameter must be an positive float number")
    thickness_input = input("Enter your thickness(has to be positive float type)").strip()
    thickness = float(thickness_input) if thickness_input else 1
    if thickness <= 0:
        raise ValueError("thickness must be an positive float number")
    
    sphere_area(material,diameter,thickness)
    print(f"Material --> {material}, Diameter --> {diameter}, Thickness --> {thickness}, Area --> {area}, Weight --> {weight}kg")

except ValueError as e:
    print(f"input error: {e}")
except Exception as e:
    print(f"Unexptected error: ")


