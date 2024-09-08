import math
import numpy as np
import random
from typing import List, Dict, Tuple, Union, Optional

from .Classes import Line, LineSegment, Polygon
from .sample_in_polygon import sample_in_polygon, is_inside_polygon

def doLinesIntersect(line1: Line, line2: Line) -> Tuple[bool, Union[Tuple[float, float], None]]:
    """
    Check if two lines intersect and return the intersection point.

    Args:
    - line1 (Line): The first line segment.
    - line2 (Line): The second line segment.

    Returns:
    - intersect (bool): True if the lines intersect, False otherwise.
    - intersection_point (tuple or None): The intersection point (x, y) if lines intersect, None otherwise.
    """
    x1, y1 = line1.location
    v1, w1 = line1.direction

    x2, y2 = line2.location
    v2, w2 = line2.direction

    determinant = v1 * w2 - v2 * w1

    if determinant == 0:
        return False, (None, None)

    t1 = ((x2 - x1) * w2 - (y2 - y1) * v2) / determinant
    t2 = ((x2 - x1) * w1 - (y2 - y1) * v1) / determinant

    intersect_x = x1 + v1 * t1
    intersect_y = y2 + w2 * t2

    if -1e-6 < intersect_x < 1 + 1e-6 and -1e-6 < intersect_y < 1 + 1e-6:
        return True, (intersect_x, intersect_y)
    else:
        return False, (None, None)
    
def doSegmentsIntersect(
    segment1: LineSegment, 
    segment2: LineSegment
) -> Tuple[bool, Tuple[Optional[float], Optional[float]]]:
    """
    Determines if two line segments intersect and returns the intersection point if they do.

    Args:
        segment1 (LineSegment): The first line segment.
        segment2 (LineSegment): The second line segment.

    Returns:
        Tuple[bool, Tuple[Optional[float], Optional[float]]]:
            - A boolean indicating whether the segments intersect.
            - A tuple of the x and y coordinates of the intersection point if they intersect,
              otherwise (None, None).
    """
    
    # Create line equations based on the segments' start and end points
    line1 = Line(location=segment1.start, direction=np.array(segment1.end) - np.array(segment1.start))
    line2 = Line(location=segment2.start, direction=np.array(segment2.end) - np.array(segment2.start))
    
    # Check if the infinite extensions of the two lines intersect
    intersect, (intersect_x, intersect_y) = doLinesIntersect(line1, line2)
    
    # If no intersection, return False
    if not intersect:
        return False, (None, None)
    
    # Check if the intersection point is within the bounds of both segments in the x-direction
    xcheck = (
        (segment1.end[0] <= intersect_x <= segment1.start[0]
        or segment1.start[0] <= intersect_x <= segment1.end[0]
        or abs(intersect_x - segment1.end[0]) < 1e-6
        or abs(intersect_x - segment1.start[0]) < 1e-6)
        and
        (segment2.end[0] <= intersect_x <= segment2.start[0]
        or segment2.start[0] <= intersect_x <= segment2.end[0]
        or abs(intersect_x - segment2.end[0]) < 1e-6
        or abs(intersect_x - segment2.start[0]) < 1e-6)
    )
    
    # Check if the intersection point is within the bounds of both segments in the y-direction
    ycheck = (
        (segment1.end[1] <= intersect_y <= segment1.start[1]
        or segment1.start[1] <= intersect_y <= segment1.end[1]
        or abs(intersect_y - segment1.end[1]) < 1e-6
        or abs(intersect_y - segment1.start[1]) < 1e-6)
        and
        (segment2.end[1] <= intersect_y <= segment2.start[1]
        or segment2.start[1] <= intersect_y <= segment2.end[1]
        or abs(intersect_y - segment2.end[1]) < 1e-6
        or abs(intersect_y - segment2.start[1]) < 1e-6)
    )
    
    # If the intersection point lies within the bounds of both segments, return True with the intersection point
    if xcheck and ycheck:
        return True, (intersect_x, intersect_y)
    
    # Otherwise, return False and no intersection point
    return False, (None, None)

