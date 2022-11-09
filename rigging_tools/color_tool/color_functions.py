from maya import cmds
import os
import random


def show():
    if cmds.window('Color', exists=True):
        cmds.deleteUI('Color')

    # .UI FILE LOAD #
    absolut_path = os.path.dirname(os.path.abspath(__file__))
    qt_win = cmds.loadUI(uiFile='{}/color.ui'.format(absolut_path))
    cmds.showWindow(qt_win)


def color_draw(color_ui):
    default_colors = {1: (1, 0, 0),
                      2: (1, 1, 0),
                      3: (0, 1, 0),
                      4: (0, 1, 1),
                      5: (0, 0, 1),
                      6: (1, 0, 1),
                      7: (0.375, 0, 0.039),
                      8: (0, 0.003, 0.157),
                      9: (0.000, 0.091, 0.022),
                      10: (0.037, 0.000, 0.085),
                      11: (0.301, 0.095, 0.055),
                      12: (0.077, 0.033, 0.028),
                      13: (0.366, 0.037, 0.000),
                      14: (0.399, 0.051, 0.182),
                      15: (0.000, 0.081, 0.366),
                      16: (0.085, 1.000, 0.413),
                      17: (1.000, 0.479, 0.479),
                      18: (0.798, 0.458, 0.236),
                      19: (1.000, 1.000, 0.164),
                      20: (0.000, 0.366, 0.123),
                      21: (0.403, 0.185, 0.051),
                      22: (0.389, 0.403, 0.051),
                      23: (0.179, 0.403, 0.051),
                      24: (0.051, 0.403, 0.147),
                      25: (0.051, 0.403, 0.403),
                      26: (0.051, 0.176, 0.403),
                      27: (0.201, 0.051, 0.403),
                      28: (0.403, 0.051, 0.185)
                      }

    list_wb = {
        1: (1, 1, 1),
        2: (0.890, 0.890, 0.890),
        3: (0.780, 0.780, 0.780),
        4: (0.671, 0.671, 0.671),
        5: (0.561, 0.561, 0.561),
        6: (0.451, 0.451, 0.451),
        7: (0.341, 0.341, 0.341),
        8: (0.231, 0.231, 0.231),
        9: (0.122, 0.122, 0.122),
        10: (0, 0, 0)
    }

    list_cha = {
        'center': (1, 1, 0),
        'right': (1, 0, 0),
        'left': (0, 0, 1),
        'spine': (0.5, 1, 0.5),
        'root': (0, 1, 0),
        'blend_r': (1, 0.5, 1),
        'blend_l': (0, 1, 1),
        'setting': (1, 0, 1)
    }

    obj_shape = cmds.listRelatives(path=1, type='shape')

    # to know what list
    usage = color_ui.split('_')[0]

    if usage == 'default':
        number = color_ui.split('default_')[1]
        color = default_colors.get(int(number))
    elif usage == 'wb':
        number = color_ui.split('wb_')[1]
        color = list_wb.get(int(number))
    else:
        if color_ui == 'random':
            color = (random.uniform(0.000, 1.000), random.uniform(0.000, 1.000), random.uniform(0.000, 1.000))
        else:
            color = list_cha.get(str(color_ui))

    # color
    rgb = ('R', 'G', 'B')

    # set colors all Shape Node
    for channel, color in zip(rgb, color):
        for obj in obj_shape:
            cmds.setAttr('{}.overrideEnabled'.format(obj), 1)
            cmds.setAttr('{}.overrideRGBColors'.format(obj), 1)
            cmds.setAttr('{}.overrideColor{}'.format(obj, channel), color)


def color_draw_picker():
    obj_shape = cmds.listRelatives(path=1, type='shape')

    color = cmds.colorEditor(query=True, rgb=True)

    # Color
    rgb = ('R', 'G', 'B')
    for channel, color in zip(rgb, color):
        for obj in obj_shape:
            cmds.setAttr('{}.overrideEnabled'.format(obj), 1)
            cmds.setAttr('{}.overrideRGBColors'.format(obj), 1)
            cmds.setAttr('{}.overrideColor{}'.format(obj, channel), color)


