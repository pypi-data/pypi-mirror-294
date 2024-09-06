from html.parser import HTMLParser
import base64
from copy import deepcopy
import time

# Install
import requests
import pandas as pd
import matplotlib.pyplot as plt

class CPIHTMLTableParser(HTMLParser):
    """
    A specialized HTML parser for extracting Consumer Price Index (CPI) data from an HTML table.

    Attributes:
        url (str): The URL of the webpage containing the CPI data table, encoded in base64.
        in_table (bool): Indicates if the parser is currently within an HTML table.
        in_row (bool): Indicates if the parser is currently within a row of an HTML table.
        in_cell (bool): Indicates if the parser is currently within a cell of an HTML table.
        table_data (list): A list to store the parsed table data.
        current_row (list): A list to store data for the current row being parsed.
        current_cell (str): A string to store data for the current cell being parsed.
        data_frame (pd.DataFrame): A pandas DataFrame to store the parsed table data.
    """
    def __init__(self, url='aHR0cHM6Ly93d3cudXNpbmZsYXRpb25jYWxjdWxhdG9yLmNvbS9pbmZsYXRpb24vY29uc3VtZXItcHJpY2UtaW5kZXgtYW5kLWFubnVhbC1wZXJjZW50LWNoYW5nZXMtZnJvbS0xOTEzLXRvLTIwMDgv'):
        """
        Initializes the CPIHTMLTableParser with a URL to the CPI data table.

        Args:
            url (str): The URL of the webpage containing the CPI data table, encoded in base64.
        """
        super().__init__()
        self.url = base64.b64decode(url).decode('utf-8')
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.table_data = []
        self.current_row = []
        self.current_cell = ''
        self.data_frame = None
        self.request_successful = False
        self.data_fetched = False

    def handle_starttag(self, tag, attrs):
        """
        Handles the start tags of the HTML elements.

        Args:
            tag (str): The name of the HTML tag.
            attrs (list): A list of attribute-value pairs for the tag.
        """
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag == 'td' and self.in_row:
            self.in_cell = True

    def handle_endtag(self, tag):
        """
        Handles the end tags of the HTML elements.

        Args:
            tag (str): The name of the HTML tag.
        """
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_table:
            self.in_row = False
            self.table_data.append(self.current_row)
        elif tag == 'td' and self.in_row:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ''

    def handle_data(self, data):
        """
        Handles the data within the HTML elements.

        Args:
            data (str): The data within the HTML element.
        """
        if self.in_cell:
            self.current_cell += data

    def fetch_data(self):
        """
        Fetches the HTML table data from the given URL.

        Returns:
            str: The HTML content of the webpage.
        """
        if self.data_fetched:
            print("Data has already been fetched and validated.")
            return
        
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.request_successful = True
            self.parse_data(response.text)
        except requests.RequestException as e:
            self.request_successful = False
            print(f"Failed to fetch data: {e}")
        
    def parse_data(self, html):
        """
        Parses the HTML table data.

        Args:
            html (str): The HTML content of the webpage.
        """
        if self.request_successful:
            self.feed(html)
            self.create_data_frame()
            self.validate_data_frame()       

    def create_data_frame(self):
        """
        Converts the parsed table data into a pandas DataFrame.
        """
        if len(self.table_data) > 1:
            columns = self.table_data[1]
            table_data = [row[:len(columns)] for row in self.table_data[2:]]
            self.data_frame = pd.DataFrame(table_data, columns=columns)
            self.data_frame = self.data_frame.drop(columns=['Dec-Dec', 'Avg-Avg'], errors='ignore')

    def validate_data_frame(self):
        """
        Validates the parsed data frame to ensure it meets the required criteria.
        """
        required_columns = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Avg']
        current_year = time.localtime().tm_year

        if not all(column in self.data_frame.columns for column in required_columns):
            print("Data frame does not contain all required columns.")
            self.data_frame = None
            return

        last_two_years = self.data_frame['Year'].tail(2).astype(int)
        if not ((last_two_years.iloc[0] == current_year - 1 and last_two_years.iloc[1] == current_year) or 
                (last_two_years.iloc[0] == current_year and last_two_years.iloc[1] == current_year + 1)):
            print("Last two years in the data frame do not match the expected years.")
            self.data_frame = None
            return
        self.data_fetched = True

    def get_data_frame(self):
        """
        Returns the parsed data as a pandas DataFrame.

        Returns:
            pd.DataFrame: The parsed CPI data.
        """
        return self.data_frame



