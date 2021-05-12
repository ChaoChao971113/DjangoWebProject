from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id
# Create your views here.
def home_view(request):
    form = SalesSearchForm(request.POST or None)
    sale_data_frame = None
    positions_data_frame = None

    if(request.method == 'POST'):
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        print(date_from, date_to, chart_type)
        #qs refers query sets
        qs = Sale.objects.filter(created__gt=date_from, created__lt=date_to)
        if(len(qs) > 0):
            # data frame helps to visualize query set
            sale_data_frame = pd.DataFrame(qs.values())
            sale_data_frame['customers_id'] = sale_data_frame['customers_id'].apply(get_customer_from_id)
            sale_data_frame['salesman_id'] = sale_data_frame['salesman_id'].apply(get_salesman_from_id)

            # rename the feild name displayed where axis =1 refer to first row which is the feild names
            # attr inplace sepcify apply the changes to object self: Object = Object.rename
            sale_data_frame.rename({'customers_id':'customer', 'salesman_id':'salesman','id':'sales_id'},axis=1,inplace=True)
            sale_data_frame['created'] = sale_data_frame['created'].apply(lambda  x: x.strftime('%y-%m-%d'))
            sale_data_frame['updated'] = sale_data_frame['updated'].apply(lambda  x: x.strftime('%y-%m-%d'))




            positions_data = []
            for sale in qs:
                for pos in sale.get_positions():
                    temp = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id':pos.get_sales_id(),
                        #'transaction_id':pos.get_sales_trans_id(),
                    }
                    positions_data.append(temp)

            positions_data_frame = pd.DataFrame(positions_data)
            merged_data_frame = pd.merge(sale_data_frame, positions_data_frame, on='sales_id')

            sale_data_frame = sale_data_frame.to_html()
            positions_data_frame =positions_data_frame.to_html()






        else:
            print("No data match the interval")






    hello = 'hello worlds from views sale'

    context = {
        'hello':hello,
        'form': form,
        'sale_data_frame':sale_data_frame,
        'positions_data_frame':positions_data_frame
    }
    return render(request,'sales/home.html', context)

class SalesListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale;
    template_name = 'sales/detail.html'

def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html',{'object_list':qs})

def sale_detail_view(request, pk):
    obj = Sale.objects.get(pk=pk)
    return render(request, 'sales/detail.html',{'object':obj} )

