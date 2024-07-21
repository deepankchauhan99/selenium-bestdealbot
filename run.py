from booking.booking import Booking
import booking.constants as const

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.close_popup()
        bot.change_currency(currency=const.CURRENCY)
        bot.select_place_to_go(place_to_go=const.PLACE_TO_GO)
        bot.select_dates(check_in_date=const.CHECK_IN_DATE, check_out_date=const.CHECK_OUT_DATE)
        bot.select_persons(const.ADULTS, const.CHILDREN, const.ROOMS)
        bot.apply_filtration()
        bot.refresh()
        bot.report_results()
        print("Exiting...")

# Handling exception caused if the Selenium driver is not present on PATH
except Exception as e:
    if 'in PATH' in str(e):
        print('''You are trying to run the bot from command line
        Please add to PATH your Selenium Drivers
        Windows:
            set PATH=%PATH%;C:path-to-your-folder \n
        Linux:
            PATH=$PATH:/path/to/your/folder/''')
    else:
        raise
