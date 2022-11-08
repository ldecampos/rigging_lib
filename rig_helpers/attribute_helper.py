from maya import cmds


def is_attr(node, attr):
    """
    Check if attr exists in the node

    Args:
        node (str): Name of the node to check
        attr (str): Name of the attribute to look for

    Returns:
        bool
    """

    # Check if attribute exists
    if not cmds.objExists('{}.{}'.format(node, attr)):
        return False

    return True


def set_attr(node, attr, value, **kwargs):
    """

    Set the value of a node attribute

    Args:
        node (str): Name of the node
        attr (str): Name of the attribute
        value: Value to set
        **kwargs:

    """

    # Checks
    if not is_attr(node=node, attr=attr):
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

    Returns
        value

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Get value
    value = cmds.getAttr('{}.{}'.format(node, attr), **kwargs)

    return value


def add_attr(node, attr, channel_box=False, **kwargs):
    """

    Add an attribute to a node

    Args:
        node (str): Name of the node to add the attribute
        attr (str): Name of the attribute to add
        channel_box (bool): Show attribute on channelBox. Default to False.
        **kwargs:

    """

    # Checks
    if cmds.objExists('{}.{}'.format(node, attr)):
        raise ValueError('attribute "{}" already exists in "{}" node'.format(attr, node))

    # Add Attribute
    cmds.addAttr(node, longName=attr, shortName=attr, **kwargs)
    if channel_box:
        cmds.setAttr('{}.{}'.format(node, attr), channelBox=True)


def delete_attr(node, attr, **kwargs):
    """

    Remove an attribute from a node

    Args:
        node (str): Name of the node to remove the attribute
        attr (str): Name of the attribute to remove
        *kwargs:

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # unlock the attribute to be able to delete it
    un_lock_attr(node=node, attr=attr)

    # Delete attribute
    cmds.deleteAttr(node, attribute=attr, **kwargs)


def lock_attr(node, attr):
    """

    Lock attributes

    Args:
        node (str): Name of the node to lock
        attr (str): Name of the attribute to lock

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Lock Attr
    cmds.setAttr('{}.{}'.format(node, attr), lock=True)


def un_lock_attr(node, attr):
    """

    Unlock attribute

    Args:
        node (str): Name of the node to lock
        attr (str): Name of the attribute to lock

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Unlock Attr
    cmds.setAttr('{}.{}'.format(node, attr), lock=False)


def toogle_lock_attr(node, attr):
    """

    Switch lock / unlock attribute

    Args:
        node (str): Name of the node
        attr (str): Name of the node to switch lock value

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Get lock value
    lock = cmds.getAttr('{}.{}'.format(node, attr), lock=True)

    # Switch values
    lock_status = False if lock else True

    # Set value
    cmds.setAttr('{}.{}'.format(node, attr), lock=lock_status)


def hide_attr(node, attr):
    """

    Hide attribute from channel Box

    Args:
        node (str): Name of the node to hide
        attr (str): Name of the attribute to hide

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Hide attribute
    cmds.setAttr('{}.{}'.format(node, attr), keyable=False)


def un_hide_attr(node, attr):
    """

    Un hide attribute from channel Box

    Args:
        node (str): Name of the node to un hide
        attr: (str): Name of the attribute to hide

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Hide attribute
    cmds.setAttr('{}.{}'.format(node, attr), keyable=True)


