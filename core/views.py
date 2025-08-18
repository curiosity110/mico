from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from core.forms import OrderForm
from products.models import ProductPage


def index(request):
    return render(request, 'index.html')



class ProductPageFormView(FormView):
    form_class = OrderForm

    def get_template_names(self):
        product_page = self.get_object()
        return [product_page.get_template_name()]

    def get_object(self):
        slug = self.kwargs.get("slug")
        return ProductPage.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_page"] = self.get_object()
        return context

    def get_initial(self):
        initial = super().get_initial()
        product_page = self.get_object()
        initial["product_id"] = product_page.product.id
        return initial

    def form_valid(self, form):
        order = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "core:thank-you",
        )


class TestView(TemplateView):
    template_name = "product-pages/bonefix/index.html"

class ThankYouView(TemplateView):
    template_name = "thank_you.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FAQView(TemplateView):
    template_name = "faq.html"


class ContactView(TemplateView):
    template_name = "contact.html"
