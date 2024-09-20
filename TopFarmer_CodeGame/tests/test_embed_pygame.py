import time
import pytest

import pygame
from embed_pygame import EmbedPygame


@pytest.fixture
def embed_pygame_instance():
    return EmbedPygame()


def test_exit(embed_pygame_instance):
    # Act
    embed_pygame_instance.exit()

    # Assert
    assert not pygame.get_init(), "Pygame should be uninitialized after exit."


@pytest.fixture
def embed_pygame_instance():
    return EmbedPygame()


@pytest.mark.parametrize(
    "width, height, cell_size",
    [
        (100, 100, 10),
        (200, 200, 20),
        (300, 300, 30),
    ],
    ids=[
        "10x10 grid",
        "10x10 grid with larger cells",
        "10x10 grid with even larger cells",
    ],
)
def test_render_grid(embed_pygame_instance, width, height, cell_size):
    # Act
    embed_pygame_instance.render_grid(width, height, cell_size)

    # Assert
    # No exceptions should be raised, and the grid should be rendered correctly
    assert True


def test_render_farm(embed_pygame_instance):
    # Act
    embed_pygame_instance.render_farm()

    # Assert
    # No exceptions should be raised, and the farm should be rendered correctly
    assert True


@pytest.mark.parametrize(
    "code, expected",
    [
        ("farmer.move('up')", []),
        ("farmer.move('wrong')", [("farmer.move", 1)]),
        ("farmer.plant('potato', 'down')", []),
        ("farmer.plant('potato', 'wrong')", [("farmer.plant", 1)]),
        ("farmer.harvest('left')", []),
        ("farmer.harvest('wrong')", [("farmer.harvest", 1)]),
    ],
    ids=[
        "valid move",
        "invalid move",
        "valid plant",
        "invalid plant",
        "valid harvest",
        "invalid harvest",
    ],
)
def test_direction_helper(embed_pygame_instance, code, expected):
    # Act
    result = embed_pygame_instance.direction_helper(code)

    # Assert
    assert result == expected


@pytest.fixture
def embed_pygame_instance():
    return EmbedPygame()


def test_update(embed_pygame_instance, mocker):
    # Arrange
    mock_render_farm = mocker.patch.object(embed_pygame_instance, "render_farm")
    mock_render_grid = mocker.patch.object(embed_pygame_instance, "render_grid")
    mock_flip = mocker.patch("pygame.display.flip")

    # Act
    embed_pygame_instance.update()

    # Assert
    mock_render_farm.assert_called_once()
    mock_render_grid.assert_called_once_with(
        embed_pygame_instance.SCREEN_WIDTH,
        embed_pygame_instance.SCREEN_HEIGHT,
        embed_pygame_instance.SCALE_FACTOR,
    )
    mock_flip.assert_called_once()
