from src import config
from src.business_logic import TrackerBusinessLogic

def main():
    bl = TrackerBusinessLogic(config)
    bl.run()

if __name__ == "__main__":
    main()