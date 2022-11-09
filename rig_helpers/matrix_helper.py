from maya import cmds
from maya.api import OpenMaya


IDENTITY_MATRIX = [1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0]


def check_node_exists(node):
    """

    Check if the node exists inside the current scene

    Args:
        node (str) : Name of the node to check

    Raises:
        ValueError: when the node does not exit

    """

    if not cmds.objExists(node):
        raise ValueError('node "{}" does not exist in  the scene'.format(node))


def get_position(node, **kwargs):
    """

    Get world space position of a node

    Args:
        node (str): Name of the node
        **kwargs:

    Returns:
        (list) Position [0.0, 0.0, 0,0]

    """

    # Checks
    check_node_exists(node)

    position = cmds.xform(node, query=True, translation=True, worldSpace=True, **kwargs)

    return position


def get_rotation(node, **kwargs):
    """

    Get world space rotation of a node

    Args:
        node (str): Name of the node
        **kwargs:

    Returns:
        (list) Rotation [0.0, 0.0, 0,0]

    """

    # Checks
    check_node_exists(node)

    rotation = cmds.xform(node, query=True, rotation=True, worldSpace=True, **kwargs)

    return rotation


def get_scale(node, **kwargs):
    """

    Get world space scale of a node

    Args:
        node (str): Name of the node
        **kwargs:

    Returns:
        (list) Scale [1.0, 1.0, 1.0]

    """

    # Checks
    check_node_exists(node)

    scale = cmds.xform(node, query=True, scale=True, worldSpace=True, **kwargs)

    return scale


def get_matrix(node, **kwargs):
    """

    Get world space matrix of a node

    Note:
        Matrix is represented by 16 double arguments

    Args:
        node (str): Name of the node
        **kwargs:

    Returns:
        (list): Matrix [1.0, 0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 1.0]
    """

    # Checks
    check_node_exists(node)

    matrix = cmds.xform(node, query=True, matrix=True, worldSpace=True, **kwargs)

    return matrix


def set_position(node, position, **kwargs):
    """

    Set world space position of a node

    Args:
        node (str): Name of the node
        position (list): Axis X, Y, Z position of a point
        **kwargs:

    """

    # Checks
    check_node_exists(node)

    cmds.xform(node, translation=position, absolute=True, worldSpace=True, **kwargs)


def set_rotation(node, rotation, **kwargs):
    """

    Set world space rotation of a node

    Args:
        node (str): Name of the node
        rotation (list): Axis X, Y, Z rotation of a point
        **kwargs:

    """

    # Checks
    check_node_exists(node)

    cmds.xform(node, rotation=rotation, absolute=True, worldSpace=True, **kwargs)


def set_scale(node, scale, **kwargs):
    """

    Set world space scale of a node

    Args:
        node: str. Name of the node
        scale: list. X, Y, Z scale of a point
        **kwargs:

    """

    # Checks
    check_node_exists(node)

    cmds.xform(node, scale=scale, absolute=True, worldSpace=True, **kwargs)


def set_matrix(node, matrix, **kwargs):
    """

    Set world space matrix of a node

    Args:
        node (str): Name of the node
        matrix (list): Matrix is represented by 16 double arguments
        **kwargs:

    """

    # Checks
    check_node_exists(node)

    cmds.xform(node, matrix=matrix, absolute=True, worldSpace=True, **kwargs)


def put_in_place(source, target, pos=True, rot=True, scl=False):
    """

    Sets translation, rotation and scale from source to target in world space

    Args:
        source (str): Name of the source node
        target (str): Name of the target node
        pos (bool): Optional. Set position from source to target in world space. Defaults to True
        rot (bool): Optional. Set rotation from source to target in world space. Defaults to True
        scl (bool): Optional. Set scale from source to target in world space. Defaults to False

    """

    # Checks
    check_node_exists(source)
    check_node_exists(target)

    if pos:
        target_pos = get_position(node=source)
        set_position(node=target, position=target_pos)

    if rot:
        target_rot = get_rotation(node=source)
        set_rotation(node=target, rotation=target_rot)

    if scl:
        target_scl = get_scale(node=source)
        set_scale(node=target, scale=target_scl)


def bake_transform_to_offset_parent_matrix(node):
    """
        Bake values from main matrix to the offset parent Matrix

    Args:
        node (str): Name of the node to bake the matrix

    """

    # Checks maya version
    if not int(cmds.about(version=True).split('.')[0]) >= 2020:
        raise Exception('You need a version of maya 2020 or higher')

    # Checks
    check_node_exists(node)

    # openMAya is used because matrix multiplication is easier and faster
    local_matrix = OpenMaya.MMatrix(cmds.xform(node, query=True, matrix=True, worldSpace=False))
    offset_parent_matrix = OpenMaya.MMatrix(cmds.getAttr('{}.offsetParentMatrix'.format(node)))

    baked_matrix = local_matrix * offset_parent_matrix

    # Reset main matrix
    cmds.xform(node, matrix=IDENTITY_MATRIX, worldSpace=False, absolute=True)

    # Bake matrix values
    cmds.setAttr('{}.offsetParentMatrix'.format(node), baked_matrix, type="matrix")