def lock_and_hide_attr(node, attr):
    """

    Lock and hide attribute from channel box

    Args:
        node (str): Name of the node to lock and hide
        attr (str): Name of the attribute to lock and hide

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    # Lock and hide attribute
    cmds.setAttr('{}.{}'.format(node, attr), lock=True, keyable=False)


def create_spacer(node, spacer):
    """

    Add a spacer attribute and showed in channelBox

    Args:
        node (str): Name of the node
        spacer (str): Name of the spacer

    """

    # Checks
    if cmds.objExists('{}.{}'.format(node, spacer)):
        raise ValueError('spacer "{}" already exists in "{}" node'.format(spacer, node))

    # Create spacer
    cmds.addAttr(node, longName=spacer, niceName=' ', attributeType='enum', enumName=spacer, keyable=False)

    # Lock and show spacer
    cmds.setAttr('{}.{}'.format(node, spacer), lock=True, channelBox=True)


def delete_connection(node, attr):
    """

    Delete connection between two nodes

    Args:
        node (str): Name of the node
        attr (str): Name of the input or output connection attribute

    """

    # Checks
    if not is_attr(node=node, attr=attr):
        raise ValueError('attribute "{}" does not exists in "{}" node'.format(attr, node))

    if cmds.connectionInfo('{}.{}'.format(node, attr), isDestination=True):
        plug = cmds.connectionInfo('{}.{}'.format(node, attr), getExactDestination=True)
        read_only = cmds.ls(plug, readOnly=True)
        # Delete input connections if destination attr is read only
        if read_only:
            source = cmds.connectionInfo(plug, sourceFromDestination=True)
            cmds.disconnectAttr(source, plug)
        else:
            cmds.delete(plug, inputConnectionsAndNodes=True)


def toogle_reference_display(node):
    """

    Lock or unlock reference display node

    Args:
        node (str): Name of the node to switch reference display

    """

    # Checks
    if not cmds.objExists(node):
        raise ValueError('node "{}" does not exists in the scene'.format(node))

    override_enabled = cmds.getAttr('{}.overrideEnabled'.format(node))

    # normal as 0 or reference as 2
    override_type = 0 if override_enabled else 2
    cmds.setAttr('{}.overrideEnabled'.format(node), not override_enabled)
    cmds.setAttr('{}.overrideDisplayType'.format(node), override_type)


def connect_trs(source, target, force=True):
    """

    Connect translation, rotation and scale from source to target

    Args:
        source (str): Name of the source node
        target (str): Name of the target node
        force (bool): Force connections. Defaults to True

    """

    for attr in ('translate', 'rotate', 'scale'):
        for axis in ('X', 'Y', 'Z'):
            cmds.connectAttr('{}.{}{}'.format(source, attr, axis), '{}.{}{}'.format(target, attr, axis), force=force)


def connect_translate(source, target, force=True):
    """

    Connect translation from source to target

    Args:
        source (str): Name of the source node
        target (str): Name of the target node
        force (bool): Force connections. Defaults to True

    """

    for axis in ('X', 'Y', 'Z'):
        cmds.connectAttr('{}.translate{}'.format(source, axis), '{}.translate{}'.format(target, axis), force=force)


def connect_rotate(source, target, force=True):
    """

    Connect rotation from source to target

    Args:
        source (str): Name of the source node
        target (str): Name of the target node
        force (bool): Force connections. Defaults to True

    """

    for axis in ('X', 'Y', 'Z'):
        cmds.connectAttr('{}.rotate{}'.format(source, axis), '{}.rotate{}'.format(target, axis), force=force)


def connect_scale(source, target, force=True):
    """

    Connect scale from source to target

    Args:
        source (str): Name of the source node
        target (str): Name of the target node
        force (bool): Force connections. Defaults to True

    """

    for axis in ('X', 'Y', 'Z'):
        cmds.connectAttr('{}.scale{}'.format(source, axis), '{}.scale{}'.format(target, axis), force=force)


def reset_default_values(node):
    """

    Reset attribute values of the node to default values

    Args:
        node (str): Name of the node to reset values

    """

    # Checks
    if not cmds.objExists(node):
        raise ValueError('node "{}" does not exists in the scene'.format(node))

    # Reset transformations
    for attr in ('translate', 'rotate', 'scale'):
        for axis in ('X', 'Y', 'Z'):
            if cmds.getAttr('{}.{}{}'.format(node, attr, axis), settable=True):
                if attr == 'scale':
                    cmds.setAttr('{}.{}{}'.format(node, attr, axis), 1)
                else:
                    cmds.setAttr('{}.{}{}'.format(node, attr, axis), 0)

    # Reset user define attributes
    user_define_attrs = cmds.listAttr(node, userDefined=True, settable=True)
    if user_define_attrs:
        for attr in user_define_attrs:
            if cmds.getAttr('{}.{}'.format(node, attr), type=True) != 'message':
                if cmds.getAttr('{}.{}'.format(node, attr), type=True) != 'string':
                    default_value = cmds.addAttr('{}.{}'.format(node, attr), query=True, defaultValue=True)
                    if default_value:
                        cmds.setAttr('{}.{}'.format(node, attr), default_value)


def get_attributes(source, attrs=False):
    """

    Get values from attributes and store in a dictionary

    Notes:
        In case of not giving any input attribute, keyable attributes will be used by default.

    Args:
        source (str): Name of the node
        attrs (list): Optional. Name of the attributes to store.

    Returns:
        (dict): {'attr1': value, 'attr2':value, ...}

    """

    # Checks
    if not cmds.objExists(source):
        raise ValueError('node "{}" does not exists in the scene'. format(source))

    if not attrs:
        attrs = cmds.listAttr(source, keyable=True, visible=True)

    attrs_values = {}

    # Store attribute values in a dictionary
    for attr in attrs:
        if cmds.objExists('{}.{}'.format(source, attr)):
            value = cmds.getAttr('{}.{}'.format(source, attr))
            attrs_values[attr] = value

    return attrs_values
