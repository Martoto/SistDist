from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler


from Pyro5.api import Daemon, locate_ns
from mercadoLeiloes import mercadoLeiloes


if __name__ == '__main__':
    with Daemon() as daemon:

        mercado = mercadoLeiloes()
        with locate_ns() as ns:
            uri = daemon.register(mercado)
            ns.register("Mercado de Leiloes", uri)

        # enter the service loop.
        scheduler = BackgroundScheduler()
        scheduler.add_job(mercado.atualizarLista, 'interval', seconds=1)
        scheduler.start()
        print("Servidor do Mercado de Leilões aberto")
        daemon.requestLoop()
