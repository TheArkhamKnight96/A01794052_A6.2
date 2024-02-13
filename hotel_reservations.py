"""
Program created to read a file that is assumed to contain words
"""
# filename: print_numbers.py
import json
import os
import unittest


class IDShouldBeIntException(Exception):
    """A custom exception."""
    def __init__(self):
        message = "Id should be a valid integer"
        super().__init__(message)
        self.message = message


class Hotel():
    '''
    Class to store product information
    '''
    def __init__(self):
        self._hotel_id = None
        self._hotel_name = None

    @property
    def hotel_id(self):
        '''
        Method to return the hotel id
        '''
        return self._hotel_id

    @hotel_id.setter
    def hotel_id(self, value):
        try:
            int_value = int(value)
        except ValueError as exc:
            raise IDShouldBeIntException() from exc
        self._hotel_id = int_value

    @property
    def hotel_name(self):
        '''
        Method to return the hotel name
        '''
        return self._hotel_name

    @hotel_name.setter
    def hotel_name(self, value):
        self._hotel_name = value

    @staticmethod
    def from_json(json_object):
        '''
        Static factory method to map json to object
        '''
        hotel = Hotel()

        hotel.hotel_id = json_object['hotel_id']
        hotel.hotel_name = json_object['hotel_name']

        return hotel


class HotelEncoder(json.JSONEncoder):
    '''
    Encoder for the Hotel class
    '''

    def default(self, o):
        if isinstance(o, Hotel):
            return {"hotel_id": o.hotel_id, "hotel_name": o.hotel_name}
        return json.JSONEncoder.default(self, o)


class Customer():
    '''
    Class to store product information
    '''
    def __init__(self):
        self._customer_id = None
        self._customer_name = None

    @property
    def customer_id(self):
        '''
        Method to return the customer id
        '''
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value):
        try:
            int_value = int(value)
        except ValueError as exc:
            raise IDShouldBeIntException() from exc
        self._customer_id = int_value

    @property
    def customer_name(self):
        '''
        Method to return the customer name
        '''
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = value

    @staticmethod
    def from_json(json_object):
        '''
        Static factory method to map json to object
        '''
        customer = Customer()

        customer.customer_id = json_object['customer_id']
        customer.customer_name = json_object['customer_name']

        return customer


class CustomerEncoder(json.JSONEncoder):
    '''
    Encoder for the Hotel class
    '''

    def default(self, o):
        if isinstance(o, Customer):
            return {
                "customer_id": o.customer_id,
                "customer_name": o.customer_name
            }
        return json.JSONEncoder.default(self, o)


class Reservation():
    '''
    Class to store product information
    '''
    def __init__(self):
        self._hotel_id = None
        self._customer_id = None
        self._from_date = None
        self._to_date = None

    @property
    def hotel_id(self):
        '''
        Method to return the hotel id
        '''
        return self._hotel_id

    @hotel_id.setter
    def hotel_id(self, value):
        try:
            int_value = int(value)
        except ValueError as exc:
            raise IDShouldBeIntException() from exc
        self._hotel_id = int_value

    @property
    def customer_id(self):
        '''
        Method to return the customer id
        '''
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value):
        try:
            int_value = int(value)
        except ValueError as exc:
            raise IDShouldBeIntException() from exc
        self._customer_id = int_value

    @property
    def from_date(self):
        '''
        Method to return the from date for reservation
        '''
        return self._from_date

    @from_date.setter
    def from_date(self, value):
        self._from_date = value

    @property
    def to_date(self):
        '''
        Method to return the to date for reservation
        '''
        return self._to_date

    @to_date.setter
    def to_date(self, value):
        self._to_date = value

    @staticmethod
    def from_json(json_object):
        '''
        Static factory method to map json to object
        '''
        reservation = Reservation()

        reservation.hotel_id = json_object['hotel_id']
        reservation.customer_id = json_object['customer_id']
        reservation.from_date = json_object['from_date']
        reservation.to_date = json_object['to_date']

        return reservation


class ReservationEncoder(json.JSONEncoder):
    '''
    Encoder for the Hotel class
    '''

    def default(self, o):
        if isinstance(o, Reservation):
            return {"hotel_id": o.hotel_id, "customer_id": o.customer_id,
                    "from_date": o.from_date, "to_date": o.to_date}
        return json.JSONEncoder.default(self, o)


class CorruptedJsonDBException(Exception):
    """A custom exception."""
    def __init__(self, json_file_name):
        message = (
            f"DB is corrupted for file {json_file_name} "
            f"please delete the file"
        )
        super().__init__(message)
        self.message = message


