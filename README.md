# DoctolibNotifier
DoctolibNotifier is a Python package that automates checking for available appointment slots on the German Doctolib and notifies the user when slots are found. It leverages the [Nodriver package](https://github.com/ultrafunkamsterdam/nodriver/) for browser automation and data retrieval.

## How it works
The `DoctolibNotifier` script automates checking for available appointment slots on Doctolib. It takes a Doctolib URL, parses it to extract query parameters, and builds a query string to fetch availability data. The script checks for available slots every 60 seconds. If slots within 15 days of today are found, it sounds a notification and prints the available dates to the console. If there are slots available beyond 15 days, it provides information on the next available slot.


## Usage

The authors recommend using Python 3.11. Follow these steps:

1. **Install Poetry**: If you don't have Poetry installed, you can install it by following the [Poetry installation guide](https://python-poetry.org/docs/#installation).
2. **Navigate to the Project's Root Directory**: Open a terminal and navigate to the root directory of the project.
3. **Install Dependencies**: Run the following command to install all dependencies:
    ```
    poetry install
    ```

4. **Grab the the Doctolib URL**: Navigate to the final appointments page and copy the url:
![grafik](https://github.com/user-attachments/assets/2f47a0a8-1d56-4e84-82f6-0b3fdd6a7a56)



5. **Start the Program**:
    ```
    poetry run python main.py your_doctolib_url_here
    ```
