from maya import cmds


class AttributeHelper(object):
    def __init__(self, obj):
        """
        Args:
            obj: (str): Maya object name
        """

        self.obj = obj

    # ---------- Checks Methods ----------
    def attribute_exists(self, attribute_name):
        """
        Check if attributes exists in the object

        Args:
            attribute_name (str): Attribute name

        Returns:
            bool
        """

        # Check if attributes exists
        if cmds.attributeQuery(attribute_name, node=self.obj, exists=True):
            return True

        return False

    def is_attribute_locked(self, attribute_name):
        """
        Returns True if the attributes us locked.

        Args:
            attribute_name (str): Attribute name

        Returns:
            bool
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        return bool(cmds.getAttr('{}.{}'.format(self.obj, attribute_name), lock=True))

    def is_attribute_connected(self, attribute_name):
        """
        Returns True if the attributes has an incoming connection

        Args:
            attribute_name (str): Attribute name

        Returns:
            bool
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        if self.is_attribute_locked(attribute_name=attribute_name):
            return False

        return bool(cmds.listConnections('{}.{}'.format(self.obj, attribute_name), destination=False))

    def is_attribute_animated(self, attribute_name):
        """
        Returns True if the attributes has an incoming connection from an animated curve.

        Args:
            attribute_name (str): Attribute name

        Returns:
            bool
        """

        if not self.is_attribute_connected(attribute_name=attribute_name):
            return False

        connected_node = cmds.listConnections('{}.{}'.format(self.obj, attribute_name), destination=False)[0]

        if not cmds.nodeType(connected_node).startswith('animCurve'):
            return False

        return True

    def is_attribute_settable(self, attribute_name):
        """
        Returns True is the attributes can be set

        Args:
            attribute_name (str): Attribute name

        Returns:
            bool
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        return cmds.getAttr('{}.{}'.format(self.obj, attribute_name), settable=True)

    def is_attribute_in_channel_box(self, attribute_name):
        """
        Returns True if the attributes is visible in the channel box

        Args:
            attribute_name (str): Attribute name

        Returns:
            True if the attributes is visible in the channel box
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        if cmds.attributeQuery(attribute_name, node=self.obj, hidden=True):
            return False

        if cmds.attributeQuery(attribute_name, node=self.obj, attributeType=True) == 'typed':
            return False

        l = set(cmds.listAttr(self.obj, channelBox=False)).intersection(cmds.listAttr(self.obj, keyable=True))
        if attribute_name not in l:
            return False

        return True

    # ---------- Set Methods ----------
    def set_attribute_value(self, attribute_name, value, **kwargs):
        """
        Set attributes values

        Args:
            attribute_name (str): Attribute name
            value: Value to set
            **kwargs:
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), value, **kwargs)

    def set_attribute_default_value(self, attribute_name, default_value):
        """
        Set value to default value

        Args:
            attribute_name (str): Attribute name
            default_value: Value to set
        """

        if not self.is_attribute_settable(attribute_name=attribute_name):
            return False

        cmds.addAttr('{}.{}'.format(self.obj, attribute_name), edit=True, defaultValue=default_value)
        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), default_value)

    def set_attributes_default_values(self, attribute_list=None):
        """
        Set attributes list to default value

        Args:
            attribute_list (list): Attributes names. Defaults to keyable attributes
        """

        if not attribute_list:
            attribute_list = self.get_keyable_attributes()

        for attr in attribute_list:
            if self.is_attribute_settable(attribute_name=attr):
                cmds.setAttr('{}.{}'.format(self.obj, attr), self.get_default_value_attribute(attribute_name=attr))

    def set_user_define_attributes_default_values(self):
        """
        Set user define attributes to default value
        """

        if not self.get_user_define_attributes():
            return

        for attr in self.get_user_define_attributes():
            if cmds.getAttr('{}.{}'.format(self.obj, attr), type=True) == 'message':
                continue
            if cmds.getAttr('{}.{}'.format(self.obj, attr), type=True) == 'string':
                continue
            if self.is_attribute_settable(attribute_name=attr):
                cmds.setAttr('{}.{}'.format(self.obj, attr),
                             self.get_default_value_attribute(attribute_name=attr))

    def set_attribute_keyable(self, attribute_name, keyable=True):
        """
        Set attributes property between keyable and not keyable

        Args:
            attribute_name (str): Attribute name
            keyable (bool): Defaults to True
        """

        if self.attribute_exists(attribute_name=attribute_name):
            return False

        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), keyable=keyable, channelBox=not keyable)

    def set_attributes_keyable(self, attribute_list, keyable=True):
        """
        Set attributes list property between keyable and not keyable

        Args:
            attribute_list (list): Attribute names to set keyable.
            keyable (bool): Defaults to True
        """

        for attr in attribute_list:
            self.set_attribute_keyable(attribute_name=attr, keyable=keyable)

    def lock_attribute(self, attribute_name, lock=True):
        """
        Lock an attributes

        Args:
            attribute_name (str): Attribute name to lock.
            lock (bool): Defaults to True
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return False

        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), lock=lock)

    def lock_attributes(self, attributes_list, lock=True):
        """
        Lock attributes list

        Args:
            attributes_list (list): Attributes names to lock.
            lock (bool): Defaults to True
        """

        for attr in attributes_list:
            self.lock_attribute(attribute_name=attr, lock=lock)

    def hide_attribute(self, attribute_name, hide=True):
        """
        Hide attributes from channel Box

        Args:
            attribute_name (str): Attribute name to hide.
            hide (bool): Defaults to True
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return

        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), keyable=not hide, channelBox=not hide)

    def hide_attributes(self, attributes_list, hide=True):
        """
        Hide attributes list

        Args:
            attributes_list (list): Attributes names to hide.
            hide (bool): Defaults to True
        """

        for attr in attributes_list:
            self.hide_attribute(attribute_name=attr, hide=hide)

    def lock_and_hide_attribute(self, attribute_name, lock=True, hide=True):
        """
        Lock and hide an attributes

        Args:
            attribute_name (str): Attribute name to lock and hide
            lock (bool): Defaults to True
            hide (bool): Defaults to True
        """

        self.lock_attribute(attribute_name=attribute_name, lock=lock)
        self.hide_attribute(attribute_name=attribute_name, hide=hide)

    def lock_and_hide_attributes(self, attributes_list, lock=True, hide=True):
        """
        Lock and hide attributes list

        Args:
            attributes_list (list): Attribute names to lock and hide
            lock (bool): Defaults to True
            hide (bool): Defaults to True
        """

        for attr in attributes_list:
            self.lock_and_hide_attribute(attribute_name=attr, lock=lock, hide=hide)

    def set_reference_display(self, enabled=True):
        """
        Set reference display object

        Args:
            enabled (bool): Defaults to True
        """

        # normal as 0 or reference as 2
        override_type = 2 if enabled else 0

        cmds.setAttr('{}.overrideEnabled'.format(self.obj), enabled)
        cmds.setAttr('{}.overrideDisplayType'.format(self.obj), override_type)

    # ---------- Get Methods ----------
    def get_user_define_attributes(self):
        """
        Get user define values from object

        Returns:
            list. user_define_attributes or []
        """

        return cmds.listAttr(self.obj, userDefined=True, settable=True)

    def get_keyable_attributes(self):
        """
        Get keyable attributes from object

        Returns:
            list. keyable_attributes or []
        """

        return cmds.listAttr(self.obj, keyable=True)

    def get_default_value_attribute(self, attribute_name):
        """
        Get default value from an Attribute

        Args:
            attribute_name (str): Attribute name

        Returns:
            value
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return

        if cmds.getAttr('{}.{}'.format(self.obj, attribute_name), type=True) == 'message':
            raise ValueError('message type attributes does not have default values')

        if cmds.getAttr('{}.{}'.format(self.obj, attribute_name), type=True) == 'string':
            raise ValueError('string type attributes does not have default values')

        return cmds.attributeQuery(attribute_name, node=self.obj, listDefault=True)[0]

    def get_attribute_value(self, attribute_name, **kwargs):
        """
        Get attributes value from the object

        Args:
            attribute_name (str): Attribute name
            **kwargs:

        Returns:
            value
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return

        return cmds.getAttr('{}.{}'.format(self.obj, attribute_name), **kwargs)

    def get_attributes_values(self, attributes_list):
        """
        Get values from attributes and store in a dictionary

        Args:
            attributes_list (list). Attributes names

        Returns:
            dict. {'attr1': value, 'attr2':value, ...}

        """

        attributes_values = {}

        # Store attributes values in a dictionary
        for attr in attributes_list:
            attributes_values[attr] = self.get_attribute_value(attribute_name=attr)

        return attributes_values

    def get_attribute_type(self, attribute_name):
        """
        Get attributes data type

        Args:
            attribute_name (str): Attribute name

        Returns:
            type.
        """

        if not self.attribute_exists(attribute_name=attribute_name):
            return

        return cmds.getAttr('{}.{}'.format(self.obj, attribute_name), type=True)

    def get_attributes_type(self, attributes_list):
        """
        Get data type attributes and store in a dictionary

        Args:
            attributes_list:

        Returns:
            dict: {'attr1': float, 'attr2':matrix, ...}
        """

        attributes_types = {}

        # Store attributes values in a dictionary
        for attr in attributes_list:
            attributes_types[attr] = self.get_attribute_type(attribute_name=attr)

        return attributes_types

    # ---------- Add Methods ----------
    def add_attribute(self, attribute_name, **kwargs):
        """
        Add an attributes to the object

        Args:
            attribute_name (str): Attribute name
            **kwargs:

        Returns:
            str. attribute_name
        """

        if self.attribute_exists(attribute_name=attribute_name):
            raise RuntimeError('Attribute: "{}" already exists in object: "{}"'.format(attribute_name, self.obj))

        cmds.addAttr(self.obj, longName=attribute_name, **kwargs)

        return attribute_name

    def add_separator_attribute(self, separator_name):
        """
        Add a separator attributes and showed in channelBox

        Args:
            separator_name (str): Attribute name

        Returns:
            str. separator_name
        """

        self.add_attribute(attribute_name=separator_name,
                           channelBox=True,
                           niceName=' ',
                           attributeType='enum',
                           enumName=separator_name)
        self.set_attribute_keyable(attribute_name=separator_name, keyable=False)
        self.lock_attribute(attribute_name=separator_name)

        return separator_name

    def add_float_attribute(self, attribute_name, **kwargs):
        """
        Add a float attributes

        Args:
            attribute_name (str): Attribute name
            **kwargs: minValue, maxValue, defaultValue, etc

        Returns:
            str. attribute_name
        """

        return self.add_attribute(attribute_name=attribute_name, attributeType='float', **kwargs)

    def add_int_attribute(self, attribute_name, **kwargs):
        """
        Add an integer attributes

        Args:
            attribute_name (str): Attribute name
            **kwargs: minValue, maxValue, defaultValue, etc

        Returns:
            str. attribute_name
        """
        return self.add_attribute(attribute_name=attribute_name, attributeType='long', **kwargs)

    def add_bool_attribute(self, attribute_name, **kwargs):
        """
        Add a bool attributes

        Args:
            attribute_name (str): Attribute name
            **kwargs: minValue, maxValue, defaultValue, etc

        Returns:
            str. attribute_name
        """
        return self.add_attribute(attribute_name=attribute_name, attributeType='bool', **kwargs)

    def add_enum_attribute(self, attribute_name, states, keyable=True, **kwargs):
        """
        Add enum attributes

        Args:
            attribute_name (str): Attribute name
            states (str): separate he values with ':'
            keyable (bool): Defaults to True
            **kwargs: minValue, maxValue, defaultValue, etc

        Returns:
            str. attribute_name
        """

        return self.add_attribute(attribute_name, attributeType='enum', enumName=states, keyable=keyable, **kwargs)

    def add_matrix_attribute(self, attribute_name, **kwargs):
        """
        Add a matrix attributes

        Args:
            attribute_name (str): Attribute name
            **kwargs: minValue, maxValue, defaultValue, etc

        Returns:
            str. attribute_name
        """

        return self.add_attribute(attribute_name, attributeType='matrix', **kwargs)

    def add_string_attribute(self, attribute_name, text):
        """
        Add a string attributes

        Args:
            attribute_name (str): Attribute name
            text (str): Text to set in the string value

        Returns:
            str. attribute_name
        """

        self.add_attribute(attribute_name, dataType='string')
        cmds.setAttr('{}.{}'.format(self.obj, attribute_name), text, type='string')

        return attribute_name

    def add_proxy_attribute(self, attribute_name, proxy):
        """
        Add a proxy attributes

        Args:
            attribute_name (str): Attribute name
            proxy (str): Node with the attributes

        Returns:
            str. attribute_name
        """

        cmds.addAttr(self.obj, longName=attribute_name, proxy=proxy)

        return attribute_name

    def delete_attribute(self, attribute_name, **kwargs):
        """
        Remove an attributes from object

        Args:
            attribute_name (str): Attribute name to remove
            **kwargs:

        """

        if not self.attribute_exists(attribute_name=attribute_name):
            raise RuntimeError('Attribute: "{}" no exists in object: "{}"'.format(attribute_name, self.obj))

        self.lock_attribute(attribute_name=attribute_name, lock=False)

        cmds.deleteAttr(self.obj, attribute=attribute_name, **kwargs)


# ---------- Connection Attributes Methods ----------

def connect_trs(source, target, force=True):
    """
    Connect translation, rotation and scale from source to target

    Args:
        source (str): Source name
        target (str): Target name
        force (bool): Force connections. Defaults to True
    """

    for attr in ('translate', 'rotate', 'scale'):
        for axis in ('X', 'Y', 'Z'):
            source_ah = AttributeHelper(source)
            target_ah = AttributeHelper(target)
            if not source_ah.is_attribute_locked(
                    attribute_name='{}{}'.format(attr, axis)) and not target_ah.is_attribute_locked(
                attribute_name='{}{}'.format(attr, axis)):
                cmds.connectAttr('{}.{}{}'.format(source, attr, axis), '{}.{}{}'.format(target, attr, axis),
                                 force=force)


def connect_translate(source, target, force=True):
    """
    Connect translation from source to target

    Args:
        source (str): Source name
        target (str): target name
        force (bool): Force connections. Defaults to True
    """

    target_ah = AttributeHelper(target)
    for axis in ('X', 'Y', 'Z'):
        if not target_ah.is_attribute_locked(attribute_name='translate{}'.format(axis)):
            cmds.connectAttr('{}.translate{}'.format(source, axis),
                             '{}.translate{}'.format(target, axis),
                             force=force)


def connect_rotate(source, target, force=True):
    """
    Connect rotation from source to target

    Args:
        source (str): Source name
        target (str): Target name
        force (bool): Force connections. Defaults to True
    """

    target_ah = AttributeHelper(target)
    for axis in ('X', 'Y', 'Z'):
        if not target_ah.is_attribute_locked(attribute_name='rotate{}'.format(axis)):
            cmds.connectAttr('{}.rotate{}'.format(source, axis),
                             '{}.rotate{}'.format(target, axis),
                             force=force)


def connect_scale(source, target, force=True):
    """
    Connect scale from source to target

    Args:
        source (str): Source name
        target (str): Target name
        force (bool): Force connections. Defaults to True
    """

    target_ah = AttributeHelper(target)
    for axis in ('X', 'Y', 'Z'):
        if not target_ah.is_attribute_locked(attribute_name='scale{}'.format(axis)):
            cmds.connectAttr('{}.scale{}'.format(source, axis),
                             '{}.scale{}'.format(target, axis),
                             force=force)


def delete_connection(node, attribute_name):
    """
    Delete connection between two nodes

    Args:
        node (str): Node name
        attribute_name (str): Name of the input or output connection attributes
    """

    ah = AttributeHelper(node)

    if not ah.attribute_exists(attribute_name=attribute_name):
        raise RuntimeError('Attribute: "{}" no exists in object: "{}"'.format(attribute_name, node))

    if cmds.connectionInfo('{}.{}'.format(node, attribute_name), isDestination=True):
        plug = cmds.connectionInfo('{}.{}'.format(node, attribute_name), getExactDestination=True)
        read_only = cmds.ls(plug, readOnly=True)
        # Delete input connections if destination attr is read only
        if read_only:
            source = cmds.connectionInfo(plug, sourceFromDestination=True)
            cmds.disconnectAttr(source, plug)
        else:
            cmds.delete(plug, inputConnectionsAndNodes=True)