class HotelNotFoundException(Exception):
    """A custom exception."""
    def __init__(self, identificator):
        message = f"Hotel not found for ID {identificator}"
        super().__init__(message)
        self.message = message


class HotelArray(list):
    """
    Custom class which extends list and
    does required computation of it's elements
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hotels_json_file_name = "hotels.json"

    @property
    def hotels_json_file_name(self):
        """
        Method to get the hotels json file name
        """
        return self._hotels_json_file_name

    @hotels_json_file_name.setter
    def hotels_json_file_name(self, value):
        self._hotels_json_file_name = value

    def create_hotel(self, hotel_name):
        """
        Create another hotel in the json file
        """
        self.clear()
        last_id = 0

        try:
            if not os.path.exists(self.hotels_json_file_name):
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
            else:
                with open(
                    self.hotels_json_file_name, 'r', encoding="utf-8"
                ) as file:
                    hotels_list_json = json.load(file)
                    if len(hotels_list_json) > 0:
                        hotel_list = list(map(
                            Hotel.from_json,
                            hotels_list_json
                        ))
                        sorted_hotel_list = sorted(
                            hotel_list,
                            key=lambda x: x.hotel_id
                        )
                        self.extend(sorted_hotel_list)
                        last_id = self[len(self) - 1].hotel_id

            hotel = Hotel()
            hotel.hotel_id = last_id + 1
            hotel.hotel_name = hotel_name
            self.append(hotel)

            with open(
                self.hotels_json_file_name, "w", encoding="utf-8"
            ) as file:
                print(json.dumps(self, cls=HotelEncoder), file=file)

            return hotel
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def delete_hotel(self, hotel_id):
        """
        Delete hotel in the json file by given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise HotelNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Hotel.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.hotel_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise HotelNotFoundException(hotel_id)

                self.clear()
                del hotel_dict[hotel_id]
                self.extend(list(hotel_dict.values()))
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
        except FileNotFoundError as exc:
            raise HotelNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def display_hotel_information(self, hotel_id):
        """
        Return hotel information for a given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise HotelNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Hotel.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.hotel_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise HotelNotFoundException(hotel_id)

                return hotel_dict.get(hotel_id)
        except FileNotFoundError as exc:
            raise HotelNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def modify_hotel_information(self, hotel_id, hotel_name):
        """
        modify hotel information for a given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise HotelNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Hotel.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.hotel_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise HotelNotFoundException(hotel_id)

                self.clear()
                hotel_obj = Hotel()
                hotel_obj.hotel_id = hotel_id
                hotel_obj.hotel_name = hotel_name
                hotel_dict[hotel_id] = hotel_obj
                self.extend(list(hotel_dict.values()))
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self, cls=HotelEncoder), file=file)

                return hotel_obj
        except FileNotFoundError as exc:
            raise HotelNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e


class CustomerNotFoundException(Exception):
    """A custom exception."""
    def __init__(self, identificator):
        message = f"Customer not found for ID {identificator}"
        super().__init__(message)
        self.message = message


