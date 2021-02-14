import psycopg2
from utils import load_config
from datetime import datetime


class TravelDetails:
    def __init__(self):
        print('enter client name: ')
        self.client_name = input()
        print('enter flight number: ')
        self.flight_number = input()
        print('enter airport from: ')
        self.airport_from = input()
        print('enter airport to: ')
        self.airport_to = input()
        self.date = datetime.now()
        print('enter hotel name: ')
        self.hotel_name = input()
        print('enter arrival YYYY-MM-DD')
        self.arrival_str = input()
        self.arrival = datetime.strptime(self.arrival_str, '%Y-%m-%d')
        #self.arrival = self.arrival_str
        print('enter departure YYYY-MM-DD')
        self.departure_str = input()
        self.departure = datetime.strptime(self.departure_str, '%Y-%m-%d')
        print('enter price')
        self.price = input()
        #self.departure = self.departure_str

class BookingService:
    def __init__(self):
        config = load_config()
        self._flight_db_connection = psycopg2.connect(config["flight_db_connection"])
        self._hotel_db_connection = psycopg2.connect(config["hotel_db_connection"])
        self._account_db_connection = psycopg2.connect(config["account_db_connection"])
        self.insert_flight_query = '''
                                insert into flightbooking(ClientName, FlightNumber, "From", "To", "Date")
                                values (%s, %s, %s, %s, %s)
                            '''
        self.insert_hotel_query = '''
                                insert into hotelbooking(ClientName, HotelName, Arrival, Departure)
                                values (%s, %s, %s, %s)
                            '''
        self.update_account_query = ''' 
                                    update account
                                    set Amount = Amount - %s
                                    where ClientName = %s
                                    '''
        self.query_connection = {
            self._flight_db_connection: self.insert_flight_query
            , self._hotel_db_connection: self.insert_hotel_query
            , self._account_db_connection: self.update_account_query
        }
        self.xid = {
            self._flight_db_connection: 'flight'
            , self._hotel_db_connection: 'hotel'
            , self._account_db_connection: 'account'
        }

    def book_flight(self, journey):

        flight = (journey.client_name, journey.flight_number, journey.airport_from, journey.airport_to, journey.date)
        hotel = (journey.client_name, journey.hotel_name, journey.arrival, journey.departure)
        account = (journey.price, journey.client_name)

        for connection in self.query_connection:
            #xid = connection.xid(1, "gtrid", "bqual")
            #print(xid)
            print(self.xid[connection])
            connection.tpc_begin(self.xid[connection])

        try:

            for connection, query in self.query_connection.items():
                cursor = connection.cursor()
                if 'flight' in query:
                    print(query)
                    print(flight)
                    cursor.execute(query, flight)
                elif 'account'in query:
                    print(query)
                    cursor.execute(query, account)
                else:
                    print(query)
                    print(hotel)
                    cursor.execute(query, hotel)

            for connection in self.query_connection:
                connection.tpc_prepare()

            for connection in self.query_connection:
                connection.tpc_commit()

        except Exception as e:
            for connection in self.query_connection:
                connection.tpc_rollback()
                print('rolled back ' + str(connection))
            print(e)

