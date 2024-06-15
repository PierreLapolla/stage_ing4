from lightning.pytorch import seed_everything

from src.config import config
from src.helpers.decorators import timer
from src.helpers.menu import Menu
from src.model_training.lightning_manager import lightning_manager
from src.preprocessing.data_creation import create_csv_files
from src.preprocessing.sequencer import sequence
from src.preprocessing.visualizer import visualize


@timer
def main() -> None:
    seed_everything(config.seed, workers=True)
    Menu({
        "1": ("Create CSV files", create_csv_files),
        "2": ("Visualize speed", visualize),
        "3": ("Create sequences", sequence),
        "4": ("Train model", lightning_manager.train_model)
    }).start(timeout=10)


if __name__ == '__main__':
    main()
