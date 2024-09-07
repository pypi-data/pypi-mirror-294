from typing import List, Union
from math import floor

class hex_functions : 
    """
    Sujestion, import as hf. 
    A class for working with hexadecimal numbers
    There is no need to create instances off this class. 

    Attributes : 
        This class dont have attributes 

    Functions : 
        hex_sum(value : int, hex_len : int)  : 
            The value will be used in the equation with the hex_len to return the result 
            returns : 
                One int value result of the equatiion.
        
        alpha_to_hex(values : str) : 
            convert alphabetical characters (A...F) in hexadecimal values 
            returns : 
                A list with the corresponding values of the characters in int. 

        to_dec(values : str) :
            convert hexl / hexadecimal format to decimal
            return the real sum of entire hexadecimal string

        dec_hex_equation(values : Union[str, int]) : 
            Convert int or string hexadecimal to decimal, 
            using standard hex to dec equation

            returns : 
                List of integers

        dec_to_hex(values : List[int]) : 
            Use list of integers to create a new hexl / hexadecimal value

            returns : 
                Hexel instance
    """

    @staticmethod 
    def hex_sum(value : int, hex_len : int) -> int: 
        """
        Uses value (0 - 9) digits an hex_len to convert to decimal 
        using | value *  ^ hex_len | equation.

        Args : 
            Value (int) : Principal value that will be used in the equation
            hex_len (int) : value that will be used to determine the power in equation.

        Returns : 
            Real decimal value of the number. 
        """
        result = value * 16 ** hex_len 

        return result 

    @staticmethod
    def alpha_to_hex(values : str) -> List[int] : 
        """
        Convert alphabetic type to int type 

        Args : 
            values (str) : string, can contain numbers and letters, only letters will be converted.
        
        Returns :  
            List[int] with the new values. 
        """
        inverse_hex_map = {
           "F": "15",
           "E": "14",
           "D": "13",
           "C": "12",
           "B": "11",
           "A": "10" 
    }

        HEX_LIST: List[str] = []

        for i in values.upper() : 
            HEX_LIST.append(i)

        HEX_LIST = [inverse_hex_map.get(var,var) for var in HEX_LIST]


        HEX_LIST = [int(var) for var in HEX_LIST]

        return HEX_LIST

    @staticmethod
    def to_dec(values : str) -> int : 
        """
        Return the real sum of entire Hexadecimal string. 

        Args : 
            Values (str) : recive a str that contains the hexadecimal.

        Returns : 
            The sum of values (Hexadecimal) casted as int. 
        """

        if isinstance(values, int) : 
            pass 

        hex_id = []
        hex_id_len = len(values)

        for i in values :  
            hex_id_len -= 1 
            if i.isalpha() and i.upper() in ["A", "B", "C", "D", "E", "F"]: 

                holder = hex_functions.alpha_to_hex(i)
                hex_id.append(hex_functions.hex_sum(int(holder[0]), hex_id_len))


            elif i.isdigit() : 
                hex_id.append(hex_functions.hex_sum(int(i), hex_id_len))

            else : 
                raise TypeError(f"Invalid value : {i}")
            
        return sum(hex_id)

    @staticmethod
    def dec_hex_equation(values: Union[str, int]) -> List[int]:
        """ 
        Converts a decimal number into a list of integers representing each digit of the hexadecimal value.

        Args:
            values (str, int): The decimal number as a string or integer.

        Returns:
            List[int]: A list of integers representing the hexadecimal digits.
        """
        leftover = []

        if isinstance(values, str):
            try:
                values = int(values)
            except ValueError:
                raise ValueError(f"Invalid hexadecimal value: {values}")

        # Handle case where the value is 0
        if values == 0:
            leftover.append(0)

        while values > 0:
            mod = values % 16 
            leftover.append(mod)  # No need to floor, mod is already an integer
            values //= 16  

        leftover.reverse()  # Reverse the list to get the correct order

        return leftover

    @staticmethod
    def dec_to_hex(values: List[int]) -> str:
        """
        Converts a list of integers representing hex digits into a hexadecimal string.

        Args:
            values (List[int]): A list of integers representing hex digits.

        Returns:
            str: A string representing the hexadecimal value.
        """
        hex_map = {
            15: "F",
            14: "E",
            13: "D",
            12: "C",
            11: "B",
            10: "A"
        }

        values = [hex_map.get(var, str(var)) for var in values]

        return ''.join(values)
