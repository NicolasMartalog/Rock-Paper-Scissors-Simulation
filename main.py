import constants
from model import Model
from ViewController import ViewController

def main() -> None: 
    model = Model(constants.CELL_COUNT, constants.CELL_SPEED)
    vc = ViewController(model)
    vc.start_simulation()

if __name__ == "__main__": 
    main()