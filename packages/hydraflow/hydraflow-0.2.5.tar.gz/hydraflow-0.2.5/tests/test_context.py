from unittest.mock import MagicMock, patch

import mlflow
import pytest

from hydraflow.context import log_run, start_run, watch
from hydraflow.runs import RunCollection


@pytest.fixture
def runs(monkeypatch, tmp_path):
    from hydraflow.runs import list_runs

    monkeypatch.chdir(tmp_path)

    with (
        patch("hydraflow.context.HydraConfig.get") as mock_hydra_config,
        patch("hydraflow.context.mlflow.log_artifacts") as mock_log_artifacts,
    ):
        mock_hydra_config.return_value.runtime.output_dir = "/tmp"
        mock_log_artifacts.return_value = None

        mlflow.set_experiment("test_run")
        for x in range(3):
            cfg = {"x": x, "l": [x, x, x], "d": {"i": x}}
            with start_run(cfg):
                mlflow.log_param("y", x)

        return list_runs(["test_run"])


def test_runs_len(runs: RunCollection):
    assert len(runs) == 3


@pytest.mark.parametrize("i", [0, 1, 2])
@pytest.mark.parametrize("n", ["x", "y"])
def test_runs_params(runs: RunCollection, i: int, n: str):
    assert runs[i].data.params[n] == str(i)


@pytest.mark.parametrize("i", [0, 1, 2])
def test_runs_params_list(runs: RunCollection, i: int):
    assert runs[i].data.params["l"] == f"[{i}, {i}, {i}]"


@pytest.mark.parametrize("i", [0, 1, 2])
def test_runs_params_dict(runs: RunCollection, i: int):
    assert runs[i].data.params["d.i"] == str(i)


def test_log_run_error_handling():
    config = MagicMock()
    config.some_param = "value"

    with (
        patch("hydraflow.context.log_params") as mock_log_params,
        patch("hydraflow.context.HydraConfig.get") as mock_hydra_config,
        patch("hydraflow.context.mlflow.log_artifacts") as mock_log_artifacts,
    ):
        mock_log_params.side_effect = Exception("Test exception")
        mock_hydra_config.return_value.runtime.output_dir = "/tmp"
        mock_log_artifacts.return_value = None

        with pytest.raises(Exception, match="Test exception"):
            with log_run(config):
                pass


def test_watch_error_handling():
    func = MagicMock()
    dir = "/tmp"

    with patch("hydraflow.context.Observer") as mock_observer:
        mock_observer_instance = mock_observer.return_value
        mock_observer_instance.start.side_effect = Exception("Test exception")

        with pytest.raises(Exception, match="Test exception"):
            with watch(func, dir):
                pass