def pick_item_with_probability(
    polygon_arr: Dict[str, Dict[str, object]]
) -> Tuple[str, Dict[str, object]]:
    """
    Randomly selects an item from the polygon array with a probability proportional to the area of the polygons.

    Args:
        polygon_arr (Dict[str, Dict[str, object]]): 
            A dictionary where keys are polygon identifiers (e.g., 'p1', 'p2') and values are dictionaries containing polygon properties, 
            including an 'area' key that stores the area of the polygon.

    Returns:
        Tuple[str, Dict[str, object]]: 
            - The identifier of the selected polygon.
            - The corresponding polygon data (dictionary) containing its properties.
    """
    
    # Calculate the total weight (sum of areas of all polygons)
    max_weight = sum(pol['area'] for pol in polygon_arr.values())
    
    # Generate a random threshold between 0 and the total weight
    threshold = random.uniform(0, max_weight)
    cumulative_weight = 0
    
    # Iterate through the polygons, accumulating weights
    for item, pol in polygon_arr.items():
        weight = pol['area']
        cumulative_weight += weight
        
        # Return the polygon when the cumulative weight surpasses the threshold
        if cumulative_weight >= threshold:
            return item, pol

def get_location_and_direction(
    polygon_arr: Dict[str, Dict[str, object]], 
    thickness: float, 
    max_attempts: int = 1000, 
    angles: Union[str, List[float]] = 'uniform'
) -> Union[Tuple[str, Dict[str, object], Tuple[float, float], np.ndarray, np.ndarray], bool]:
    """
    Attempts to find a valid location and direction within a polygon for placing a new segment. The direction can either be randomly 
    chosen (uniformly) or from a specified list of angles. It ensures that the segment lies within the polygon's bounds given the 
    specified thickness.

    Args:
        polygon_arr (Dict[str, Dict[str, object]]): 
            A dictionary where the keys are polygon identifiers and the values are dictionaries containing polygon properties, including 'vertices'.
        thickness (float): 
            The thickness of the segment that needs to fit inside the polygon.
        max_attempts (int, optional): 
            The maximum number of attempts to find a valid location and direction. Defaults to 1000.
        angles (Union[str, List[float]], optional): 
            A string ('uniform' for random directions) or a list of angles (in radians) to choose the direction from. Defaults to 'uniform'.

    Returns:
        Union[Tuple[str, Dict[str, object], Tuple[float, float], np.ndarray, np.ndarray], bool]:
            - If a valid location and direction are found, returns a tuple containing:
                - The polygon ID (`str`).
                - The polygon data (`Dict[str, object]`).
                - The new location as a tuple of floats (`Tuple[float, float]`).
                - The direction vector as a numpy array (`np.ndarray`).
                - The perpendicular vector to the direction as a numpy array (`np.ndarray`).
            - Returns `False` if no valid location and direction are found after the maximum attempts.
    """
    
    # Generate a new direction based on the angles parameter
    if angles == 'uniform':
        direction = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        direction = direction / np.linalg.norm(direction)  # Normalize the direction vector
    else:
        directions = [ (np.cos(angle), np.sin(angle)) for angle in angles ]
        direction = random.choice(directions)
        direction = np.array(direction) / np.linalg.norm(direction)  # Normalize the chosen direction
    
    # Try to find a valid location and direction up to max_attempts
    attempt = 0
    while attempt < max_attempts:
        polygon_id, polygon = pick_item_with_probability(polygon_arr)
        
        # Sample a location within the polygon
        location_new = sample_in_polygon(polygon['vertices'])
        
        # Compute the perpendicular vector to the direction
        perpendicular = np.array([direction[1], -direction[0]])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)
        
        # Ensure the perpendicular vector is oriented consistently (y-component is non-negative)
        if perpendicular[1] < 0:
            perpendicular = -perpendicular
        
        # Compute the positions for the segment with thickness, shifted by half-thickness along the perpendicular direction
        p1 = np.array(location_new) + thickness / 2 * perpendicular
        p2 = np.array(location_new) - thickness / 2 * perpendicular
        
        # Check if both endpoints of the segment are inside the polygon
        if is_inside_polygon(polygon['vertices'], p1) and is_inside_polygon(polygon['vertices'], p2):
            return polygon_id, polygon, location_new, direction, perpendicular
        
        attempt += 1
    
    # If no valid location and direction is found, return False
    return False

