#
#   The banks server
#

from Pyro5.api import Daemon, locate_ns
from mercadoLeiloes import mercadoLeiloes


with Daemon() as daemon:
    with locate_ns() as ns:
        uri = daemon.register(mercadoLeiloes)
        ns.register("Mercado de Leiloes", uri)

    # enter the service loop.
    print("Servidor do Mercado de Leilões aberto")
    daemon.requestLoop()
