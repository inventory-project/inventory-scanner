import numpy as np
#import scipy.stats as sct

class Item:

    def __init__(
        self, d_avg, d_std, l_avg, order_quantity, service,
        l_std=0, service_measure = 'p1', review=1, u_avg=0, u_std=0, dl_avg=0, dl_std=0, costprice=0, current_reorderpoint=0, __reorder_point=0,
        ):

        self.d_avg = d_avg
        self.d_std = d_std
        self.l_avg = l_avg
        self.l_std = l_std
        self.order_quantity = order_quantity
        self.service = service
        self.service_measure = service_measure
        self.review = review
        self.u_avg = u_avg
        self.u_std = u_std
        self.dl_avg = dl_avg
        self.dl_std = dl_std
        self.costprice = costprice
        self.current_reorderpoint = current_reorderpoint
        self.__reorder_point = __reorder_point

    def average_inventory(self, undershoot=False):
        if self.__reorder_point == 0:
            self.reorder_point()
        return self.__reorder_point + self.order_quantity / 2

    def safety_stock(self, undershoot=False):
        if self.__reorder_point == 0:
            self.reorder_point()
        return self.__reorder_point - self.dl_avg

    def stock_costs(self, undershoot=False):
        if self.__reorder_point == 0:
            self.reorder_point()
        return 0.1*(self.__reorder_point - self.dl_avg + self.order_quantity / 2)

    def current_stock_costs(self, undershoot=False):
        if self.__reorder_point == 0:
            self.reorder_point()
        return 0.1*(self.current_reorderpoint - self.dl_avg + self.order_quantity / 2)

    def average_stock(self, undershoot=False):
        if self.__reorder_point == 0:
            self.reorder_point()
        return self.__reorder_point - self.dl_avg + self.order_quantity / 2

    def reorder_point(self, undershoot=False):
        self.leadtime_demand(undershoot)
        self.__reorder_point = self.dl_avg + self._find_k() * self.dl_std
        return self.__reorder_point

    def leadtime_demand(self, undershoot):
        _dl_avg = self.l_avg * self.d_avg
        _dl_std = (self.l_avg * self.d_std**2 + self.d_avg**2 * self.l_std**2)**0.5
        if not undershoot:
            self.dl_avg = _dl_avg
            self.dl_std = _dl_std
        elif undershoot:
            self._undershoot()
            self.dl_avg = _dl_avg + self.u_avg
            self.dl_std = (_dl_std**2 + self.u_std**2)**0.5
        return True


    def _find_k(self):
        if self.service_measure == 'p1':
            #return sct.norm.isf(q=(1-self.service),loc=0,scale=1)
            return 1.64
        elif self.service_measure == 'p2':
            guk = min((1 - self.service) * self.order_quantity / self.dl_std,5)
            z = np.sqrt(np.log(25/(guk**2)))
            h_top = -5.3925569 + 5.6211054*z - 3.8836830*(z**2) + 1.0897299*(z**3)
            h_bot = 1 - 0.72496485*z + 0.507326622*(z**2) + 0.0669136868*(z**3) - 0.00329129114*(z**4)
            return h_top / h_bot
        else:
            return 0

    def _undershoot(self):
        self.u_avg = (self.d_std**2 * self.review + self.d_avg**2 * self.review**2) / ( 2 * self.d_avg * self.review )
        # import pdb
        # pdb.set_trace()
        self.u_std = ((1 + (self.d_std/self.d_avg)**2 / self.review) * (1+2*(self.d_std/self.d_avg)**2 / self.review) * (self.review*self.d_avg)**2/3-self.u_avg**2)**0.5
        return True

X_LIST = []

X_LIST.append(22.6)
X_LIST.append(12.2)
X_LIST.append(30.6)
X_LIST.append(25.0)
X_LIST.append(35.0)
X_LIST.append(20.9)
X_LIST.append(43.4)
X_LIST.append(37.7)
X_LIST.append(24.1)
X_LIST.append(27.9)
X_LIST.append(19.6)
X_LIST.append(47.7)
X_LIST.append(39.4)
X_LIST.append(15.2)
X_LIST.append(37)
X_LIST.append(21.4)
X_LIST.append(42.4)
X_LIST.append(45.1)
X_LIST.append(23.4)
X_LIST.append(25.7)
X_LIST.append(29.6)
X_LIST.append(34.9)
X_LIST.append(32.2)
X_LIST.append(16.7)
X_LIST.append(16)
X_LIST.append(31.7)

X = np.array(X_LIST)

item = Item(
    # d_avg = np.average(X),
    # d_std = np.std(X, ddof=1),
    d_avg = 100,
    d_std = 10,
    l_avg = 10,
    order_quantity = 200,
    service = 0.95,
    service_measure = 'p2'
)

print (item.reorder_point(True))

item.service_measure = 'p1'

print (item.reorder_point(True))