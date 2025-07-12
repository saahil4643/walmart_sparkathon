from django.shortcuts import render, redirect
from .models import Product


def index(request):
    return render(request,'index.html')



def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        store_id = request.POST.get('store_id')
        current_stock = request.POST.get('current_stock')
        weekly_sales_rate = request.POST.get('weekly_sales_rate')
        price = request.POST.get('price')
        is_dead_stock = request.POST.get('is_dead_stock') == 'on'

        Product.objects.create(
            name=name,
            category=category,
            brand=brand,
            description=description,
            store_id=store_id,
            current_stock=current_stock,
            weekly_sales_rate=weekly_sales_rate,
            price=price,
            is_dead_stock=is_dead_stock
        )

        return redirect('product_sucess')

    return render(request, 'add_product.html')


def product_success(request):
    return render(request,'product_sucess.html')

from django.http import HttpResponse


from .models import Product, Notification
from django.http import HttpResponse

from django.http import HttpResponse
from .models import Product, Notification

def tag_dead_stock(request):
    products = Product.objects.all()
    updated_count = 0

    for product in products:
        was_dead = product.is_dead_stock
        product.is_dead_stock = product.weekly_sales_rate < 5 and product.current_stock > 100
        if product.is_dead_stock != was_dead:
            product.save()
            updated_count += 1

            if product.is_dead_stock:
                Notification.create_dead_stock_alert(product)

    return HttpResponse(f"✅ Dead stock tagging complete. {updated_count} items updated.")


from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product
from django.db.models import Q

def inventory_view(request):
    query = request.GET.get("q", "")
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()

    inventory = []
    for p in products:
        inventory.append({
            "Product": f"{p.name} ({p.brand})",
            "Quantity": p.current_stock,
            "Category": p.category,
            "Status": "Dead Stock" if p.is_dead_stock else "Live Stock"
        })

    return render(request, "inventory.html", {
        "inventory": inventory,
        "search_query": query  # So you can show the typed value back in input
    })


from .models import Notification
from django.shortcuts import render

from django.http import JsonResponse
from django.http import JsonResponse
from .models import Product

def alerts_view(request):
    dead_stock_products = Product.objects.filter(is_dead_stock=True).order_by('-store_id')

    return render(request, "alerts.html", {"alerts": dead_stock_products})

from django.shortcuts import render, redirect
from .models import Product, TransferRequest
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Product, TransferRequest


@csrf_exempt
def request_transfer_view(request):
    my_store_id = 101  # ⚠️ Replace with your actual store ID or use session

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        to_store_id = request.POST.get("to_store_id")
        quantity = int(request.POST.get("quantity"))

        print("🔁 Transfer POST Request Received")
        print(f"Product ID: {product_id}")
        print(f"From Store ID: {my_store_id}")
        print(f"To Store ID: {to_store_id}")
        print(f"Quantity: {quantity}")

        TransferRequest.objects.create(
            product_id=product_id,
            from_store_id=my_store_id,
            to_store_id=to_store_id,
            quantity=quantity,
        )
        print("✅ TransferRequest saved to DB")
        return redirect("request_transfer")

    # List all dead stock in my store
    my_dead_stock = Product.objects.filter(store_id=my_store_id, is_dead_stock=True)
    print(f"🔍 Found {my_dead_stock.count()} dead stock products in store {my_store_id}")

    candidates = []
    for prod in my_dead_stock:
        print(f"➡ Checking dead stock product: {prod.name} ({prod.brand})")

        # Find live stock in other stores
        live_in_others = Product.objects.filter(
            name=prod.name,
            brand=prod.brand,
            is_dead_stock=False
        ).exclude(store_id=my_store_id)

        print(f"   ➕ Found {live_in_others.count()} live stock(s) of same product in other stores")

        for live_prod in live_in_others:
            candidates.append({
                "product": prod,
                "to_store_id": live_prod.store_id,
                "available": live_prod.current_stock
            })
            print(f"   ✅ Added candidate transfer to store {live_prod.store_id}")

    print(f"📦 Total transfer candidates prepared: {len(candidates)}")

    return render(request, "transfer_request.html", {"candidates": candidates})


from django.shortcuts import render
from .models import Product

def transport_calculator_view(request):
    products = Product.objects.filter(is_dead_stock=True)  # You can change filter if needed
    result = None

    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        distance = float(request.POST.get("distance"))
        rate_per_km = float(request.POST.get("rate_per_km"))

        product = Product.objects.get(product_id=product_id)
        quantity = product.current_stock  # or any other field like quantity to be transferred

        total_cost = quantity * distance * rate_per_km

        result = {
            "product": product,
            "distance": distance,
            "rate_per_km": rate_per_km,
            "quantity": quantity,
            "total_cost": total_cost
        }

    return render(request, "transfer.html", {"products": products, "result": result})
