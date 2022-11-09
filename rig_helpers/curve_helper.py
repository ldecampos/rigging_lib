from maya import cmds


def node_exists(node):
    """

    Check if the node exists inside the current scene

    Args:
        node (str) : Name of the node to check

    Raises:
        ValueError: when the node does not exit

    """

    if not cmds.objExists(node):
        raise ValueError('node "{}" does not exist in the scene'.format(node))


def is_nurbs_curve(crv):
    """
    Check if input object is a valid nurbsCurve

    Args:
        crv (str): Name of the nurbs curve

    Returns:
        bool
    """

    # Checks
    node_exists(crv)

    # Check object type
    if cmds.objectType(crv) != 'nurbsCurve':
        return False

    return True


def get_cvs_number(node):
    """

    Get the number of CVs from a curve

    Notes:
        Works with both transform and nurbs curve shape

    Args:
        node (str): Name of the curve to get the CVs

    Returns:
        (int) CVs

    """

    # Checks
    node_exists(node)

    # Get the nurbs curve
    crv = node
    if not is_nurbs_curve(crv=crv):
        crv = cmds.listRelatives(node, shapes=True)[0]
        if not is_nurbs_curve(crv=crv):
            raise ValueError('node "{}" is not a nurbsCurve'.format(node))

    return cmds.getAttr('{}.cp'.format(crv), size=True)


def get_curve_length(node):
    """

    Get the length parameter of a curve

    Notes:
        Works with both transform and nurbs curve shape

    Args:
        node (str): Name of the curve to get length

    Returns:
        (float): length

    """

    # Checks
    node_exists(node)

    # Get the nurbs curve
    crv = node
    if not is_nurbs_curve(crv=crv):
        crv = cmds.listRelatives(node, shapes=True)[0]
        if not is_nurbs_curve(crv=crv):
            raise ValueError('node "{}" is not a nurbsCurve'.format(node))

    return cmds.arclen(crv)


def create_curve_from_points(points, name, world_space=True, **kwargs):
    """

    Create a curve from points and rename the shapes to be unique

    Note:
        The points of the curve will be taken as world space by default

    Args:
        points (list): Axis X, Y, Z position of a point
        name (str): Optional. Name for the new curve
        world_space (bool): Curve is created as worldSpace. Defaults to True
        **kwargs:

    Returns:
        (str, str) Curve transform and Shape

    """

    # Create curve
    crv = cmds.curve(point=points, name=name, worldSpace=world_space, **kwargs)

    # Get shape
    shape = cmds.listRelatives(crv, shapes=True, fullPath=True)[0]

    # Rename shape
    shape = cmds.rename(shape, '{}Shape'.format(crv))

    return crv, shape


def convert_to_bezier(node):
    """

    Convert a curve to a Bezier curve

    Args:
        node (str): Name of the curve

    Returns:
        curve
    """

    # Checks
    node_exists(node)

    # Get shape
    shape = cmds.listRelatives(node, shapes=True)[0]

    # Convert to bezier curve
    if cmds.nodeType(shape) == 'bezierCurve':
        return

    if cmds.nodeType(shape) == 'nurbsCurve':
        cmds.select(shape)
        cmds.nurbsCurveToBezier()


def get_nearest_point_on_curve(node, source, world_space=True):
    """

    Find the nearest point on a curve.

    Note:
        Node works with both transform and nurbs curve shape

    Args:
        node (str): Name of the curve
        source (str): Object from where to find the closest position
        world_space (bool): Source position will be taken as worldSpace. Defaults to True

    Returns:
        (dict) {'position': (0.0, 0.0, 0.0), 'parameter': 0.0}

    """

    # Checks
    node_exists(node)
    node_exists(source)

    # Get the nurbs curve
    crv = node
    if not is_nurbs_curve(crv=crv):
        crv = cmds.listRelatives(node, shapes=True)[0]
        if not is_nurbs_curve(crv=crv):
            raise ValueError('node "{}" is not a nurbsCurve'.format(node))

    source_pos = cmds.xform(source, query=True, translation=True, worldSpace=world_space)

    # Create the nearestPoint
    temp_npc = cmds.createNode('nearestPointOnCurve')

    # Get the values
    cmds.connectAttr('{}.worldSpace'.format(crv), '{}.inputCurve'.format(temp_npc))
    cmds.setAttr('{}.inPosition'.format(temp_npc), source_pos[0], source_pos[1], source_pos[2], type='double3')
    position = cmds.getAttr('{}.position'.format(temp_npc))[0]
    param = cmds.getAttr('{}.parameter'.format(temp_npc))

    cmds.delete(temp_npc)

    return {'position': position, 'parameter': param}


def create_animation_curve(name, values=None, in_tangent_type='linear', out_tangent_type='linear'):
    """

    Create animation curve and set values if there is any.

    Args:
        name (str): Name for the new curve
        values (dict): Values for the new animation curve {'time': 'value'}, ex {2:4}
        in_tangent_type: str. Fixed, Linear, Flat, Step,Slow, Fast, Spline, Clamped, Plateau, StepNext.
                         Defaults to linear.
        out_tangent_type: str. Fixed, Linear, Flat, Step,Slow, Fast, Spline, Clamped, Plateau, StepNext.
                         Defaults to linear.

    Returns:
        (str) animation curve

    """

    if values is None:
        values = {}

    # Check if animation curve already exists
    if cmds.objExists(name):
        raise Exception('node "{}" already exists'.format(name))

    anim_curve = cmds.createNode('animCurveUL', name=name)

    # Set values for animation curve
    if values and isinstance(values, dict):
        for key, value in values.items():
            cmds.setKeyframe(anim_curve,
                             float=key,
                             value=value,
                             inTangentType=in_tangent_type,
                             outTangentType=out_tangent_type)

    return anim_curve
