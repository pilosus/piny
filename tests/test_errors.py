import pytest

from src.piny import LoadingError, YamlLoader


def test_loading_error():
    with pytest.raises(
        LoadingError, match=r"Loading YAML file failed.+no-such-config.yaml"
    ):
        YamlLoader(path="no-such-config.yaml").load()
