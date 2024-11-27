import rhinoscriptsyntax as rs
import random

def create_branch(start_point, direction, level, angle_range, length_range, max_levels, target_height):
    """
    Recursively creates branches.

    Args:
        start_point (tuple): Starting point of the branch.
        direction (tuple): Direction vector of the branch.
        level (int): Current level of branching.
        angle_range (tuple): Minimum and maximum angle for branching.
        length_range (tuple): Minimum and maximum length for branches.
        max_levels (int): Maximum depth of branching.
        target_height (float): Approximate height where the branches should end.

    Returns:
        tuple: A tuple containing a list of branch lines and a list of end points of the last level branches.
    """
    # Base case: Stop recursion if maximum depth is reached
    if level > max_levels:
        # Adjust endpoint height to match target height with slight variation
        adjusted_point = (start_point[0], start_point[1], target_height + random.uniform(-1.0, 1.0))
        return ([], [adjusted_point])

    branches = []  # Store the lines representing branches
    end_points = []  # Store the endpoints of the branches

    # Generate a random length for the current branch
    branch_length = random.uniform(*length_range)

    # Calculate the endpoint of the branch
    end_point = rs.PointAdd(start_point, rs.VectorScale(direction, branch_length))

    # Add the branch as a line in Rhino
    branches.append(rs.AddLine(start_point, end_point))

    # Determine the number of child branches (randomized for natural variation)
    num_branches = random.randint(2, 3)

    for _ in range(num_branches):
        # Create a random direction by perturbing the current direction
        angle = random.uniform(*angle_range)  # Random angle within the given range
        axis = (
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )  # Generate a random rotation axis
        axis = rs.VectorUnitize(axis)  # Normalize the axis

        # Rotate the direction vector by the random angle around the random axis
        rotated_direction = rs.VectorRotate(direction, angle, axis)

        # Combine the rotated direction with the current direction for natural growth
        rotation = rs.VectorAdd(rotated_direction, direction)
        rotation = rs.VectorUnitize(rotation)  # Normalize the resulting vector

        # Recursively create child branches
        child_branches, child_end_points = create_branch(
            end_point, rotation, level + 1, angle_range, length_range, max_levels, target_height
        )
        branches.extend(child_branches)  # Add the child branches to the main list
        end_points.extend(child_end_points)  # Collect the endpoints from child branches

    return (branches, end_points)

# Parameters
start_point = (0, 0, 0) 
initial_direction = (0, 0, 1) 
angle_range = (-45, 45) 
length_range = (2.0, 5.0) 
max_levels = 5 
target_height = 20.0 

# Generate the tree structure by initiating the recursive branching function
branches, last_level_end_points = create_branch(start_point, initial_direction, 1, angle_range, length_range, max_levels, target_height
)

# Output the results
a = branches
b = last_level_end_points 
