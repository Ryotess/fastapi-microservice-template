import ast
from pathlib import Path


CONFIG_SOURCE = Path(__file__).resolve().parents[1] / "src" / "config.py"


def test_global_settings_uses_settings_config_builder():
    tree = ast.parse(CONFIG_SOURCE.read_text())

    global_settings_class = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "GlobalSettings"
    )
    model_config_assignment = next(
        node
        for node in global_settings_class.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "model_config"
            for target in node.targets
        )
    )

    assert isinstance(model_config_assignment.value, ast.Call)
    assert isinstance(model_config_assignment.value.func, ast.Name)
    assert model_config_assignment.value.func.id == "build_settings_config"


def test_config_does_not_use_pydantic_config_dict():
    tree = ast.parse(CONFIG_SOURCE.read_text())

    pydantic_config_dict_imports = [
        alias.name
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module == "pydantic"
        for alias in node.names
        if alias.name == "ConfigDict"
    ]

    assert pydantic_config_dict_imports == []
