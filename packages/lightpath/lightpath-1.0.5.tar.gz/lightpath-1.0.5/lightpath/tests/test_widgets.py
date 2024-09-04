from unittest.mock import Mock

import pytest
from ophyd import Device

from lightpath import BeamPath
from lightpath.tests.conftest import wait_until
from lightpath.ui import LightRow
from lightpath.ui.widgets import (state_colors, symbol_for_device,
                                  to_stylesheet_color)


@pytest.fixture(scope='function')
def lightrow(path: BeamPath, qtbot):
    # Generate lightpath
    w = LightRow(path.path[3], path)
    qtbot.addWidget(w)
    # Replace Update functions with mocks
    setattr(w.state_label, 'setText', Mock())
    return w


def test_widget_updates(lightrow: LightRow, path: BeamPath):
    # inserted device may still permit beam
    ipimb = path.path[5]
    ipimb_row = LightRow(ipimb, path)
    # Toggle device to trigger callbacks
    ipimb.insert()
    ipimb.remove()
    ipimb.insert()
    lightrow.device.insert()

    def half_removed():
        return (to_stylesheet_color(state_colors['half_removed'])
                in ipimb_row.state_label.styleSheet())

    wait_until(half_removed, timeout=5)
    assert half_removed()

    lightrow.device.remove()

    def removed():
        return (to_stylesheet_color(state_colors['removed'])
                in lightrow.state_label.styleSheet())

    wait_until(removed, timeout=5)
    assert removed()

    lightrow.device.insert()

    def blocking():
        return (to_stylesheet_color(state_colors['blocking'])
                in lightrow.state_label.styleSheet())

    wait_until(blocking, timeout=5)
    assert blocking()

    # Check that callbacks have been called
    assert lightrow.state_label.setText.called


def test_widget_icon(lightrow: LightRow):
    assert symbol_for_device(lightrow.device) == lightrow.device._icon
    # Smoke test a device without an icon
    device = Device(name='test')
    symbol_for_device(device)
    # Smoke test a device with a malformed icon
    device._icon = 'definetly not an icon'
    lr = LightRow(device, lightrow.path)
    lr.update_state()
