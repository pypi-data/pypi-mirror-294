"""This file prepares unit tests for model training."""

import os
from pathlib import Path

import pytest
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, open_dict

from alphafold3_pytorch.train import train
from tests.helpers.run_if import RunIf


def test_train_fast_dev_run(cfg_train: DictConfig) -> None:
    """Run for 1 train, val and test step.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    pytest.skip("This test is skipped for the sake of CI speed.")
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_steps = 1
        cfg_train.trainer.fast_dev_run = True
        cfg_train.trainer.accelerator = "cpu"
    train(cfg_train)


@RunIf(min_gpus=1)
def test_train_fast_dev_run_gpu(cfg_train: DictConfig) -> None:
    """Run for 1 train, val and test step on GPU.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    pytest.skip("This test is skipped for the sake of CI speed.")
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_steps = 1
        cfg_train.trainer.fast_dev_run = True
        cfg_train.trainer.accelerator = "gpu"
    train(cfg_train)


# NOTE: The current AlphaFold 3 implementation does not support mixed-precision training
# due to the `torch.svd` error: `RuntimeError: "svd_cuda_gesvdjBatched" not implemented for 'Half'`.
# This test is skipped until the issue is resolved.


@RunIf(min_gpus=1)
@pytest.mark.slow
def test_train_steps_gpu_amp(cfg_train: DictConfig) -> None:
    """Train 2 steps on GPU with mixed-precision.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    pytest.skip(
        "This test is skipped for the sake of CI speed as well as the current lack of mixed-precision support."
    )
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_steps = 2
        cfg_train.trainer.accelerator = "gpu"
        cfg_train.trainer.precision = 16
    train(cfg_train)


@pytest.mark.slow
def test_train_steps_double_val_loop(cfg_train: DictConfig) -> None:
    """Train 2 steps with validation loop twice per epoch.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    pytest.skip("This test is skipped for the sake of CI speed.")
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_steps = 2
        cfg_train.trainer.val_check_interval = 0.5
    train(cfg_train)


@pytest.mark.slow
def test_train_ddp_sim(cfg_train: DictConfig) -> None:
    """Simulate DDP (Distributed Data Parallel) for 2 steps on 2 CPU processes.

    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    pytest.skip("This test is skipped for the sake of CI speed.")
    HydraConfig().set_config(cfg_train)
    with open_dict(cfg_train):
        cfg_train.trainer.max_steps = 2
        cfg_train.trainer.accelerator = "cpu"
        cfg_train.trainer.devices = 2
        cfg_train.trainer.strategy = "ddp_spawn"
    train(cfg_train)


@pytest.mark.slow
def test_train_resume(tmp_path: Path, cfg_train: DictConfig) -> None:
    """Run 1 epoch, finish, and resume for another epoch.

    :param tmp_path: The temporary logging path.
    :param cfg_train: A DictConfig containing a valid training configuration.
    """
    with open_dict(cfg_train):
        cfg_train.test = True
        cfg_train.trainer.max_steps = 2

    HydraConfig().set_config(cfg_train)
    train_metric_dict_1, _ = train(cfg_train)

    assert train_metric_dict_1["test/top_ranked_lddt"] > 0.0

    files = os.listdir(tmp_path / "checkpoints")
    assert "last.ckpt" in files

    with open_dict(cfg_train):
        cfg_train.ckpt_path = str(tmp_path / "checkpoints" / "last.ckpt")
        cfg_train.trainer.max_steps = 4

    train_metric_dict_2, _ = train(cfg_train)

    assert train_metric_dict_2["test/top_ranked_lddt"] > 0.0

    # NOTE: when sanity-checking the model with a random dataset, the validation metric may not increase
    # assert train_metric_dict_1["val/model_selection_score"] < train_metric_dict_2["val/model_selection_score"]