class CPIDataTool:
    """
    A tool for processing and analyzing Consumer Price Index (CPI) data.

    Attributes:
        df (pd.DataFrame): The dataframe containing the CPI data.
        current_month (str): The current month.
        current_year (int): The current year.
        month_map (dict): A mapping from full month names to their abbreviations.
    """
    def __init__(self, dataframe):
        """
        Initializes the CPIDataTool with a dataframe.

        Args:
            dataframe (pd.DataFrame): The dataframe containing the CPI data.
        """
        self.df = deepcopy(dataframe)
        self.current_month = time.strftime("%B")
        self.current_year = time.localtime().tm_year
        self.month_map = {
            'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
            'May': 'May', 'June': 'June', 'July': 'July', 'August': 'Aug',
            'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
        }
        self.convert_columns_to_float()
        self.calculate_avg_for_nan()
        self.set_year_as_index()
        self.min = self.df.index.min()
        self.max = self.df.index.max()

    def validate_year(self, year, comparison_year):
        """
        Validates if year arguments are within range.
        """
        if year == comparison_year:
            raise ValueError("The given year and comparison year cannot be the same.")
        if int(year) < int(self.min) or int(year) > int(self.max):
            raise ValueError(f"The given year {year} is out of the allowable range ({self.min} to {self.max}).")
        if int(comparison_year) < int(self.min) or int(comparison_year) > int(self.max):
            raise ValueError(f"The comparison year {comparison_year} is out of the allowable range ({self.min} to {self.max}).")

    def convert_columns_to_float(self):
        """
        Converts numeric columns to float, handling non-numeric values as NaN.
        """
        numeric_columns = self.df.columns[1:]  # Skip the 'Year' column
        self.df[numeric_columns] = self.df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    def calculate_avg_for_nan(self):
        """
        Calculates the average for rows with NaN in the 'Avg' column.
        """
        for index, row in self.df.iterrows():
            if pd.isna(row['Avg']):
                values_to_average = row['Jan':'Dec'].dropna().astype(float)
                if not values_to_average.empty:
                    self.df.at[index, 'Avg'] = values_to_average.mean()
    
    def set_year_as_index(self):
        """
        Sets the 'Year' column as the index for easier access.
        """
        self.df['Year'] = self.df['Year'].astype(str)  # Ensure the Year column is string type
        self.df.set_index('Year', inplace=True)
    
    def get_value(self, year, column):
        """
        Retrieves a value for a specified year and column.

        Args:
            year (int or str): The year for which the value is to be retrieved.
            column (str): The column (month or 'Avg') for which the value is to be retrieved.

        Returns:
            float: The CPI value for the specified year and column.
        """
        year = str(year)
        column = self.month_map.get(column, column)
        return self.df.at[year, column]

    def get_month_values(self, year, comparison_year=None, print_message=True, month=None, override_validation=False):
        """
        Retrieves the values for a specified month or the current month for both the given year and the comparison year.
        
        If the comparison year's value is not available, it switches to using the average values.

        Args:
            year (int or str): The year for which the value is to be retrieved.
            comparison_year (int or str, optional): The comparison year for which the value is also to be retrieved.
            print_message (bool): Flag to indicate if a message should be printed when switching to average values.
            month (str, optional): The month for which values are to be retrieved, defaults to the current month if None.
            override_validation (bool): Allows bypassing the year validation.

        Returns:
            pd.DataFrame: A DataFrame with the CPI values for the specified month and years.
        """
        comparison_year = str(comparison_year) if comparison_year else str(self.current_year)
        if not override_validation:
            self.validate_year(str(year), comparison_year)

        month = month.capitalize() if month else self.current_month
        month_abbreviation = self.month_map.get(month, month)
        value_for_given_year = self.get_value(year, month_abbreviation)
        value_for_comparison_year = self.get_value(comparison_year, month_abbreviation)

        if pd.isna(value_for_comparison_year):
            if print_message:
                print(f"Switching to average for calculation, {month} CPI is not available as of yet for {comparison_year}.")
            return self.get_avg_values(year, comparison_year, month_abbreviation, override_validation)

        data = {
            str(year): [value_for_given_year],
            comparison_year: [value_for_comparison_year]
        }
        return pd.DataFrame(data, index=[month])
    
    def get_avg_values(self, year, comparison_year=None, month=None, override_validation=False):
        """
        Retrieves the values from the 'Avg' column for both the given year and the comparison year, considering a specified month.

        Args:
            year (int or str): The year for which the average value is to be retrieved.
            comparison_year (int or str, optional): The comparison year for which the average value is also to be retrieved.
            month (str, optional): The month which context is considered when printing messages about missing data.
            override_validation (bool): Allows bypassing the year validation.

        Returns:
            pd.DataFrame: A DataFrame with the average CPI values for the specified year and the current year.
        """
        comparison_year = str(comparison_year) if comparison_year else str(self.current_year)
        
        if not override_validation:
            self.validate_year(str(year), comparison_year)

        month = month.capitalize() if month else self.current_month
        month_abbreviation = self.month_map.get(month, month)
        
        avg_column = 'Avg'
        value_for_given_year = self.get_value(year, avg_column)
        value_for_comparison_year = self.get_value(comparison_year, avg_column)

        data = {
            str(year): [value_for_given_year],
            comparison_year: [value_for_comparison_year]
        }
        return pd.DataFrame(data, index=[month if month else 'Avg'])




