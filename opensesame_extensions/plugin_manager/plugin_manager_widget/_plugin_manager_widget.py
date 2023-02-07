# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from libqtopensesame.widgets.base_widget import base_widget
from plugin_manager_widget._plugin_widget import plugin_widget


class plugin_manager_widget(base_widget):

    r"""A list of plugins."""
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main-window object.
        """
        super().__init__(main_window,
            ui=u'extensions.plugin_manager.plugin_manager')
        self.plugin_list = self.plugin_manager.filter(
            mode=main_window.mode)
        for plugin in sorted(self.plugin_list):
            w = plugin_widget(plugin, main_window)
            self.ui.layout_container.addWidget(w)
