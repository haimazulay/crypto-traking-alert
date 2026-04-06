from src import config
from src.business_logic import TrackerBusinessLogic

# Main entry point function for the application
def main():
    # Initialize the business logic component with configuration
    bl = TrackerBusinessLogic(config)
    # Execute the core run cycle
    bl.run()

# If statement to ensure script is executed directly and not imported as a module
if __name__ == "__main__":
    main()