def get_polygons(polygon_id, polygon_arr, neighbor1_1, neighbor1_2, vertex_begin_1, vertex_end_1, neighbor2_1, neighbor2_2, vertex_begin_2, vertex_end_2, segment_new_id_1, segment_new_id_2):
    # Extract vertices and cycle (faces) of the original polygon
    vertices = polygon_arr[polygon_id]['vertices']
    cycle = polygon_arr[polygon_id]['faces']
    
    # Get first cycle and vertices
    index_start_1, index_end_1 = (cycle.index(neighbor1_1), cycle.index(neighbor1_2))
    if index_start_1 < index_end_1:
        cycle1 = [segment_new_id_1] + cycle[index_start_1:index_end_1+1]
        vertices1 = [vertex_begin_1] + vertices[index_start_1:index_end_1] + [vertex_end_1]
    else:
        cycle1 = [segment_new_id_1] + cycle[index_start_1:] + cycle[:index_end_1+1]
        vertices1 = [vertex_begin_1] + vertices[index_start_1:] + vertices[:index_end_1] + [vertex_end_1]
        
    # Get second cycle and vertices
    index_start_2, index_end_2 = (cycle.index(neighbor2_2), cycle.index(neighbor2_1))
    if index_start_2 < index_end_2:
        cycle2 = [segment_new_id_2] + cycle[index_start_2:index_end_2+1]
        vertices2 = [vertex_end_2] + vertices[index_start_2:index_end_2] + [vertex_begin_2]
    else:
        cycle2 = [segment_new_id_2] + cycle[index_start_2:] + cycle[:index_end_2+1]
        vertices2 = [vertex_end_2] + vertices[index_start_2:] + vertices[:index_end_2] + [vertex_begin_2]
    
    # Get middle cycle and vertices
    cycle0 = [neighbor1_1, segment_new_id_1, neighbor1_2]
    vertices0 = [vertex_begin_1, vertex_end_1]
    
    index_start_0, index_end_0 = (cycle.index(neighbor1_2), cycle.index(neighbor2_2))
    if index_start_0 < index_end_0:
        cycle0 = cycle0 + cycle[index_start_0:index_end_0+1]
        vertices0 = vertices0 + vertices[index_start_0:index_end_0] 
        
    elif index_start_0 > index_end_0:
        cycle0 = cycle0 + cycle[index_start_0:] + cycle[:index_end_0+1]
        vertices0 = vertices0 + vertices[index_start_0:] + vertices[:index_end_0]
        
    cycle0 = cycle0 + [segment_new_id_2]
    vertices0 = vertices0 + [vertex_end_2] + [vertex_begin_2]
    
    index_start_0, index_end_0 = (cycle.index(neighbor2_1), cycle.index(neighbor1_1))
    if index_start_0 < index_end_0:
        cycle0 = cycle0 + cycle[index_start_0:index_end_0+1]
        vertices0 = vertices0 + vertices[index_start_0:index_end_0] 
        
    elif index_start_0 > index_end_0:
        cycle0 = cycle0 + cycle[index_start_0:] + cycle[:index_end_0+1]
        vertices0 = vertices0 + vertices[index_start_0:] + vertices[:index_end_0]
    
    return cycle0, vertices0, cycle1, vertices1, cycle2, vertices2

