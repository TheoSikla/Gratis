from itertools import product
from unittest import TestCase

from cli.utils import validate_model_cli_args
from graphs.graph import GraphType


class UtilsTests(TestCase):
    """
    Test for the utils module
    """

    class MockArgs:
        def __init__(self, model=None, number_of_vertices=None, number_of_edges=None, number_of_initial_nodes=None,
                     graph_degree=None, initial_connections_per_node=None, probability=None, seed=None):
            self.model = model
            self.number_of_vertices = number_of_vertices
            self.number_of_edges = number_of_edges
            self.number_of_initial_nodes = number_of_initial_nodes
            self.graph_degree = graph_degree
            self.initial_connections_per_node = initial_connections_per_node
            self.probability = probability
            self.seed = seed

    def test_validate_model_cli_args(self):
        # ------------------------------------------- #
        # Ensure invalid result for no model provided #
        # ------------------------------------------- #
        self.assertFalse(validate_model_cli_args(self.MockArgs()))

        # ------------------------------------------- #
        # Ensure invalid result for Homogeneous model #
        # ------------------------------------------- #
        self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.HOMOGENEOUS.value)))

        # ----------------------------------------- #
        # Ensure valid result for Homogeneous model #
        # ----------------------------------------- #
        self.assertTrue(validate_model_cli_args(
            self.MockArgs(model=GraphType.HOMOGENEOUS.value, number_of_vertices=10))
        )

        # ------------------------------------------- #
        # Ensure invalid result for Erdos Renyi model #
        # ------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'probability': [None, 0.5],
            'seed': [None, 0],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.ER.value, **combination)))

        # ----------------------------------------- #
        # Ensure valid result for Erdos Renyi model #
        # ----------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.ER.value, number_of_vertices=10,
                                                              probability=0.5, seed=0)))

        # -------------------------------------------------- #
        # Ensure invalid result for Custom Erdos Renyi model #
        # -------------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'number_of_edges': [None, 10],
            'probability': [None, 0.5],
            'seed': [None, 0],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_ER.value, **combination)))

        # ------------------------------------------------ #
        # Ensure valid result for Custom Erdos Renyi model #
        # ------------------------------------------------ #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_ER.value, number_of_vertices=10,
                                                              number_of_edges=10, probability=0.5, seed=0)))

        # -------------------------------------------- #
        # Ensure invalid result for Random Fixed model #
        # -------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'graph_degree': [None, 10],
            'seed': [None, 0],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.RANDOM_FIXED.value, **combination)))

        # ------------------------------------------ #
        # Ensure valid result for Random Fixed model #
        # ------------------------------------------ #
        mock_args = self.MockArgs(model=GraphType.RANDOM_FIXED.value, number_of_vertices=10, graph_degree=10, seed=0)
        self.assertTrue(validate_model_cli_args(mock_args))

        # ------------------------------------------ #
        # Ensure invalid result for Scale Free model #
        # ------------------------------------------ #
        data = {
            'number_of_vertices': [None, 10],
            'seed': [None, 0],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.SCALE_FREE.value, **combination)))

        # ---------------------------------------- #
        # Ensure valid result for Scale Free model #
        # ---------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.SCALE_FREE.value, number_of_vertices=10,
                                                              seed=0)))

        # ------------------------------------------------- #
        # Ensure invalid result for Custom Scale Free model #
        # ------------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'seed': [None, 0],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(
                self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, **combination))
            )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=0))
        )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=0,
                          number_of_initial_nodes=5))
        )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=0,
                          initial_connections_per_node=2))
        )

        # ----------------------------------------------- #
        # Ensure valid result for Custom Scale Free model #
        # ----------------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                              number_of_vertices=10, number_of_edges=10, seed=0)))
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                              number_of_vertices=10, seed=0, number_of_initial_nodes=5,
                                                              initial_connections_per_node=2)))
