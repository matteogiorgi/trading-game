from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string


class Trader:
    """trader main run function
    metodo chiave che viene invocato ogni volta che il sistema fornisce un nuovo snapshot del mercato
    """

    def run(self, state: TradingState):
        # prettyprint per il logging o il tuning della strategia
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        # alloco il dizionario che conterrà gli ordini per ogni prodotto e
        # itero su ogni prodotto per cui ci sono dati di mercato
        # (
        #     nota: se dico profondità 2, considero i primi due livelli di prezzo su entrambi i lati del mercato
        #     2 migliori offerete di acquisto e due migliori offerte di vendita
        #     con questo ho una visione più completa di come si muove il mercato e mi permette di fare:
        #         - stime sul fair value
        #         - strategie tipo order book imbalance
        #         - decisioni più informate per il market making
        # )
        result = {}
        for product in state.order_depths:
            # estraggo la profondità dell'ordine e imposto un prezzo di soglia:
            # noi dobbiamo calcolare il valore del prezzo di soglia dinamicamente con:
            #     - stato posizione attuale (rischio di superare i limiti)
            #     - ossevazioni ambientali (prezzo bene, indice e tariffe)
            #     - trades già avvenuti (nessuna reazione al mercato)
            #     - PnL o gestione del rischio
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10  # default

            # qui mostro quanti livelli cisono per comprare/vendere
            print("Acceptable price : " + str(acceptable_price))
            print(
                "Buy Order depth : "
                + str(len(order_depth.buy_orders))
                + ", Sell order depth : "
                + str(len(order_depth.sell_orders))
            )

            # se ci sono ordini di vendita, prendo il primo disponibile
            # (assunto come miglior ask)
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]

                # se il miglior ask è sotto il prezzo accettabile, acquisto tutto a quel prezzo
                if int(best_ask) < acceptable_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))

            # se ci sono ordini di acquisto, prendo il primo disponibile
            # (assunto come miglior bid)
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]

                # se il miglior bid è sotto il prezzo accettabile, vendo tutto a quel prezzo
                if int(best_bid) > acceptable_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))

            # nel dizionario fianle metto gli ordini associati al prodotto corrente
            result[product] = orders

        # string value holding Trader state data required ???
        # it will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"

        # sample conversion request ???
        # check more details below
        conversions = 1

        # ritorno dizionario, conversioni e dati persistenti
        return result, conversions, traderData