class CustomerArray(list):
    """
    Custom class which extends list and
    does required computation of it's elements
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hotels_json_file_name = "customers.json"

    @property
    def hotels_json_file_name(self):
        """
        Method to get the hotels json file name
        """
        return self._hotels_json_file_name

    @hotels_json_file_name.setter
    def hotels_json_file_name(self, value):
        self._hotels_json_file_name = value

    def create_customer(self, hotel_name):
        """
        Create another hotel in the json file
        """
        self.clear()
        last_id = 0

        try:
            if not os.path.exists(self.hotels_json_file_name):
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
            else:
                with open(
                    self.hotels_json_file_name, 'r', encoding="utf-8"
                ) as file:
                    hotels_list_json = json.load(file)
                    if len(hotels_list_json) > 0:
                        hotel_list = list(map(
                            Customer.from_json, hotels_list_json
                        ))
                        sorted_hotel_list = sorted(
                            hotel_list,
                            key=lambda x: x.customer_id
                        )
                        self.extend(sorted_hotel_list)
                        last_id = self[len(self) - 1].customer_id

            hotel = Customer()
            hotel.customer_id = last_id + 1
            hotel.customer_name = hotel_name
            self.append(hotel)

            with open(
                self.hotels_json_file_name, "w", encoding="utf-8"
            ) as file:
                print(json.dumps(self, cls=CustomerEncoder), file=file)

            return hotel
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def delete_customer(self, hotel_id):
        """
        Delete hotel in the json file by given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise CustomerNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Customer.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.customer_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise CustomerNotFoundException(hotel_id)

                self.clear()
                del hotel_dict[hotel_id]
                self.extend(list(hotel_dict.values()))
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
        except FileNotFoundError as exc:
            raise CustomerNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def display_customer_information(self, hotel_id):
        """
        Return hotel information for a given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise CustomerNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Customer.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.customer_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise CustomerNotFoundException(hotel_id)

                return hotel_dict.get(hotel_id)
        except FileNotFoundError as exc:
            raise CustomerNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def modify_customer_information(self, hotel_id, hotel_name):
        """
        modify hotel information for a given id
        Throws custom exception if no hotel found by given id
        """
        try:
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise CustomerNotFoundException(hotel_id)

                self.clear()
                hotel_list = list(map(Customer.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict((hotel.customer_id, hotel) for hotel in self)
                if hotel_id not in hotel_dict:
                    raise CustomerNotFoundException(hotel_id)

                self.clear()
                hotel_obj = Customer()
                hotel_obj.customer_id = hotel_id
                hotel_obj.customer_name = hotel_name
                hotel_dict[hotel_id] = hotel_obj
                self.extend(list(hotel_dict.values()))
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self, cls=CustomerEncoder), file=file)

                return hotel_obj
        except FileNotFoundError as exc:
            raise CustomerNotFoundException(hotel_id) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e


class InvalidHotelArrayParamException(Exception):
    """A custom exception."""
    def __init__(self):
        message = "Please provide a valid hotel array in the params"
        super().__init__(message)
        self.message = message


class InvalidCustomerArrayParamException(Exception):
    """A custom exception."""
    def __init__(self):
        message = "Please provide a valid customer array in the params"
        super().__init__(message)
        self.message = message


class InvalidHotelForReservException(Exception):
    """A custom exception."""
    def __init__(self, hotel_id):
        message = (
            f"Hotel id {hotel_id}, "
            f"please provide a valid hotel id for the reservation"
        )
        super().__init__(message)
        self.message = message


class InvalidCustomerForReservException(Exception):
    """A custom exception."""
    def __init__(self, hotel_id):
        message = (
            f"Customer id {hotel_id}, "
            f"please provide a valid customer id for the reservation"
        )
        super().__init__(message)
        self.message = message


class ReservationNotFoundException(Exception):
    """A custom exception."""
    def __init__(self, identificator):
        message = f"Reservation not found for ID {identificator}"
        super().__init__(message)
        self.message = message


class ReservationArray(list):
    """
    Custom class which extends list and
    does required computation of it's elements
    """
    def __init__(self, hotel_array, customer_array, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(hotel_array, HotelArray):
            raise InvalidHotelArrayParamException()
        if not isinstance(customer_array, CustomerArray):
            raise InvalidCustomerArrayParamException()

        self.hotel_array = hotel_array
        self.customer_array = customer_array
        self._hotels_json_file_name = "reservations.json"

    @property
    def hotels_json_file_name(self):
        """
        Method to get the hotels json file name
        """
        return self._hotels_json_file_name

    @hotels_json_file_name.setter
    def hotels_json_file_name(self, value):
        self._hotels_json_file_name = value

    def create_reservation(self, hotel_id, customer_id, from_date, to_date):
        """
        Create another hotel in the json file
        """
        self.clear()

        try:
            if not os.path.exists(self.hotels_json_file_name):
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
            else:
                with open(
                    self.hotels_json_file_name, 'r', encoding="utf-8"
                ) as file:
                    hotels_list_json = json.load(file)
                    if len(hotels_list_json) > 0:
                        hotel_list = list(map(
                            Reservation.from_json,
                            hotels_list_json
                        ))
                        sorted_hotel_list = sorted(
                            hotel_list,
                            key=lambda x: x.hotel_id
                        )
                        self.extend(sorted_hotel_list)
            try:
                self.hotel_array.display_hotel_information(hotel_id)
            except HotelNotFoundException as ex:
                raise InvalidHotelForReservException(hotel_id) from ex
            try:
                self.customer_array.display_customer_information(customer_id)
            except HotelNotFoundException as ex:
                raise InvalidCustomerForReservException(hotel_id) from ex

            hotel = Reservation()
            hotel.hotel_id = hotel_id
            hotel.customer_id = customer_id
            hotel.from_date = from_date
            hotel.to_date = to_date
            self.append(hotel)

            with open(
                self.hotels_json_file_name, "w", encoding="utf-8"
            ) as file:
                print(json.dumps(self, cls=ReservationEncoder), file=file)

            return hotel
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e

    def cancel_reservation(self, hotel_id, customer_id, from_date, to_date):
        """
        Delete hotel in the json file by given id
        Throws custom exception if no hotel found by given id
        """
        try:
            reservation_composite_key = (
                f"{hotel_id}_{customer_id}_"
                f"{from_date}_{to_date}"
            )
            with open(
                self.hotels_json_file_name, 'r', encoding="utf-8"
            ) as file:
                hotels_list_json = json.load(file)
                if len(hotels_list_json) == 0:
                    raise ReservationNotFoundException(
                        reservation_composite_key
                    )

                self.clear()
                hotel_list = list(map(Reservation.from_json, hotels_list_json))
                self.extend(hotel_list)
                hotel_dict = dict(
                    (
                        (
                            f"{hotel.hotel_id}_{hotel.customer_id}_"
                            f"{hotel.from_date}_{hotel.to_date}"
                        ),
                        hotel
                    ) for hotel in self
                )
                if reservation_composite_key not in hotel_dict:
                    raise ReservationNotFoundException(
                        reservation_composite_key
                    )

                self.clear()
                del hotel_dict[reservation_composite_key]
                self.extend(list(hotel_dict.values()))
                with open(
                    self.hotels_json_file_name, "w", encoding="utf-8"
                ) as file:
                    print(json.dumps(self), file=file)
        except FileNotFoundError as exc:
            raise ReservationNotFoundException(
                reservation_composite_key
            ) from exc
        except json.JSONDecodeError as e:
            raise CorruptedJsonDBException(self.hotels_json_file_name) from e


class TestStringMethods(unittest.TestCase):
    '''
    Class to test all of the classes above declared
    '''

    def setUp(self):
        self.hotel_array = HotelArray()
        if os.path.exists(self.hotel_array.hotels_json_file_name):
            # Delete the file
            os.remove(self.hotel_array.hotels_json_file_name)
        else:
            print("File does not exist")
        self.customer_array = CustomerArray()
        if os.path.exists(self.customer_array.hotels_json_file_name):
            # Delete the file
            os.remove(self.customer_array.hotels_json_file_name)
        else:
            print("File does not exist")
        self.reservations_array = ReservationArray(
            self.hotel_array, self.customer_array
        )
        if os.path.exists(self.reservations_array.hotels_json_file_name):
            # Delete the file
            os.remove(self.reservations_array.hotels_json_file_name)
        else:
            print("File does not exist")

    def test_create_hotel(self):
        '''
        Test if create hotel works
        '''
        result = self.hotel_array.create_hotel("Transilvania")
        self.assertEqual(isinstance(result, Hotel), True,
                         'wrong instance of variable')

    def test_create_hotel_json_exists(self):
        '''
        Test if create hotel works
        '''
        self.hotel_array.create_hotel("Transilvania")
        self.hotel_array.create_hotel("Luigi's mansion")
        self.assertEqual(len(self.hotel_array), 2,
                         'wrong instance of variable')

    def test_delete_hotel(self):
        '''
        Test if create hotel works
        '''
        passed = True
        try:
            self.hotel_array.create_hotel("Transilvania")
            self.hotel_array.delete_hotel(1)
        except HotelNotFoundException:
            passed = False

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_delete_hotel_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.hotel_array.create_hotel("Transilvania")
            self.hotel_array.delete_hotel(2)
        except HotelNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_display_hotel(self):
        '''
        Test if create hotel works
        '''
        self.hotel_array.create_hotel("Transilvania")
        result = self.hotel_array.display_hotel_information(1)
        self.assertEqual(isinstance(result, Hotel), True,
                         'wrong instance of variable')
        self.assertEqual(result.hotel_name, 'Transilvania',
                         'wrong instance of variable')

    def test_display_hotel_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.hotel_array.create_hotel("Transilvania")
            self.hotel_array.display_hotel_information(2)
        except HotelNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_modify_hotel(self):
        '''
        Test if create hotel works
        '''
        self.hotel_array.create_hotel("Transilvania")
        result = self.hotel_array.modify_hotel_information(
            1, "Caesar's Palace"
        )
        self.assertEqual(isinstance(result, Hotel), True,
                         'wrong instance of variable')
        self.assertEqual(result.hotel_id, 1,
                         'wrong instance of variable')
        self.assertEqual(result.hotel_name, "Caesar's Palace",
                         'wrong instance of variable')

    def test_modify_hotel_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.hotel_array.create_hotel("Transilvania")
            self.hotel_array.modify_hotel_information(2, "Caesar's Palace")
        except HotelNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_create_customer(self):
        '''
        Test if create hotel works
        '''
        result = self.customer_array.create_customer("Elvis")
        self.assertEqual(isinstance(result, Customer), True,
                         'wrong instance of variable')

    def test_create_customer_json_exists(self):
        '''
        Test if create hotel works
        '''
        self.customer_array.create_customer("Elvis")
        self.customer_array.create_customer("Frank")
        self.assertEqual(len(self.customer_array), 2,
                         'wrong instance of variable')

    def test_delete_customer(self):
        '''
        Test if create hotel works
        '''
        passed = True
        try:
            self.customer_array.create_customer("Elvis")
            self.customer_array.delete_customer(1)
        except CustomerNotFoundException:
            passed = False

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_delete_customer_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.customer_array.create_customer("Elvis")
            self.customer_array.delete_customer(2)
        except CustomerNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_display_customer(self):
        '''
        Test if create hotel works
        '''
        self.customer_array.create_customer("Elvis")
        result = self.customer_array.display_customer_information(1)
        self.assertEqual(isinstance(result, Customer), True,
                         'wrong instance of variable')
        self.assertEqual(result.customer_name, 'Elvis',
                         'wrong instance of variable')

    def test_display_customer_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.customer_array.create_customer("Elvis")
            self.customer_array.display_customer_information(2)
        except CustomerNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_modify_customer(self):
        '''
        Test if create hotel works
        '''
        self.customer_array.create_customer("Elvis")
        result = self.customer_array.modify_customer_information(
            1, "Elvis Presley"
        )
        self.assertEqual(isinstance(result, Customer), True,
                         'wrong instance of variable')
        self.assertEqual(result.customer_id, 1,
                         'wrong instance of variable')
        self.assertEqual(result.customer_name, "Elvis Presley",
                         'wrong instance of variable')

    def test_modify_customer_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            self.customer_array.create_customer("Elvis")
            self.customer_array.modify_customer_information(2, "Elvis Presley")
        except CustomerNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_create_reservation(self):
        '''
        Test if create hotel works
        '''
        created_hotel = self.hotel_array.create_hotel("Caesar's Palace")
        created_customer = self.customer_array.create_customer("Elvis")
        result = self.reservations_array.create_reservation(
            created_hotel.hotel_id, created_customer.customer_id,
            "2024-11-02", "2024-11-03"
        )
        self.assertEqual(isinstance(result, Reservation), True,
                         'wrong instance of variable')

    def test_create_reservation_json_exists(self):
        '''
        Test if create hotel works
        '''
        created_hotel = self.hotel_array.create_hotel("Caesar's Palace")
        created_customer = self.customer_array.create_customer("Elvis")
        self.reservations_array.create_reservation(
            created_hotel.hotel_id, created_customer.customer_id,
            "2024-11-02", "2024-11-03"
        )
        self.reservations_array.create_reservation(
            created_hotel.hotel_id, created_customer.customer_id,
            "2024-11-03", "2024-11-04"
        )
        self.assertEqual(len(self.reservations_array), 2,
                         'wrong instance of variable')

    def test_cancel_reservation(self):
        '''
        Test if create hotel works
        '''
        passed = True
        try:
            created_hotel = self.hotel_array.create_hotel("Caesar's Palace")
            created_customer = self.customer_array.create_customer("Elvis")
            result = self.reservations_array.create_reservation(
                created_hotel.hotel_id, created_customer.customer_id,
                "2024-11-02", "2024-11-03"
            )
            self.reservations_array.cancel_reservation(
                result.hotel_id, result.customer_id,
                result.from_date, result.to_date
            )
        except ReservationNotFoundException:
            passed = False

        self.assertEqual(passed, True,
                         'unkown exception thrown')

    def test_cancel_reservation_fail(self):
        '''
        Test if custom exception is triggered
        '''
        passed = False
        try:
            created_hotel = self.hotel_array.create_hotel("Caesar's Palace")
            created_customer = self.customer_array.create_customer("Elvis")
            result = self.reservations_array.create_reservation(
                created_hotel.hotel_id, created_customer.customer_id,
                "2024-11-02", "2024-11-03"
            )
            self.reservations_array.cancel_reservation(
                2, result.customer_id, result.from_date, result.to_date
            )
        except ReservationNotFoundException:
            passed = True

        self.assertEqual(passed, True,
                         'unkown exception thrown')


if __name__ == '__main__':
    unittest.main()
