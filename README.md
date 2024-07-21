# Hotel Deal Finder Bot

This project is a Selenium-based bot that helps you find the best hotel deals based on your preferences. The bot allows you to set the currency, handle any pop-ups, enter the destination, check-in and check-out dates, the number of persons, and the number of rooms. It filters the results based on the specified star ratings and sorts them by the lowest price first. The results are then displayed in a table in the terminal.

## Features

- Set the currency for the search.
- Handle any pop-ups that may appear during the search.
- Enter the destination, check-in and check-out dates, number of persons, and number of rooms.
- Apply filters to show hotels with specific star ratings (e.g., 3, 4, or 5 stars).
- Sort the results by the lowest price first.
- Display the results in the terminal in a tabular form.

## Technologies Used

- **Python**: The programming language used for this project.
- **Selenium**: A browser automation tool used to interact with web elements.
- **PrettyTable**: For representing the data in a tabular form.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/deepankchauhan99/selenium-bestdealbot.git
    cd selenium-bestdealbot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your constants in `constants.py`:
    ```python
    # Example
    BASE_URL = "https://www.booking.com"
    CURRENCY = "USD"
    PLACE_TO_GO = "Goa"
    CHECK_IN_DATE = "2024-07-27"
    CHECK_OUT_DATE = "2024-07-29"
    ADULTS = 2
    CHILDREN = {1: 10, 2: 5} # Provide key-value pair of child: age or simply write 0 if no children 
    ROOMS = 2
    STARS = [3, 4, 5]
    ```

## Usage

1. Run the bot:
    ```sh
    python run.py
    ```

2. The bot will open a browser window and start interacting with the hotel booking site, applying the specified filters, and retrieving the results.

3. The results will be displayed in a table in the terminal, showing the best deals based on the criteria provided.

## Project Structure

- `run.py`: The main script to run the bot.
- `constants.py`: A file to store constant values and inputs.
- `booking.py`: Contains individual functions to handle specific tasks such as setting currency, handling pop-ups, entering search details, applying filters, and sorting results.
- `booking_filtration.py` and `booking_report.py`: Helper functions for filtration and report generation.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Selenium](https://www.selenium.dev/) for browser automation.
- [PrettyTable](https://pypi.org/project/prettytable/) for representing results in tabular form.

---

*Happy hotel hunting!*
