from teradatasqlalchemy.types import VARCHAR
from teradataml.utils.validators import _Validators
from teradataml.dataframe.sql import _SQLColumnExpression
from teradatasqlalchemy import (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT,
                                NUMBER)
from teradatasqlalchemy import (TIMESTAMP, DATE, TIME)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
from teradatasqlalchemy import (INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH,
                                INTERVAL_DAY,INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                                INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                                INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                                INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND,
                                INTERVAL_SECOND)

def udf(user_function=None, returns=VARCHAR(1024), env_name = None, delimiter=',', quotechar=None):
    """
    DESCRIPTION:
        Creates a user defined function (UDF).

    PARAMETERS:
        user_function:
            Required Argument.
            Specifies the user defined function to create a column for
            teradataml DataFrame.
            Types: function
            Note:
                1. Lambda Function are not supported.

        returns:
            Optional Argument.
            Specifies the output column type.
            Types: teradata type
            Default: VARCHAR(1024)

        env_name:
            Optional Argument.
            Specifies the name of the remote user environment or an object of
            class UserEnv for VantageCloud Lake.
            Types: str or oject of class UserEnv.
            Note:
                * One can set up a user environment with required packages using teradataml
                  Open Analytics APIs. If no ``env_name`` is provided, udf use the default 
                  ``openml_env`` user environment. This default environment has latest Python
                  and scikit-learn versions that are supported by Open Analytics Framework
                  at the time of creating environment.

        delimiter:
            Optional Argument.
            Specifies a delimiter to use when reading columns from a row and
            writing result columns.
            Default value: ','
            Types: str with one character
            Notes:
                * This argument cannot be same as "quotechar" argument.
                * This argument cannot be a newline character.
                * Use a different delimiter if categorial columns in the data contains
                  a character same as the delimiter.

        quotechar:
            Optional Argument.
            Specifies a character that forces input of the user function
            to be quoted using this specified character.
            Using this argument enables the Advanced SQL Engine to
            distinguish between NULL fields and empty strings.
            A string with length zero is quoted, while NULL fields are not.
            Default value: None
            Types: str with one character
            Notes:
                * This argument cannot be same as "delimiter" argument.
                * This argument cannot be a newline character.

    RETURNS:
        ColumnExpression

    RAISES:
        TeradataMLException

    NOTES: 
        1. While working on date and time data types one must format these to supported formats.
           (See Requisite Input and Output Structures in Open Analytics Framework for more details.)
        2. Required packages to run the user defined function must be installed in remote user 
           environment using install_lib function Of UserEnv class. Import statements of these
           packages should be inside the user defined function itself.
        3. One can't call a regular function defined outside the udf from the user defined function.
           The function definition and call must be inside the udf. Look at Example 9 to understand more.

    EXAMPLES:
        # Load the data to run the example.
        >>> load_example_data("dataframe", "sales")

        # Create a DataFrame on 'sales' table.
        >>> df = DataFrame("sales")
        >>> df
                    Feb    Jan    Mar    Apr    datetime
        accounts                                          
        Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
        Jones LLC   200.0  150.0  140.0  180.0  04/01/2017
        Red Inc     200.0  150.0  140.0    NaN  04/01/2017
        Alpha Co    210.0  200.0  215.0  250.0  04/01/2017
        Blue Inc     90.0   50.0   95.0  101.0  04/01/2017
        Orange Inc  210.0    NaN    NaN  250.0  04/01/2017

        # Example 1: Create the user defined function to get the values in 'accounts'
        #            to upper case without passing returns argument.
        >>> from teradataml.dataframe.functions import udf
        >>> @udf
        ... def to_upper(s):
        ...     if s is not None:
        ...         return s.upper()
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(upper_stats = to_upper('accounts'))
        >>> res
                    Feb    Jan    Mar    Apr  datetime upper_stats
        accounts                                                    
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04    ALPHA CO
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04    BLUE INC
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  YELLOW INC
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04   JONES LLC
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  ORANGE INC
        Red Inc     200.0  150.0  140.0    NaN  17/01/04     RED INC
        >>>

        # Example 2: Create a user defined function to add length of string values in column  
        #           'accounts' with column 'Feb' and store the result in Integer type column.
        >>> from teradatasqlalchemy.types import INTEGER
        >>> @udf(returns=INTEGER()) 
        ... def sum(x, y):
        ...     return len(x)+y
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(len_sum = sum('accounts', 'Feb'))
        >>> res
                    Feb    Jan    Mar    Apr  datetime  len_sum
        accounts                                                 
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04      218
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04       98
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04      100
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04      209
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04      220
        Red Inc     200.0  150.0  140.0    NaN  17/01/04      207
        >>>

        # Example 3: Create a function to get the values in 'accounts' to upper case
        #            and pass it to udf as parameter to create a user defined function.
        >>> from teradataml.dataframe.functions import udf
        >>> def to_upper(s):
        ...     if s is not None:
        ...         return s.upper()
        >>> upper_case = udf(to_upper)
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(upper_stats = upper_case('accounts'))
        >>> res
                    Feb    Jan    Mar    Apr  datetime upper_stats
        accounts                                                    
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04    ALPHA CO
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04    BLUE INC
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  YELLOW INC
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04   JONES LLC
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  ORANGE INC
        Red Inc     200.0  150.0  140.0    NaN  17/01/04     RED INC
        >>>
    
        # Example 4: Create a user defined function to add 4 to the 'datetime' column
        #            and store the result in DATE type column.
        >>> from teradatasqlalchemy.types import DATE
        >>> import datetime
        >>> @udf(returns=DATE())
        ... def add_date(x, y):
        ...     return (datetime.datetime.strptime(x, "%y/%m/%d")+datetime.timedelta(y)).strftime("%y/%m/%d")
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(new_date = add_date('datetime', 4))
        >>> res
                      Feb    Jan    Mar    Apr  datetime  new_date
        accounts                                                  
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04  17/01/08
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04  17/01/08
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04  17/01/08
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  17/01/08
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  17/01/08
        Red Inc     200.0  150.0  140.0    NaN  17/01/04  17/01/08

        # Example 5: Create a user defined function to add 4 to the 'datetime' column
        #            without passing returns argument.
        >>> from teradatasqlalchemy.types import DATE
        >>> import datetime
        >>> @udf
        ... def add_date(x, y):
        ...     return (datetime.datetime.strptime(x, "%y/%m/%d")+datetime.timedelta(y))
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(new_date = add_date('datetime', 4))
        >>> res
                      Feb    Jan    Mar    Apr  datetime             new_date
        accounts                                                             
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04  2017-01-08 00:00:00
        Red Inc     200.0  150.0  140.0    NaN  17/01/04  2017-01-08 00:00:00
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  2017-01-08 00:00:00
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04  2017-01-08 00:00:00
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  2017-01-08 00:00:00
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04  2017-01-08 00:00:00

        # Example 6: Create a two user defined function to 'to_upper' and 'sum',
        #            'to_upper' to get the values in 'accounts' to upper case and 
        #            'sum' to add length of string values in column 'accounts' 
        #            with column 'Feb' and store the result in Integer type column.
        >>> @udf
        ... def to_upper(s):
        ...     if s is not None:
        ...         return s.upper()
        >>>
        >>> from teradatasqlalchemy.types import INTEGER
        >>> @udf(returns=INTEGER()) 
        ... def sum(x, y):
        ...     return len(x)+y
        >>>
        # Assign the both Column Expression returned by user defined functions
        # to the DataFrame.
        >>> res = df.assign(upper_stats = to_upper('accounts'), len_sum = sum('accounts', 'Feb'))
        >>> res
                      Feb    Jan    Mar    Apr  datetime upper_stats  len_sum
        accounts                                                             
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04    BLUE INC       98
        Red Inc     200.0  150.0  140.0    NaN  17/01/04     RED INC      207
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  YELLOW INC      100
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04   JONES LLC      209
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  ORANGE INC      220
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04    ALPHA CO      218
        >>>

        # Example 7: Convert the values is 'accounts' column to upper case using a user 
        #            defined function on Vantage Cloud Lake.
        # Create a Python 3.10.5 environment with given name and description in Vantage.
        >>> env = create_env('test_udf', 'python_3.10.5', 'Test environment for UDF')
        User environment 'test_udf' created.
        >>>
        # Create a user defined functions to 'to_upper' to get the values in upper case 
        # and pass the user env to run it on.
        >>> from teradataml.dataframe.functions import udf
        >>> @udf(env_name = env)
        ... def to_upper(s):
        ...     if s is not None:
        ...         return s.upper()
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> df.assign(upper_stats = to_upper('accounts'))
                    Feb    Jan    Mar    Apr  datetime upper_stats
        accounts                                                    
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04    ALPHA CO
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04    BLUE INC
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  YELLOW INC
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04   JONES LLC
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  ORANGE INC
        Red Inc     200.0  150.0  140.0    NaN  17/01/04     RED INC

        # Example 8: Create a user defined function to add 4 to the 'datetime' column
        #            and store the result in DATE type column on Vantage Cloud Lake.
        >>> from teradatasqlalchemy.types import DATE
        >>> import datetime
        >>> @udf(returns=DATE())
        ... def add_date(x, y):
        ...     return (datetime.datetime.strptime(x, "%Y-%m-%d")+datetime.timedelta(y)).strftime("%Y-%m-%d")
        >>>
        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(new_date = add_date('datetime', 4))
        >>> res
                      Feb    Jan    Mar    Apr  datetime  new_date
        accounts                                                  
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04  17/01/08
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04  17/01/08
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04  17/01/08
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  17/01/08
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  17/01/08
        Red Inc     200.0  150.0  140.0    NaN  17/01/04  17/01/08
        >>>

        # Example 9: Define a function 'inner_add_date' inside the udf to create a 
        #            date object by passing year, month, and day and add 1 to that date.
        #            Call this function inside the user defined function.
        >>> @udf
        ... def add_date(y,m,d):
        ... import datetime
        ... def inner_add_date(y,m,d):
        ...     return datetime.date(y,m,d) + datetime.timedelta(1)
        ... return inner_add_date(y,m,d)

        # Assign the Column Expression returned by user defined function
        # to the DataFrame.
        >>> res = df.assign(new_date = add_date(2021, 10, 5))
        >>> res
                    Feb    Jan    Mar    Apr  datetime    new_date
        accounts                                                    
        Jones LLC   200.0  150.0  140.0  180.0  17/01/04  2021-10-06
        Blue Inc     90.0   50.0   95.0  101.0  17/01/04  2021-10-06
        Yellow Inc   90.0    NaN    NaN    NaN  17/01/04  2021-10-06
        Orange Inc  210.0    NaN    NaN  250.0  17/01/04  2021-10-06
        Alpha Co    210.0  200.0  215.0  250.0  17/01/04  2021-10-06
        Red Inc     200.0  150.0  140.0    NaN  17/01/04  2021-10-06
        >>>
    """
    
    allowed_datatypes = (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER,
                        TIMESTAMP, DATE, TIME, CHAR, VARCHAR, CLOB, BYTE, VARBYTE,
                        BLOB, PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP,
                        INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH,
                        INTERVAL_DAY, INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                        INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                        INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                        INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND
                        )

    # Validate datatypes in returns.
    _Validators._validate_function_arguments([["returns", returns, False, allowed_datatypes]])
    
    # Notation: @udf(returnType=INTEGER())
    if user_function is None:
        def wrapper(f):
            def func_(*args):
                return _SQLColumnExpression(expression=None, udf=f, udf_type=returns, udf_args=args,\
                                            env_name=env_name, delimiter=delimiter, quotechar=quotechar)
            return func_
        return wrapper
    # Notation: @udf
    else:
        def func_(*args):
            return _SQLColumnExpression(expression=None, udf=user_function, udf_type=returns, udf_args=args,\
                                        env_name=env_name, delimiter=delimiter, quotechar=quotechar)
    return func_