def get_new_segment(
    line_segments_to_check: List[LineSegment],
    location: Tuple[float, float], 
    direction: Tuple[float, float], 
    id: Optional[int] = None
) -> 'LineSegment':
    """
    Creates a new line segment by extending a given location in a specified direction and 
    determines its neighbors by checking intersections with other line segments.

    Args:
        line_segments_to_check (List[LineSegment]): List of existing line segments to check for intersections.
        location (Tuple[float, float]): The starting point (x, y) for the new line segment.
        direction (Tuple[float, float]): The direction vector in which to extend the line segment.
        id (Optional[int]): Optional ID for the new line segment. If not provided, defaults to None.

    Returns:
        LineSegment: A new line segment object with its neighbors based on intersections.
    """
    
    # Create a temporary line segment extending from the location in both directions
    s_temp = LineSegment(start=np.array(location) - 10 * np.array(direction), end=np.array(location) + 10 * np.array(direction))
    intersection_points: List[Dict[str, Tuple[float, float]]] = []

    # Check for intersections with existing line segments
    for segment in line_segments_to_check:
        intersect, (intersect_x, intersect_y) = doSegmentsIntersect(s_temp, segment)

        if intersect:
            segment_length = math.sqrt(
                (location[0] - intersect_x) ** 2
                + (location[1] - intersect_y) ** 2
            )
            intersection_points.append(
                {"id": segment.id, "point": (intersect_x, intersect_y), "segment_length": segment_length}
            )

    # Divide intersections into ones behind and in front of the new line
    intersections_b = [intersection for intersection in intersection_points if intersection["point"][0] < location[0]]
    intersections_f = [intersection for intersection in intersection_points if intersection["point"][0] > location[0]]

    if not intersections_b or not intersections_f:
        intersections_b = [intersection for intersection in intersection_points if intersection["point"][1] < location[1]]
        intersections_f = [intersection for intersection in intersection_points if intersection["point"][1] > location[1]]

    # Determine the closest intersections for segment start and end
    s_start = min(intersections_b, key=lambda x: x["segment_length"])
    s_end = min(intersections_f, key=lambda x: x["segment_length"])
    start, end = s_start['point'], s_end['point']
    start_id, end_id = s_start['id'], s_end['id']

    # Ensure the start comes before the end
    if start[0] > end[0]:
        start, end = end, start
        start_id, end_id = end_id, start_id

    # Create a new line segment and assign neighbors
    neighbors_initial = {start_id: start, end_id: end}
    segment_new = LineSegment(start=start, end=end, id=id, neighbors_initial=neighbors_initial, neighbors=neighbors_initial)
    
    return segment_new
    
def update_data(
    segments_dict: Dict[int, 'LineSegment'], 
    polygon_arr: Dict[str, Dict[str, object]], 
    polygon_id: str, 
    segment_thickness_dict: Dict[int, 'Polygon'], 
    vertices0: List[Tuple[float, float]], 
    vertices1: List[Tuple[float, float]], 
    vertices2: List[Tuple[float, float]], 
    cycle0: List[int], 
    cycle1: List[int], 
    cycle2: List[int], 
    neighbor1_1: int, 
    neighbor1_2: int, 
    neighbor2_1: int, 
    neighbor2_2: int, 
    vertex_begin_1: Tuple[float, float], 
    vertex_end_1: Tuple[float, float], 
    vertex_begin_2: Tuple[float, float], 
    vertex_end_2: Tuple[float, float], 
    id_1: int, 
    id_2: int
) -> Tuple[Dict[int, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]]:
    """
    Updates the segments, polygons, and segment thickness dictionaries by adding new data derived
    from provided vertices and neighbor information.

    Args:
        segments_dict (Dict[int, LineSegment]): A dictionary of segments with segment ID as the key.
        polygon_arr (Dict[str, Dict[str, object]]): A dictionary of polygons with polygon ID as the key.
        polygon_id (str): The ID of the polygon being updated.
        segment_thickness_dict (Dict[int, Polygon]): A dictionary mapping thickness information to polygon objects.
        vertices0 (List[Tuple[float, float]]): Vertices of the base polygon.
        vertices1 (List[Tuple[float, float]]): Vertices of the first new polygon.
        vertices2 (List[Tuple[float, float]]): Vertices of the second new polygon.
        cycle0 (List[int]): List of face indices for the base polygon.
        cycle1 (List[int]): List of face indices for the first new polygon.
        cycle2 (List[int]): List of face indices for the second new polygon.
        neighbor1_1 (int): ID of the first neighbor of the first segment.
        neighbor1_2 (int): ID of the second neighbor of the first segment.
        neighbor2_1 (int): ID of the first neighbor of the second segment.
        neighbor2_2 (int): ID of the second neighbor of the second segment.
        vertex_begin_1 (Tuple[float, float]): Starting vertex of the first segment.
        vertex_end_1 (Tuple[float, float]): Ending vertex of the first segment.
        vertex_begin_2 (Tuple[float, float]): Starting vertex of the second segment.
        vertex_end_2 (Tuple[float, float]): Ending vertex of the second segment.
        id_1 (int): ID of the first new segment.
        id_2 (int): ID of the second new segment.

    Returns:
        Tuple[Dict[int, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]]:
            - Updated dictionary of line segments.
            - Updated dictionary of polygons.
            - Updated dictionary of segment thickness.
    """
    
    # Update polygon_arr (a dictionary of polygons)
    polygon_new_1 = {
        f'p{len(polygon_arr) + 1}': {
            'vertices': vertices1, 
            'area': Polygon(vertices=vertices1).area(), 
            'faces': cycle1
        }
    }
    polygon_new_2 = {
        polygon_id: {
            'vertices': vertices2, 
            'area': Polygon(vertices=vertices2).area(), 
            'faces': cycle2
        }
    }
    polygon_arr.update(polygon_new_1)
    polygon_arr.update(polygon_new_2)
    
    # Update the segments_dict for the first segment
    neighbors_initial_1 = {
        neighbor1_1: vertex_begin_1,
        neighbor1_2: vertex_end_1
    }
    segment_new_1 = LineSegment(
        start=vertex_begin_1, 
        end=vertex_end_1, 
        id=id_1, 
        neighbors_initial=neighbors_initial_1, 
        neighbors=neighbors_initial_1
    )
    segments_dict[segment_new_1.id] = segment_new_1
    segments_dict[neighbor1_1].neighbors[id_1] = vertex_begin_1
    segments_dict[neighbor1_2].neighbors[id_1] = vertex_end_1
    
    # Update the segments_dict for the second segment
    neighbors_initial_2 = {
        neighbor2_1: vertex_begin_2,
        neighbor2_2: vertex_end_2
    }
    segment_new_2 = LineSegment(
        start=vertex_begin_2, 
        end=vertex_end_2, 
        id=id_2, 
        neighbors_initial=neighbors_initial_2, 
        neighbors=neighbors_initial_2
    )
    segments_dict[segment_new_2.id] = segment_new_2
    segments_dict[neighbor2_1].neighbors[id_2] = vertex_begin_2
    segments_dict[neighbor2_2].neighbors[id_2] = vertex_end_2
    
    # Update the segment_thickness_dict with the base polygon
    segment_thickness_dict[len(segment_thickness_dict) + 1] = Polygon(vertices=vertices0)
    
    return segments_dict, polygon_arr, segment_thickness_dict
    
