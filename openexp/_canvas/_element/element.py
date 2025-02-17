# coding=utf-8

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
import copy
from libopensesame.exceptions import InvalidValue
from functools import partial
from openexp.color import color

INF = float('inf')
NUMERIC_PROPERTIES = u'x', u'y', u'w', u'h', u'r'


class Element:

    r"""A base class for sketchpad elements."""
    # A property that indicates whether style properties (color etc) can be
    # changed or not.
    read_only = False

    def __init__(self, canvas, **properties):
        r"""Constructor.

        Parameters
        ----------
        canvas : Canvas
            The canvas of which this element is part.
        **properties : dict
            A dict with style arguments such as color, fill, etc.
        """
        self._canvas = canvas
        if u'visible' not in properties:
            properties[u'visible'] = True
        if u'color' in properties:
            properties[u'color'] = color(self.experiment, properties[u'color'])
        self._assert_numeric(**{
            prop: val
            for prop, val in properties.items()
            if prop in NUMERIC_PROPERTIES
        })
        self._properties = properties
        for prop in self.property_names:
            self._create_property(prop)
        if canvas.auto_prepare and self.visible:
            self.prepare()

    def __contains__(self, xy):

        x, y, w, h = self.rect
        return x <= xy[0] and x+w >= xy[0] and y <= xy[1] and y+h >= xy[1]

    def __iter__(self):
        r"""Elements are iterable, but by default contain only themselves.
        However, Group objects can contain other elements.
        """
        yield self

    def __len__(self):
        r"""Elements have a length, but by default this is 1. However, Group
        objects can have a different length.
        """
        return 1

    def __add__(self, element):
        r"""Implements the + syntax, which combines Element objects into Group
        objects.

        Parameters
        ----------
        element : Element
            The element to add.

        Returns
        -------
        Group
            A group of elements.
        """
        from openexp._canvas._element.group import Group
        return Group(self.canvas, [self, element])

    def copy(self, canvas):
        r"""Creates a deep copy of the current element. This new copy becomes
        part of the provided canvas.

        Parameters
        ----------
        canvas : Canvas
            The canvas of which the copied element is part.

        Returns
        -------
        Element
            A copy of the current element.
        """
        try:
            e = copy.deepcopy(self)
        except (ValueError, TypeError):
            # Silently fall back to shallow copies if deep copies are not
            # possible. This happens for example with the c-types-based
            # PsychoPy stimuli.
            e = copy.copy(self)
        e._canvas = canvas
        return e

    def prepare(self):
        r"""Is called when the canvas is prepared. This should be implemented
        by backend-specific element objects.
        """
        pass

    def show(self):
        r"""Is called when the canvas is shown. This should be implemented by
        backend-specfic element objects.
        """
        pass

    def _on_attribute_change(self, **kwargs):
        r"""Is called when an attribute, such as color, is changed.

        Parameters
        ----------
        **kwargs : dict
            A dict with changed attributes.
        """
        pass

    @property
    def experiment(self):
        return self._canvas.experiment

    @property
    def to_xy(self):
        return self._canvas.to_xy

    @property
    def none_to_center(self):
        return self._canvas.none_to_center

    @property
    def property_names(self):
        return (
            set(self._properties.keys())
            | set(self._canvas.configurables.keys())
        )

    @property
    def rect(self):
        raise NotImplementedError()

    @property
    def top(self):
        return self.rect[1]

    @property
    def left(self):
        return self.rect[0]

    @property
    def width(self):
        return self.rect[2]

    @property
    def height(self):
        return self.rect[3]

    @property
    def size(self):
        return self.rect[2:]

    @property
    def position(self):
        return self.rect[:2]

    def _create_property(self, key):
        r"""Dynamically creates a getter/setter property. This is used to make
        style arguments such as color get-able and set-able.
        """
        setattr(self.__class__, key, property(
                partial(self._getter, key),
                partial(self._setter, key),
                self._deller, u''))

    @staticmethod
    def _getter(key, self):
        r"""A getter for dynamically created properties.

        Parameters
        ----------
        key : str
            A property name.
        self : Element.
            The Element instance. For technical reasons this is passed as the
            second argument.
        """
        try:
            return self._properties[key]
        except KeyError:
            return self._canvas.__cfg__[key]

    @staticmethod
    def _setter(key, self, val):
        r"""A setter for dynamically created properties.

        Parameters
        ----------
        key : str
            A property name.
        self : Element.
            The Element instance. For technical reasons this is passed as the
            second argument.
        val : Any
            A property value.
        """
        if key in NUMERIC_PROPERTIES:
            self._assert_numeric(**{key: val})
        if key == u'color':
            val = color(self.experiment, val)
        self._properties[key] = val
        self._on_attribute_change(**{key: val})

    @staticmethod
    def _deller(self, key):
        r"""A deller for dynamically created properties.

        Parameters
        ----------
        key : str
            A property name.
        """
        pass

    @staticmethod
    def _assert_numeric(**kwdict):

        for name, v in kwdict.items():
            try:
                v = float(v)
            except ValueError:
                raise InvalidValue(
                    u'%s should be int or float, not %s' % (name, v))
            if v != v:
                raise InvalidValue(
                u'%s should be int or float, not nan' % name)
            if v == INF:
                raise InvalidValue(
                    u'%s should be int or float, not inf' % name)

    @staticmethod
    def _rect(x, y, w, h):
        r"""Fixes negative width and heights when defining a rect

        Parameters
        ----------
        x
            An X coordinate
        y
            A Y coordinate
        w
            A width
        h
            A height

        Returns
        -------
        """
        Element._assert_numeric(x=x, y=y, w=w, h=h)
        if w < 0:
            x += w
            w = abs(w)
        if h < 0:
            y += h
            h = abs(h)
        return x, y, w, h
