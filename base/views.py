# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.views.generic import DetailView
from .models import Product,Blog,ProductImage
from .forms import BlogForm,ProductForm,ProductImageFormSet


def home(request):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-createdAt')


    if query:
        products = products.filter(name__icontains=query)

    # Add pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)  # Show 10 products per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products, 'query': query}
    return render(request, 'home.html', context)


def product(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}

    return render(request, 'product_details.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Ensure 'slug' is not empty before querying the database
        slug = self.kwargs.get('slug')
        if not slug:
            raise Http404("Slug cannot be empty.")
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_title'] = self.get_object().name
        context['product_description'] = self.get_object().content
        context['prodct_image'] = self.get_object().thumbnail
        return context






def blog_list(request):
    # Get all blogs
    all_blogs = Blog.objects.all().order_by('-timestamp')

    # Number of blogs per page
    blogs_per_page = 10

    # Create a paginator
    paginator = Paginator(all_blogs, blogs_per_page)

    # Get the current page number from the request
    page = request.GET.get('page')

    try:
        # Get the blogs for the current page
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list.html')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form})


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        # Ensure 'slug' is not empty before querying the database
        slug = self.kwargs.get('slug')
        if not slug:
            raise Http404("Slug cannot be empty.")
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_object().title
        context['page_description'] = self.get_object().content
        context['page_image'] = self.get_object().image
        return context



@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_forms = ProductImageFormSet(request.POST, request.FILES, prefix='images')

        if product_form.is_valid() and image_forms.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            for image_form in image_forms:
                if image_form.cleaned_data.get('image'):
                    ProductImage.objects.create(product=product, image=image_form.cleaned_data['image'])

            return redirect('home')  # replace 'product_list' with the URL for your product listing page
    else:
        product_form = ProductForm()
        image_forms = ProductImageFormSet(prefix='images')

    return render(request, 'add_product.html', {'product_form': product_form, 'image_forms': image_forms})
