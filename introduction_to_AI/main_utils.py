from __future__ import annotations

from typing import Optional, Any
from introduction_to_AI.models import State


def display_state(state: State, graphic_displayer: Optional[Any], verbose):
    """Display State

    manage the visual/terminal display of a given state object.
    this is an optional function that will do nothing if both graphic_displayer and verbose equal to false

    :param state: a given state object
    :param graphic_displayer: (optional) a graphic-displayer object
    :param verbose: (optional) if true, print the result of state.display() to the terminal (false by default)
    """
    if graphic_displayer:
        graphic_displayer.refresh(state.get_value())

    if verbose:
        state.display()
