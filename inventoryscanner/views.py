import numpy as np
from io import BytesIO
import base64

from django.core.files.uploadedfile import InMemoryUploadedFile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from django.shortcuts import render, HttpResponse
from django.forms import formset_factory

from .forms import DemandForm, SelectWeeksForm, ParameterForm
from .inventory import Item

def scan(request):

    select_weeks_form = SelectWeeksForm()
    parameter_form = ParameterForm()

    DemandFormSet = formset_factory(DemandForm, extra = 52)
    demand_formset = DemandFormSet()

    results = None

    if request.method == 'POST':

        #import pdb; pdb.set_trace()

        undershoot=False

        demand_formset = DemandFormSet(request.POST)
        select_weeks_form = SelectWeeksForm(request.POST)
        parameter_form = ParameterForm(request.POST)

        if demand_formset.is_valid() and parameter_form.is_valid():

            demand_list = []
            for demand_form in demand_formset:

                if demand_form.cleaned_data['active'] == 'True':

                    demand_list.append(int(demand_form.cleaned_data['quantity']))

            demand = np.array(demand_list)

            item = Item(
                d_avg = np.average(demand),
                d_std = np.std(demand, ddof=1),
                l_avg = float(parameter_form.cleaned_data['l_avg']),
                order_quantity = float(parameter_form.cleaned_data['order_quantity']),
                service = float(parameter_form.cleaned_data['service']),
                service_measure = parameter_form.cleaned_data['service_measure'],
                costprice = float(parameter_form.cleaned_data['costprice']),
                current_reorderpoint = float(parameter_form.cleaned_data['current_reorderpoint']),
            )

            ss = item.safety_stock(undershoot)
            cycle_time = item.order_quantity / item.d_avg
            reorder_point = item.reorder_point(undershoot)

            t = [0.001]
            stock = [ss + item.order_quantity]
            reorder_line = [reorder_point]
            for x in range(1, 4):
                t.append(x*cycle_time)
                t.append(x*cycle_time+0.001)
                stock.append(ss)
                stock.append(ss+item.order_quantity)
                reorder_line.append(reorder_point)
                reorder_line.append(reorder_point)

            #plt.xlim(xmin = 0)
            #plt.ylim(ymin = 0)

            #plt.plot(range(10))

            x_max = 3 * item.order_quantity / item.d_avg + 0.01
            y_max = 10*(int(1.4*(ss + item.order_quantity)/10)+1)

            v = [0, x_max, 0, y_max]

            plt.clf()

            plt.axis(v)

            plt.plot(t,stock)
            plt.plot(t,reorder_line)
            buf = BytesIO()
            plt.savefig(buf, format='png')
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
            buf.close()

            results = {
                'reorder_point': item.reorder_point(undershoot),
                'average_inventory': item.average_inventory(undershoot),
                'average_stock': item.average_stock(undershoot),
                'stock_costs': item.stock_costs(undershoot),
                'current_stock_costs': item.current_stock_costs(undershoot),
                'some_plot': image_base64,
                'stock_cost_delta': 100*(item.current_stock_costs(undershoot) - item.stock_costs(undershoot))/item.stock_costs(undershoot)
            }

            print(results)

    template_context = {
        'select_weeks_form': select_weeks_form,
        'demand_formset': demand_formset,
        'parameter_form': parameter_form,
        'results': results,
    }

    template = 'scan.html'

    return render(request, template, template_context)
