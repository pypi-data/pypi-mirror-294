import numpy as np
import random
from typing import List, Dict, Tuple, Union, Optional

from .Classes import Line, LineSegment
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
    segment1: 'LineSegment', 
    segment2: 'LineSegment'
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