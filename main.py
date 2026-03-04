import multiprocessing
from ui.app_window import AppWindow

if __name__ == "__main__":
    # when running multiprocessing in a compiled Windows .exe file
    multiprocessing.freeze_support()
    
    # Initialize and launch the graphical user interface
    app = AppWindow()
    app.run()