"""
Esta es la documentacion de player
Este es el modulo que incluye la clase del reproductor de musica
"""


class Player:
    """
    Esta Clase crea un reproductor de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio en el constructor
        Parameters: 
        song(str): este es un string con el path de la cancion

        Returns:
        int: devuelve 1 si reproduce con exito, devuelve 0 en caso de error
        """
        print("reproduciendo cancion")

    def stop(self):
        print("parando")
