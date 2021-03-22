from itertools import product
from unittest import TestCase
from unittest.mock import patch

from cli.utils import validate_model_cli_args, validate_model_cli_arg_values, handle_graph_creation
from graphs.graph import GraphType


class UtilsTests(TestCase):
    """
    Test for the utils module
    """

    class MockArgs:
        def __init__(self, model=None, graph_representation=None, number_of_vertices=None, number_of_edges=None,
                     number_of_initial_nodes=None, graph_degree=None, initial_connections_per_node=None,
                     probability=None, seed=None):
            self.model = model
            self.graph_representation = graph_representation
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
            'seed': [None, 1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.ER.value, **combination)))

        # ----------------------------------------- #
        # Ensure valid result for Erdos Renyi model #
        # ----------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.ER.value, number_of_vertices=10,
                                                              probability=0.5, seed=1)))

        # -------------------------------------------------- #
        # Ensure invalid result for Custom Erdos Renyi model #
        # -------------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'number_of_edges': [None, 10],
            'probability': [None, 0.5],
            'seed': [None, 1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_ER.value, **combination)))

        # ------------------------------------------------ #
        # Ensure valid result for Custom Erdos Renyi model #
        # ------------------------------------------------ #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_ER.value, number_of_vertices=10,
                                                              number_of_edges=10, probability=0.5, seed=1)))

        # -------------------------------------------- #
        # Ensure invalid result for Random Fixed model #
        # -------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'graph_degree': [None, 10],
            'seed': [None, 1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.RANDOM_FIXED.value, **combination)))

        # ------------------------------------------ #
        # Ensure valid result for Random Fixed model #
        # ------------------------------------------ #
        mock_args = self.MockArgs(model=GraphType.RANDOM_FIXED.value, number_of_vertices=10, graph_degree=10, seed=1)
        self.assertTrue(validate_model_cli_args(mock_args))

        # ------------------------------------------ #
        # Ensure invalid result for Scale Free model #
        # ------------------------------------------ #
        data = {
            'number_of_vertices': [None, 10],
            'seed': [None, 1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(self.MockArgs(model=GraphType.SCALE_FREE.value, **combination)))

        # ---------------------------------------- #
        # Ensure valid result for Scale Free model #
        # ---------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.SCALE_FREE.value, number_of_vertices=10,
                                                              seed=1)))

        # ------------------------------------------------- #
        # Ensure invalid result for Custom Scale Free model #
        # ------------------------------------------------- #
        data = {
            'number_of_vertices': [None, 10],
            'seed': [None, 1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        for combination in combinations:
            self.assertFalse(validate_model_cli_args(
                self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, **combination))
            )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=1))
        )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=1,
                          number_of_initial_nodes=5))
        )

        self.assertFalse(validate_model_cli_args(
            self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, number_of_vertices=10, seed=1,
                          initial_connections_per_node=2))
        )

        # ----------------------------------------------- #
        # Ensure valid result for Custom Scale Free model #
        # ----------------------------------------------- #
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                              number_of_vertices=10, number_of_edges=10, seed=1)))
        self.assertTrue(validate_model_cli_args(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                              number_of_vertices=10, seed=1, number_of_initial_nodes=5,
                                                              initial_connections_per_node=2)))

    def test_validate_model_cli_arg_values(self):
        # -------------------------------------------------------- #
        # Ensure invalid result for None, zero and negative values #
        # -------------------------------------------------------- #
        data = {
            'number_of_vertices': [None, 0, -1],
            'number_of_edges': [None, 0, -1],
            'number_of_initial_nodes': [None, 0, -1],
            'graph_degree': [None, 0, -1],
            'initial_connections_per_node': [None, 0, -1],
            'probability': [None, 0, -1],
            'seed': [None, 0, -1],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())]
        for combination in combinations:
            self.assertFalse(validate_model_cli_arg_values(model='', **combination))

        # ------------------------------------------------ #
        # Ensure invalid result for less than one vertices #
        # ------------------------------------------------ #
        self.assertFalse(validate_model_cli_arg_values(model='', number_of_vertices=1))

        # ---------------------------------------------- #
        # Ensure valid result for more than one vertices #
        # ---------------------------------------------- #
        self.assertTrue(validate_model_cli_arg_values(model='', number_of_vertices=2))

        # ----------------------------------------------------------------- #
        # Ensure invalid result for Custom Erdos Renyi graph when edges are #
        # more than expected, for a specific amount of vertices             #
        # ----------------------------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertFalse(validate_model_cli_arg_values(model=GraphType.CUSTOM_ER.value, number_of_vertices=5,
                                                           number_of_edges=5 * 4 // 2 + 1))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)

        # ----------------------------------------------------------------- #
        # Ensure valid result for Custom Erdos Renyi graph when the given   #
        # edges will result into a Homogeneous graph, for a specific amount #
        # of vertices                                                       #
        # ----------------------------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertTrue(validate_model_cli_arg_values(model=GraphType.CUSTOM_ER.value, number_of_vertices=5,
                                                          number_of_edges=5 * 4 // 2))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)

        # ------------------------------------------------------------------------------------- #
        # Ensure invalid result for Custom Scale Free graph for wrong combination of parameters #
        # ------------------------------------------------------------------------------------- #
        data = {
            'number_of_initial_nodes': [None, 10],
            'initial_connections_per_node': [None, 2],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][1:]
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            for combination in combinations:
                self.assertFalse(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                               number_of_vertices=5, number_of_edges=2, **combination))
                self.assertEqual(mock_communicate_cli_message.call_count, 0)

        # ---------------------------------------------------------------- #
        # Ensure invalid result for Custom Scale Free graph when edges are #
        # more than expected, for a specific amount of vertices            #
        # ---------------------------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertFalse(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                           number_of_vertices=5, number_of_edges=5 * 4 // 2 + 1))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)

        # ----------------------------------------------------------------- #
        # Ensure valid result for Custom Scale Free graph when the given    #
        # edges will result into a Homogeneous graph, for a specific amount #
        # of vertices                                                       #
        # ----------------------------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertTrue(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                          number_of_vertices=5, number_of_edges=5 * 4 // 2))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)

        # ------------------------------------------------------------------------------------------ #
        # Ensure invalid result for Custom Full Scale Free graph for wrong combination of parameters #
        # ------------------------------------------------------------------------------------------ #
        data = {
            'number_of_edges': [None],
            'number_of_initial_nodes': [None, 10],
            'initial_connections_per_node': [None, 2],
        }
        combinations = [dict(zip(data, v)) for v in product(*data.values())][:-1]
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            for combination in combinations:
                self.assertFalse(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                               number_of_vertices=5, **combination))
                self.assertEqual(mock_communicate_cli_message.call_count, 0)

        # ----------------------------------------------------------------------- #
        # Ensure invalid result for Custom Full Scale Free graph when the initial #
        # edges are more than expected, for a specific amount of initial vertices #
        # ----------------------------------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertFalse(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                           number_of_vertices=10, number_of_initial_nodes=3,
                                                           initial_connections_per_node=4))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)

        # ----------------------------------------------- #
        # Ensure valid result for Custom Scale Free graph #
        # ----------------------------------------------- #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            self.assertTrue(validate_model_cli_arg_values(model=GraphType.CUSTOM_SCALE_FREE.value,
                                                          number_of_vertices=5, number_of_edges=2))
            self.assertEqual(mock_communicate_cli_message.call_count, 0)

    def test_handle_graph_creation(self):
        # -------------------------------------- #
        # Ensure Homogeneous graph creation call #
        # -------------------------------------- #
        data = {'number_of_vertices': 10}
        with patch('cli.utils.Homogeneous.create_homogeneous_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.HOMOGENEOUS.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # --------------------------------------- #
        # Ensure Custom Renyi graph creation call #
        # --------------------------------------- #
        data = {'number_of_vertices': 10, 'probability': 0.5, 'seed': 0}
        with patch('cli.utils.ErdosRenyi.create_er_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.ER.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # --------------------------------------------- #
        # Ensure Custom Erdos Renyi graph creation call #
        # --------------------------------------------- #
        data = {'number_of_vertices': 10, 'number_of_edges': 10, 'probability': 0.5, 'seed': 0}
        with patch('cli.utils.ErdosRenyi.create_custom_er_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.CUSTOM_ER.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # --------------------------------------- #
        # Ensure Random Fixed graph creation call #
        # --------------------------------------- #
        data = {'number_of_vertices': 10, 'graph_degree': 10, 'seed': 0}
        with patch('cli.utils.RandomFixed.create_random_fixed_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.RANDOM_FIXED.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # ------------------------------------------------------------------ #
        # Ensure Scale Free with Preferential Attachment graph creation call #
        # ------------------------------------------------------------------ #
        data = {'number_of_vertices': 10, 'seed': 0}
        with patch('cli.utils.ScaleFreePA.create_scale_free_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.SCALE_FREE.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # ---------------------------------------------------------------------------------------------- #
        # Ensure Full Scale Free with Preferential Attachment and Incremental Growth graph creation call #
        # ---------------------------------------------------------------------------------------------- #
        data = {'number_of_vertices': 10, 'number_of_initial_nodes': 3, 'seed': 0}
        with patch('cli.utils.FullScaleFree.create_full_scale_free_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.SCALE_FREE.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # ------------------------------------------------------------------------- #
        # Ensure Custom Scale Free with Preferential Attachment graph creation call #
        # ------------------------------------------------------------------------- #
        data = {'number_of_vertices': 10, 'number_of_edges': 10, 'seed': 0}
        with patch('cli.utils.ScaleFreePA.create_custom_scale_free_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # ----------------------------------------------------------------------------------------------------- #
        # Ensure Custom Full Scale Free with Preferential Attachment and Incremental Growth graph creation call #
        # ----------------------------------------------------------------------------------------------------- #
        data = {'number_of_vertices': 10, 'number_of_initial_nodes': 3, 'initial_connections_per_node': 2, 'seed': 0}
        with patch('cli.utils.FullScaleFree.create_full_scale_free_graph') as mock_create:
            handle_graph_creation(self.MockArgs(model=GraphType.CUSTOM_SCALE_FREE.value, **data))
            self.assertEqual(mock_create.call_count, 1)
            mock_create.assert_called_with(**data)

        # ------------------------------------ #
        # Ensure error for invalid graph model #
        # ------------------------------------ #
        with patch('cli.utils.communicate_cli_message') as mock_communicate_cli_message:
            handle_graph_creation(self.MockArgs(model='Unknown'))
            self.assertEqual(mock_communicate_cli_message.call_count, 1)
