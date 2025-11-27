from django.shortcuts import render  
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Cart,CartItem
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,TemplateView

from django.views.generic import FormView

from django.urls import reverse_lazy

from .forms import ContactForm  

from django.contrib import messages

from django.core.mail import EmailMessage

class IndexView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 6
    


class BookDetailView(DetailView):
    template_name = 'detail.html'
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['cart'] = cart
        return context
    
    
class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart_detail.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        context['items'] = CartItem.objects.filter(cart=cart)
        return context


@login_required(login_url='accounts:login')
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)


    item = CartItem.objects.filter(cart=cart, book=book).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(cart=cart, book=book, quantity=1)

    return redirect('bookshop:cart_detail')  

@login_required(login_url='accounts:login')
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = sum(item.subtotal() for item in items)
    count = sum(item.quantity for item in items)

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'count': count,
    })

@login_required(login_url='accounts:login')
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('bookshop:cart_detail')




class ContactView(FormView):

    template_name='contact.html'

    form_class = ContactForm

    success_url=reverse_lazy('bookshop:contact')

    def form_valid(self, form):

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject ='お問い合わせ:{}'.format(title)

        message = \
          '送信者名:{0}\n メールアドレス:{1}\n タイトル:{2}\n メッセージ:{3}' \
          .format(name, email, title, message)

        from_email = 'admin@example.com'

        to_list = ['admin@example.com']

        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )

        message.send()

        messages.success(
            self.request, 'お問い合わせは正常に送信されました。'
        )
        return super().form_valid(form)    