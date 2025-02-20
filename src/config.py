from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError


class AccessibilityConfig(BaseModel):
    query_radius: int = 500
    random_max: float = 0.5
    minimum_speed: float = 0
    maximum_speed: float = 4
    score_multiplier: float = 1


class SequencerConfig(BaseModel):
    crafted_path: str = 'data/crafted'
    sequences_path: str = 'data/sequences'
    train_ratio: float = 0.8
    sequence_length: int = 12
    time_of_day: bool = True
    day_of_week: bool = True


class WandbConfig(BaseModel):
    # api_key is handled in .env file, wandb automatically log if it is set
    project: str = 'StageING4'
    entity: str = 'deldrel'


class DataModuleConfig(BaseModel):
    batch_size: int = 32
    num_workers: int = 8
    persistent_workers: bool = True


class ModelConfig(BaseModel):
    in_channels: int = 4
    hidden_channels: int = 64
    out_channels: int = 4
    learning_rate: float = 0.001
    loss_function: str = 'mse_loss'
    optimizer: str = 'Adam'


class TrainerConfig(BaseModel):
    max_epochs: int = 50
    log: bool = True
    save_dir: str = 'logs/models'
    test_every_n_epochs: int = 5


class CheckpointConfig(BaseModel):
    dirpath: str = 'logs/checkpoints'
    filename: str = 'checkpoint-{epoch:02d}-{val_loss:.6f}'
    monitor: str = 'val_loss'
    verbose: bool = True
    save_last: bool = True
    save_top_k: int = 1
    mode: str = 'min'


class EarlyStoppingConfig(BaseModel):
    monitor: str = 'val_loss'
    min_delta: float = 0.0001
    patience: int = 10  # 10
    verbose: bool = True
    mode: str = 'min'


class ReduceLROnPlateauConfig(BaseModel):
    monitor: str = 'val_loss'
    factor: float = 0.1
    patience: int = 5  # 5
    verbose: bool = True
    mode: str = 'min'


class Config(BaseModel):
    seed: int = 42
    logdir: str = 'logs'
    verbose: bool = True

    accessibility: AccessibilityConfig = AccessibilityConfig()
    sequencer: SequencerConfig = SequencerConfig()
    wandb: WandbConfig = WandbConfig()
    data_module: DataModuleConfig = DataModuleConfig()
    model: ModelConfig = ModelConfig()
    trainer: TrainerConfig = TrainerConfig()
    checkpoint: CheckpointConfig = CheckpointConfig()
    early_stopping: EarlyStoppingConfig = EarlyStoppingConfig()
    reduce_lr_on_plateau: ReduceLROnPlateauConfig = ReduceLROnPlateauConfig()

    def dump(self):
        return self.model_dump()


@lru_cache(maxsize=1)
def get_config() -> Config:
    try:
        if not load_dotenv(verbose=True):
            raise ValidationError('No .env variable set')
        return Config()
    except ValidationError as e:
        print(e)
        exit(1)


config: Config = get_config()
