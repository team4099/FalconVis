# Contributing to FalconVis

## Infrastructure
FalconVis uses Python and Streamlit to host  the app. Streamlit is a framework used to create and host data science apps, the documentation for Streamlit can be found [here](https://docs.streamlit.io). Before contributing, it's recommended that you play around with Streamlit & read its docs in order to get a feel for it.

## Cloning the Repository
In the folder you want to clone the repository in, run `git clone https://github.com/team4099/FalconVis.git`.


## Installing Dependencies
In order to install the dependencies, you must be in the `src` directory. Then, you can run `python -m pip install -r requirements.txt`.


## Style Guide
The code below shows generally what the style guide is, specifically with writing functions. If you have no parameters or returns, you can remove their corresponding section in the function's docstring.
Remember to follow this when following your code (FalconVis uses Sphinx docstrings).
```py
def function_name(parameter: parameter_type) -> return_type:
  """Explanation of what this function does.

  :param parameter: Explanation of the parameter.
  :return: Explanation of what the function returns.
  """
  ```

## File Structure
For FalconVis, there are four pages — Teams, Match, Event, and Picklist. Each page has a page manager found in `page_managers/[page name]_manager.py`, where the page generating happens. 

Utility functions like retrieving the current scouting data can be found in `utils/functions.py`.

Constants like when to delete the cached scouting data, event code, etc. are found in `utils/constants.py`

The `pages` directory contains the Match, Event and Picklist pages. `Teams.py` is located outside the directory due to being the entrypoint to the app. Your app should be run with this file, and an entrypoint file means that the app opens on this page and is the "main" page:

## Running the Streamlit App Locally
In order to run the Streamlit app locally, make sure you're in the `src` directory, then run `python -m streamlit run Teams.py`
