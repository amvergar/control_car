import psycopg2

class PostgresRepository:
    def __init__(self, db_name="control_car", user="postgres", password="Asvpichi2910", host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def get_vehicles(self):
        self.cursor.execute("SELECT id, placa, modelo, anio FROM vehiculo;")
        return self.cursor.fetchall()

    def add_vehicle(self, placa, modelo, anio):
        query = "INSERT INTO vehiculo (placa, modelo, anio) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (placa, modelo, anio))
        self.conn.commit()
