from __future__ import annotations

import ast
import logging

from codeflash.api.aiservice import AiServiceClient
from codeflash.code_utils.code_utils import get_run_tmp_file, module_name_from_file_path
from codeflash.discovery.functions_to_optimize import FunctionToOptimize
from codeflash.verification.verification_utils import (
    ModifyInspiredTests,
    TestConfig,
    delete_multiple_if_name_main,
    get_test_file_path,
)


def generate_tests(
    aiservice_client: AiServiceClient,
    source_code_being_tested: str,
    function_to_optimize: FunctionToOptimize,
    helper_function_names: list[str],
    module_path: str,
    test_cfg: TestConfig,
    test_timeout: int,
    use_cached_tests: bool,
    function_trace_id: str,
) -> tuple[str, str] | None:
    # TODO: Sometimes this recreates the original Class definition. This overrides and messes up the original
    #  class import. Remove the recreation of the class definition
    logging.info(f"Generating new tests for function {function_to_optimize.function_name} ...")
    if use_cached_tests:
        import importlib

        module = importlib.import_module(module_path)
        generated_test_source = module.CACHED_TESTS
        instrumented_test_source = module.CACHED_INSTRUMENTED_TESTS
        path = get_run_tmp_file("").replace("\\", "\\\\")  # Escape backslash for windows paths
        instrumented_test_source = instrumented_test_source.replace(
            "{codeflash_run_tmp_dir_client_side}",
            path,
        )
        logging.info(f"Using cached tests from {module_path}.CACHED_TESTS")
    else:
        test_module_path = module_name_from_file_path(
            get_test_file_path(test_cfg.tests_root, function_to_optimize.function_name, 0),
            test_cfg.project_root_path,
        )
        response = aiservice_client.generate_regression_tests(
            source_code_being_tested=source_code_being_tested,
            function_to_optimize=function_to_optimize,
            helper_function_names=helper_function_names,
            module_path=module_path,
            test_module_path=test_module_path,
            test_framework=test_cfg.test_framework,
            test_timeout=test_timeout,
            trace_id=function_trace_id,
        )
        if response and isinstance(response, tuple) and len(response) == 2:
            generated_test_source, instrumented_test_source = response
            path = get_run_tmp_file("").replace("\\", "\\\\")  # Escape backslash for windows paths
            instrumented_test_source = instrumented_test_source.replace(
                "{codeflash_run_tmp_dir_client_side}",
                path,
            )
        else:
            logging.warning(
                f"Failed to generate and instrument tests for {function_to_optimize.function_name}"
            )
            return None

    # TODO: Add support for inspired tests
    # inspired_unit_tests = ""

    # merged_test_source = merge_unit_tests(
    #     instrumented_test_source, inspired_unit_tests, test_cfg.test_framework
    # )

    return generated_test_source, instrumented_test_source


def merge_unit_tests(unit_test_source: str, inspired_unit_tests: str, test_framework: str) -> str:
    try:
        inspired_unit_tests_ast = ast.parse(inspired_unit_tests)
        unit_test_source_ast = ast.parse(unit_test_source)
    except SyntaxError as e:
        logging.exception(f"Syntax error in code: {e}")
        return unit_test_source
    import_list: list[ast.stmt] = list()
    modified_ast = ModifyInspiredTests(import_list, test_framework).visit(inspired_unit_tests_ast)
    if test_framework == "pytest":
        # Because we only want to modify the top level test functions
        for node in ast.iter_child_nodes(modified_ast):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    node.name = node.name + "__inspired"
    unit_test_source_ast.body.extend(modified_ast.body)
    unit_test_source_ast.body = import_list + unit_test_source_ast.body
    if test_framework == "unittest":
        unit_test_source_ast = delete_multiple_if_name_main(unit_test_source_ast)
    return ast.unparse(unit_test_source_ast)
