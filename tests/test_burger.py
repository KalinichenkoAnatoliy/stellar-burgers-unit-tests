import pytest
from unittest.mock import Mock
from typing import List

from ..burger import Burger
from ..bun import Bun
from ..ingredient import Ingredient


class TestBurger:

    @pytest.fixture
    def burger(self):
        return Burger()

    @pytest.fixture
    def mock_bun(self):
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = 50.0
        mock_bun.get_name.return_value = "Mock Bun"
        return mock_bun

    @pytest.fixture
    def mock_ingredient(self):
        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_price.return_value = 25.0
        mock_ingredient.get_name.return_value = "Mock Ingredient"
        mock_ingredient.get_type.return_value = "Mock Type"
        return mock_ingredient

    def test_set_buns(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self, burger, mock_ingredient):
        burger.add_ingredient(mock_ingredient)
        assert mock_ingredient in burger.ingredients

    def test_remove_ingredient(self, burger, mock_ingredient):
        burger.add_ingredient(mock_ingredient)
        burger.remove_ingredient(0)
        assert mock_ingredient not in burger.ingredients
        assert len(burger.ingredients) == 0

    def test_move_ingredient(self, burger, mock_ingredient):
        mock_ingredient2 = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        burger.add_ingredient(mock_ingredient2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients[1] == mock_ingredient
        assert burger.ingredients[0] == mock_ingredient2

    def test_get_price(self, burger, mock_bun, mock_ingredient):
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        expected_price = mock_bun.get_price() * 2 + mock_ingredient.get_price()
        assert burger.get_price() == expected_price

    def test_get_receipt(self, burger, mock_bun, mock_ingredient):
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        expected_receipt = (
            f"(==== {mock_bun.get_name()} ====)\n"
            f"= mock type {mock_ingredient.get_name()} =\n"
            f"(==== {mock_bun.get_name()} ====)\n"
            f"\nPrice: {mock_bun.get_price() * 2 + mock_ingredient.get_price()}"
        )
        assert burger.get_receipt() == expected_receipt

    def test_remove_ingredient_exception(self, burger: Burger, mock_ingredient: Mock):
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_move_ingredient_exception(self, burger: Burger, mock_ingredient: Mock):
        burger.add_ingredient(mock_ingredient)
        with pytest.raises(IndexError):
            burger.move_ingredient(1, 0)