import pyodbc, getpass, base64

class SQL:
    def __init__(self, server:str, database:str, user:str, password:str = '') -> None:
        self.server = server
        self.database = database
        self.user = user
        self.password = password

        if not self.password:
            self.password = self.get_server_password()

    def login_sql(self) -> pyodbc.Connection:
        # Establish connection string
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}'
        # Create the connection
        try:
            conn = pyodbc.connect(connection_string)
            self.conn = conn
        except pyodbc.InterfaceError as e:
            if 'Login failed' in str(e):
                print("Login failed. Please check your username and password.")
            else:
                print(f"An interface error occurred: {e}")            
            exit(0)            

    def get_server_password(self) -> str:
        while True:
            try:
                password = getpass.getpass(f"Geef het wachtwoord op voor {self.server} en gebruiker {self.user}: ")
                if password != "":
                    self.password = password
            except ValueError:
                print("Geef een correct wachtwoord op.")

    def get_API_key(self):
        while True:
            try:
                apikey = getpass.getpass(f"Geef de API sleutel voor de dienst: ")
                if apikey != "":
                    return apikey
            except ValueError:
                print("Geef een correcte sleutel op.")

    def transact_sql(self, query:str, executemany:bool = False, params=None) -> list:
        try:
            # Create a cursor from the connection
            self.login_sql()
            conn = self.conn

            cursor = conn.cursor()
            # Execute the query with or without parameters based on whether params is provided
            if executemany and params is not None:
                cursor.executemany(query, params)
            elif params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Check if the SQL statement returned results
            if cursor.description is not None:
                # Fetch all rows from the query result
                rows = cursor.fetchall()
            else:
                print("The SQL statement did not return any results.")
                rows = []
            
            # Commit and, close the cursor and connection
            conn.commit()
            cursor.close()
            conn.close()

            # Convert the rows to a list and return
            return [list(row) for row in rows]
        except pyodbc.InterfaceError as e:
            print(f"An interface error occurred: {e}")            
            exit(0)

    def string_to_base64(self,string):
        string_bytes = string.encode("utf-8")
        base64_bytes = base64.b64encode(string_bytes)
        return base64_bytes.decode('utf-8')