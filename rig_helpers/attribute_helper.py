from maya import cmds


def add_attr(node, attr, channel_box=False, **kwargs):
    """

    Add an attribute to a node

    Args:
        node (str): Name of the node to add and attribute
        attr (str): Name of the attribute to add
        channel_box (bool): Show attribute on channelBox. Default to False.
        **kwargs:

    """

    if cmds.objExists('{}.{}'.format(node, attr)):
        raise ValueError('attribute "{}" already exists in "{}" node'.format(attr, node))

    # Add Attribute
    cmds.addAttr(node, longName=attr, shortName=attr, **kwargs)
    if channel_box:
        cmds.setAttr('{}.{}'.format(node, attr), channelBox=True)


def set_attr(node, attr, value, **kwargs):
    """

    Set the value of a node attribute

    Args:
        node (str): Name of the node
        attr (str): Name of the attribute
        value: Value to set
        **kwargs:

    """

    if not cmds.objExists('{}.{}'.format(node, attr)):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Set value
    cmds.setAttr('{}.{}'.format(node, attr), value, **kwargs)


def get_attr(node, attr, **kwargs):
    """

    Get the value of a node attribute

    Args:
        node (str): Name of the node
        attr (str): Name of the attribute
        **kwargs:

    """

    if cmds.objExists('{}.{}'.format(node, attr)):
        return

    # Get value
    value = cmds.getAttr('{}.{}'.format(node, attr), **kwargs)

    return value
