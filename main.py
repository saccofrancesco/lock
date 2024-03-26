# Importing the App component
from components.app import App

# Instance of the App object
title: str = 'Lock'
size: tuple = (500, 425)
APP = App(title, size)

# Running the App
APP.run()