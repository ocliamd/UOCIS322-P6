# UOCIS322 - Project 6 #
Brevet time calculator with AJAX, MongoDB, and a RESTful API!

# Functionality
The algorithm uses the French calculation for KM 0-60, each brevet has the same open and close time as well as up to 20% past. Each specific brevet has a unique max, these are in hours and minutes: HH:MM 3:30 for 200 KM, 20:00 for 300 KM, 27:00 for 400 KM, 40:00 for 600 KM, and 75:00 for 1000 KM. Each of the starting times is relative to the previous starting times, and this is the same for the to the closing times.

The program now accepts valid inputs into a database. If the user attempts to submit an invalid value nothing will be added to the data base, and an error message will be pop up on the user's screen. If the user displays from an empty database another error will be popped up on the users screen.

This program also now has a RESTful api service which allows the user to choose what parts of the input data will be returned back to them via a new webpage.

docker-compose.yml file runs 3 separate containers as well as the MongoDB database.

If the top "k" value is out of range of the top times it displays all of the inputted times. This will include bothnegative and positive values. If k = 0 it displays nothing for all api access's.

## Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.
