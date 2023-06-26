# Dusseldorf-stammdaten
Program to get base data information from Dusseldorf based on portfolio of ISINs requested






### Learning from this program, references used
use the GoogleTranslator from the deep_translator to translate value in dictionary
from deep_translator import GoogleTranslator
translated_value = GoogleTranslator(source='auto', target='en').translate(value)

To handle the KeyError when a field is missing in the stammdaten dictionary, 
you can use the get() method to retrieve the values with a default fallback value of "N/A".
