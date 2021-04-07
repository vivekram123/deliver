from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from deliver import settings
from .models import MenuItem, Category, OrderModel

class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/index.html')

class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        cookedfood = MenuItem.objects.filter(category__name__contains='Cookedfood')
        rawfood = MenuItem.objects.filter(category__name__contains='Rawfood')
        lightmeal = MenuItem.objects.filter(category__name__contains='Lightmeal')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'cookedfood': cookedfood,
            'rawfood': rawfood,
            'lightmeal': lightmeal,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
        )
        order.items.add(*item_ids)
        obj = EmailMessage(subject='Thanks for Registering on Blood Bank',
                    body='please click on this link 127.0.0.1:8000/ to Veriy your email id',
        from_email=settings.EMAIL_HOST_USER, bcc=[email,],)
        obj.send(fail_silently=False)
        # after everything is done send confirmation mail to the user
        # body= ('thank you for your order! you food is being made and will be delivered soon!\n'
        #         f'your total:{price}\n'
        #         'thank you again for your order!')

        # send_mail(
        #       'thank you for your order! body',
        #       'example@example.com',
        #       [email],
        #       fail_silently=False,
        #       ) 

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)
        
        







