import pandas as pd
 
def get_me_course_name():
    return "Fundamentals of Programming"

def get_me_number_of_students():
    return 5

 
def get_planetary_data():
    """
    Returns a pandas DataFrame containing the names, sizes, and masses of planets.
    """
    data = {
        "Planet": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        "Diameter (km)": [4879, 12104, 12742, 6779, 139820, 116460, 50724, 49244],
        "Mass (10^24 kg)": [0.33, 4.87, 5.97, 0.64, 1898, 568, 86.8, 102]
    }
    df = pd.DataFrame(data)
    return df
