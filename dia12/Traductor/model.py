import mysql.connector

class ModeloTraduccion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="BD_TRADUCCIONES_MOI"

        )

    def agregar_palabra(self, espanol, ingles):
        cursor = self.conexion.cursor()
        sql = """
            INSERT INTO TRADUCCIONES
            VALUES (DEFAULT, %s, %s)
        """
        cursor.execute(sql, (espanol, ingles))
        self.conexion.commit()
        cursor.close()

    def buscar_palabra(self, espanol):
        cursor = self.conexion.cursor()
        sql = """
            SELECT * FROM TRADUCCIONES
            WHERE PALABRA_ESPAÑOL = %s
            LIMIT 1
        """
        cursor.execute(sql, (espanol,))
        resultado = cursor.fetchone()
        cursor.fetchall()
        cursor.close()
        return resultado