class NaoTemBlocosNoRadarException(Exception):

    def __init__(self):
        super().__init__('Não há blocos no radar')
