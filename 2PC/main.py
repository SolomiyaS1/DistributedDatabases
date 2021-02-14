from datetime import datetime
from booking_service import BookingService, TravelDetails

def get_input_data():
    pass



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    journey = TravelDetails()
    booking = BookingService()
    booking.book_flight(journey)