from unittest.mock import Mock
import pytest
from praktikum.burger import Burger

class TestBurger:

    def test_add_ingredient_adds_ingredient_to_list(self):
        burger = Burger()
        ingredient = Mock()

        burger.add_ingredient(ingredient)

        assert burger.ingredients == [ingredient]

    def test_set_buns_sets_bun(self):
        burger = Burger()
        bun = Mock()

        burger.set_buns(bun)

        assert burger.bun == bun

    def test_remove_ingredient_removes_ingredient(self):
        burger = Burger()
        ingredient_1 = Mock()
        ingredient_2 = Mock()

        burger.add_ingredient(ingredient_1)
        burger.add_ingredient(ingredient_2)

        burger.remove_ingredient(0)
        assert burger.ingredients == [ingredient_2]

    @pytest.mark.parametrize('index, new_index, expected_order', [
        (0, 2, [1, 2, 0]),
        (2, 0, [2, 0, 1]),
    ])
    def test_move_ingredient_changes_order(self, index, new_index, expected_order):
        burger = Burger()
        ingredients = [Mock(), Mock(), Mock()]
        for ingredient in ingredients:
            burger.add_ingredient(ingredient)

        burger.move_ingredient(index, new_index)

        assert burger.ingredients == [ingredients[i] for i in expected_order]

    def test_get_receipt_returns_correct_receipt(self):
        burger = Burger()

        bun = Mock()
        bun.get_name.return_value = 'black bun'
        bun.get_price.return_value = 100

        ingredient = Mock()
        ingredient.get_type.return_value = 'SAUCE'
        ingredient.get_name.return_value = 'hot sauce'
        ingredient.get_price.return_value = 100

        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        expected_receipt = '\n'.join([
            '(==== black bun ====)',
            '= sauce hot sauce =',
            '(==== black bun ====)\n',
            'Price: 300',
        ])

        assert burger.get_receipt() == expected_receipt

    @pytest.mark.parametrize('bun_price, ingredient_prices, expected_price', [
        (100, [], 200),
        (100, [50], 250),
        (100, [50, 30, 20], 300),
    ])
    def test_get_price_returns_sum_of_bun_and_ingredients(self, bun_price, ingredient_prices, expected_price):
        burger = Burger()

        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected_price