def add_line_segment(
    segments_dict: Dict[int, LineSegment], 
    polygon_arr: Dict[str, Dict[str, object]], 
    segment_thickness_dict: Dict[int, Polygon], 
    thickness: float = 0, 
    angles: str = 'uniform'
) -> Union[Tuple[Dict[int, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]], bool]:
    """
    Adds a new line segment to the segments and polygon data structures, with a given thickness and angle distribution.

    Args:
        segments_dict (Dict[int, LineSegment]): A dictionary containing the current line segments.
        polygon_arr (Dict[str, Dict[str, object]]): A dictionary containing the current polygons and their properties.
        segment_thickness_dict (Dict[int, Polygon]): A dictionary storing the thickness information mapped to polygons.
        thickness (float): The thickness of the new segment to be added. Defaults to 0.
        angles (str): The angle distribution method. Defaults to 'uniform'.

    Returns:
        Union[Tuple[Dict[int, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]], bool]:
            - A tuple containing the updated segments dictionary, polygon dictionary, and thickness dictionary, 
              or False if no valid location for the new segment is found.
    """
    
    # Get a valid location and direction, or return False if none is found
    loc = get_location_and_direction(polygon_arr, thickness, max_attempts=1000, angles=angles)
    if loc:
        polygon_id, polygon, location_new, direction_new, perpendicular = loc
    else:
        print('No valid location found')
        return False
        
    # Get the borders of the new segment with the given thickness
    line_segments_to_check = [segments_dict[segment] for segment in polygon['faces']]
    middle_segment = get_new_segment(line_segments_to_check, location=location_new, direction=direction_new)
    s1 = get_new_segment(line_segments_to_check, location=np.array(location_new) + thickness * perpendicular / 2, direction=direction_new)
    s2 = get_new_segment(line_segments_to_check, location=np.array(location_new) - thickness * perpendicular / 2, direction=direction_new)
    
    # Extract neighbor information and segment vertices
    neighbor1_1, neighbor1_2 = list(s1.neighbors.keys())
    vertex_begin_1, vertex_end_1 = list(s1.neighbors.values())
    neighbor2_1, neighbor2_2 = list(s2.neighbors.keys())
    vertex_begin_2, vertex_end_2 = list(s2.neighbors.values())
    id_1 = str(int((len(segments_dict.keys()) - 2) / 2)) + '_1'
    id_2 = str(int((len(segments_dict.keys()) - 2) / 2)) + '_2'
    
    # Get the resulting polygons after splitting
    cycle0, vertices0, cycle1, vertices1, cycle2, vertices2 = get_polygons(
        polygon_id,
        polygon_arr, 
        neighbor1_1, 
        neighbor1_2, 
        vertex_begin_1, 
        vertex_end_1, 
        neighbor2_1, 
        neighbor2_2,
        vertex_begin_2=vertex_begin_2,
        vertex_end_2=vertex_end_2,
        segment_new_id_1=id_1, 
        segment_new_id_2=id_2
    )
    
    # Update all relevant data structures
    segments_dict, polygon_arr, segment_thickness_dict = update_data(
        segments_dict, 
        polygon_arr, 
        polygon_id, 
        segment_thickness_dict, 
        vertices0, 
        vertices1, 
        vertices2, 
        cycle0, 
        cycle1, 
        cycle2, 
        neighbor1_1, 
        neighbor1_2, 
        neighbor2_1, 
        neighbor2_2, 
        vertex_begin_1, 
        vertex_end_1, 
        vertex_begin_2, 
        vertex_end_2, 
        id_1, 
        id_2
    )
    
    # Associate the middle segment with the newly created thickness entry
    segment_thickness_dict[list(segment_thickness_dict.keys())[-1]].middle_segment = middle_segment
    
    return segments_dict, polygon_arr, segment_thickness_dict

