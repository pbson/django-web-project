from django.views.generic import ListView,TemplateView,DetailView,TemplateView,View
from homepage.models import Product,Category,Order,OrderProduct,Address
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext 
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from django.http import HttpResponseRedirect


# Create your views here.
class HomePageListView(ListView):
    template_name = 'index.html'
    def get_queryset(self):
        return Product.objects.all() 
    def get_context_data(self, **kwargs):
        context = super(HomePageListView, self).get_context_data(**kwargs)
        context.update({
            'category_list': Category.objects.all(),
            'product_list': Product.objects.all(),
        })
        return context
    
class BestSellerListView(ListView):
    template_name = 'best_seller.html'
    querryset = Product.objects.all()
    context_name = 'product_list'
    
    def get_queryset(self):
        return Product.objects.all()
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_name = 'product_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.all()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category.html'
    context_name = 'category'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context
    
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This product quantity was updated.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            order.products.add(order_product)
            messages.info(request, "This product was added to your cart.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "This product was added to your cart.")
        return redirect(request.META['HTTP_REFERER'])

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs.last()})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("homepage:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs.last()
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('homepage:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                        
                    if is_valid_form([shipping_address1]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
            return redirect('homepage:order-info')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("homepage:order-summary")

class OrderInfo(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
                'object': order
        }
        return render(self.request, 'info.html', context)
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        order_products = order.products.all()
        order_products.update(ordered=True)
        for product in order_products:
            product.save()
        order.ordered = True
        order.save()

        messages.success(self.request, "Thank you for shopping!")
        return redirect("/")

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, "This product was removed from your cart.")
            return redirect("homepage:order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("homepage:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("homepage:product", slug=slug)

@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "This product quantity was updated.")
            return redirect("homepage:order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("homepage:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("homepage:product", slug=slug)




    