class InflationCalculator:
    def __init__(self, cpi_data_tool):
        """
        Initializes the InflationCalculator with a CPIDataTool instance or handles a Fail instance.
        Raises TypeError if the wrong type is provided and manages Fail instance appropriately.

        Parameters:
            cpi_data_tool (CPIDataTool or Fail): An instance of CPIDataTool containing CPI data, or a Fail instance indicating an initialization failure.
        """
        if isinstance(cpi_data_tool, Fail):
            print("Inflation calculator is currently unavailable.")
            self.is_available = False
            return
        elif not isinstance(cpi_data_tool, CPIDataTool):
            raise TypeError("cpi_data_tool must be an instance of CPIDataTool")
        
        self.cpi_data_tool = cpi_data_tool
        self.is_available = True

    def __call__(self, amount, original_year, target_year):
        """
        Allows the instance to be called like a function to calculate inflation-adjusted values.

        Parameters:
            amount (float): The amount of money to adjust for inflation.
            original_year (int): The original year of the amount.
            target_year (int): The target year to which you want to adjust the value.

        Returns:
            float or None: The inflation-adjusted value, or None if the calculator is unavailable.
        """
        return self.adjusted_value(amount, original_year, target_year)

    def adjusted_value(self, amount, original_year, target_year):
        """
        Calculate the inflation-adjusted value of an amount from the original year to the target year using CPI data.
        Automatically prints the result if the calculator is available.

        Parameters:
            amount (float): The amount of money to adjust for inflation.
            original_year (int): The original year of the amount.
            target_year (int): The target year to which you want to adjust the value.
        """
        if not self.is_available:
            print("Inflation calculation is unavailable due to initialization failure.")
            return None

        cpi_values = self.cpi_data_tool.get_avg_values(str(original_year), str(target_year))

        # Extract CPI values from the DataFrame
        cpi_original_year = cpi_values.iloc[0][str(original_year)]
        cpi_target_year = cpi_values.iloc[0][str(target_year)]

        # Calculate the adjusted value
        adjusted_value = amount * (cpi_target_year / cpi_original_year)
        adjusted_value = round(adjusted_value, 2)       
         
        # Print the result directly
        print(f"${amount} from {original_year} is equivalent to ${adjusted_value:.2f} in {target_year} dollars.")
        return adjusted_value

    def comparison(self, amount, n_years, plot=False):
        """
        Calculates the historical value change of a given dollar amount over the past n_years compared to the current month's CPI.
        If the current month's CPI is unavailable, it uses the annual average as a fallback. The current year is excluded if it's within the range of past years.

        Parameters:
            amount (float): The amount of money to examine historically.
            n_years (int): The number of years back to calculate the value from.
            plot (bool): Whether to plot the results. Defaults to False.

        Returns:
            dict: A dictionary containing years and their corresponding inflation-adjusted values relative to the current month's CPI or annual average.
        """
        if not self.is_available:
            print("Historical value calculation is unavailable due to initialization failure.")
            return None

        current_year = int(self.cpi_data_tool.current_year)
        start_year = current_year - n_years

        if start_year < int(self.cpi_data_tool.min) or current_year > int(self.cpi_data_tool.max):
            print(f"Data for the requested range is not available. Available range is {self.cpi_data_tool.min} to {self.cpi_data_tool.max}.")
            return None

        cpi_current = self.cpi_data_tool.get_avg_values(current_year, override_validation=True).iloc[0, 0]

        historical_values = {}

        for year in range(start_year, current_year):
            cpi_year = self.cpi_data_tool.get_avg_values(year, override_validation=True).iloc[0, 0]
            adjusted_value = amount * (cpi_year / cpi_current)
            adjusted_value = round(adjusted_value, 2)
            historical_values[year] = adjusted_value 

        for year, value in historical_values.items():
            print(f"${amount} from {year} is equivalent to ${value:.2f} in {current_year} dollars.")

        if plot:
            # Plot the results
            years = list(historical_values.keys())
            values = list(historical_values.values())

            plt.figure(figsize=(10, 5))
            plt.plot(years, values, marker='o', linestyle='-', color='b')
            plt.title(f'Inflation Adjusted Value of ${amount} Over Time ({start_year}-{current_year})')
            plt.xlabel('Year')
            plt.ylabel(f'Equivalent Value in {current_year} Dollars')
            plt.grid(True)
            plt.xticks(years, rotation=45)
            plt.tight_layout()
            plt.show()

        return historical_values

    def current_year_change(self, amount, plot=False):
        """
        Calculates the value of a given amount against the CPI values for each month of the current year where data is available.

        Args:
            amount (float): The amount of money to adjust based on past months' CPI data.
            plot (bool): Whether to plot the results. Defaults to False.

        Returns:
            dict: A dictionary with month names as keys and adjusted values as values, indicating the equivalent value of the given amount in each past month of the current year.
        """
        if not self.is_available:
            print("CPI data is unavailable, cannot perform calculation.")
            return None

        current_year = str(self.cpi_data_tool.current_year)
        month_values = self.cpi_data_tool.df.loc[current_year]
        results = {}

        for month, cpi in month_values.iteritems():
            if month != 'Avg' and not pd.isna(cpi):
                month_name = [name for name, abbr in self.cpi_data_tool.month_map.items() if abbr == month]
                if month_name:
                    month_name = month_name[0]
                else:
                    month_name = month

                adjusted_value = amount * (cpi / month_values['Avg'])
                results[month_name] = round(adjusted_value, 2) 

        if plot:
            # Plot the results
            months = list(results.keys())
            adjusted_values = list(results.values())

            plt.figure(figsize=(10, 5))
            plt.plot(months, adjusted_values, marker='o', linestyle='-', color='b')

            # Add titles and labels
            plt.title(f'Value of ${amount} Adjusted by CPI Changes for Each Month of {current_year}')
            plt.xlabel('Month')
            plt.ylabel('Adjusted Value ($)')
            plt.grid(True)

            # Display the plot
            plt.show()

        return results

    def __dir__(self):
        return ['comparison', 'current_year_change', 'adjusted_value']



class Fail:
    """
    Class to handle failure scenario for CPI Data Tool.

    Attributes:
        message (str): A message describing the failure reason.
    """

    def __init__(self, message=None):
        """
        Initializes a Fail object with a message.
        """
        self.message = message

    def print_message(self):
        """
        Prints the failure message to standard output.
        """
        print(self.message)

def create_cpi_tool(dataframe):
    """
    Factory function to create a CPIDataTool instance. Returns a Fail instance if the input is None.

    Args:
        dataframe (pd.DataFrame or None): The DataFrame containing the CPI data or None to indicate a failure condition.

    Returns:
        CPIDataTool or Fail: Returns an instance of CPIDataTool if the dataframe is valid, otherwise returns a Fail instance.
    """
    if dataframe is None:
        return Fail("Dataframe cannot be None. Please provide a valid pd.DataFrame.")
    else:
        return CPIDataTool(dataframe)



df = None 
try:
    PARSE = CPIHTMLTableParser()
    PARSE.fetch_data()
    df = PARSE.get_data_frame()
except:
    pass

cpi_processor = create_cpi_tool(df)
inflation_calculator = InflationCalculator(cpi_processor)
   

__all__= ["inflation_calculator"]