def generate_line_segments_dynamic_thickness(
    size: int, 
    thickness_arr: List[float], 
    angles: str = 'uniform'
) -> Tuple[Dict[str, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]]:
    """
    Generates a specified number of line segments and updates the polygon and segment thickness dictionaries.

    Args:
        size (int): The number of line segments to generate.
        thickness_arr (List[float]): A list containing the thickness values for each segment to be generated.
        angles (str): The angle distribution method for generating segments. Defaults to 'uniform'.

    Returns:
        Tuple[Dict[str, LineSegment], Dict[str, Dict[str, object]], Dict[int, Polygon]]:
            - Updated dictionary of line segments.
            - Updated dictionary of polygons.
            - Updated dictionary of segment thicknesses.
    """
    
    # Initialize border segments for a square and its polygon representation
    borders = [
        LineSegment((1, 0), (0, 0), id='b1', neighbors_initial={'b2': (0, 0), 'b4': (1, 0)}, neighbors={'b2': (0, 0), 'b4': (1, 0)}),
        LineSegment((0, 1), (0, 0), id='b2', neighbors_initial={'b1': (0, 0), 'b3': (0, 1)}, neighbors={'b1': (0, 0), 'b3': (0, 1)}),
        LineSegment((0, 1), (1, 1), id='b3', neighbors_initial={'b2': (0, 1), 'b4': (1, 1)}, neighbors={'b2': (0, 1), 'b4': (1, 1)}),
        LineSegment((1, 1), (1, 0), id='b4', neighbors_initial={'b1': (1, 0), 'b3': (1, 1)}, neighbors={'b1': (1, 0), 'b3': (1, 1)})
    ]
    
    polygon_arr = {
        'p1': {
            'vertices': [(0, 0), (0, 1), (1, 1), (1, 0)], 
            'area': 1, 
            'faces': ['b1', 'b2', 'b3', 'b4']
        }
    }

    segments = borders
    segments_dict = {segment.id: segment for segment in segments}
    segment_thickness_dict = {}

    # Generate new line segments based on the given size and thickness array
    for i in range(size):
        output = add_line_segment(segments_dict, polygon_arr, segment_thickness_dict, thickness=thickness_arr[i], angles=angles)
        if output:
            segments_dict, polygon_arr, segment_thickness_dict = output
        else: 
            print(f"Stopped at iteration {i}, could not find a valid segment position.")
            break
        
        # Uncomment the following line if you want progress feedback
        percentage = np.round(i / size * 100, 3)
        print(f'generate_segments: {percentage}% done', end='\r')
    
    return segments_dict, polygon_arr, segment_thickness_dict