# sourcing/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Procurement, Product
from django.db.models import Sum, Avg
# sourcing/views.py

from django.db.models import Avg, Sum, Count

def sourcing_home(request):
    suppliers = Supplier.objects.all()

    ranked = []

    for s in suppliers:
        avg_price = s.procurements.aggregate(Avg('price_per_unit'))['price_per_unit__avg'] or 0
        avg_quality = s.procurements.aggregate(Avg('quality_score'))['quality_score__avg'] or 0
        total_orders = s.procurements.count()

        # 🔥 SCORING FORMULA (tweakable)
        score = (avg_quality * 0.6) + (total_orders * 0.2) - (avg_price * 0.2)

        ranked.append({
            "supplier": s,
            "avg_price": round(avg_price, 2),
            "quality": round(avg_quality, 1),
            "orders": total_orders,
            "score": round(score, 2)
        })

    # 🔥 sort best first
    ranked.sort(key=lambda x: x['score'], reverse=True)

    return render(request, "sourcing/home.html", {
        "data": ranked,
        "best_supplier": ranked[0] if ranked else None
    })


def add_supplier(request):
    if request.method == "POST":
        Supplier.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address")
        )
        return redirect("sourcing_home")

    return render(request, "sourcing/add_supplier.html")


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    procurements = supplier.procurements.all().order_by('-created_at')

    return render(request, "sourcing/detail.html", {
        "supplier": supplier,
        "procurements": procurements
    })


def add_procurement(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        product = Product.objects.get(id=product_id)

        Procurement.objects.create(
            supplier=supplier,
            product=product,
            quantity=request.POST.get("quantity"),
            price_per_unit=request.POST.get("price"),
            quality_score=request.POST.get("quality")
        )

        return redirect("supplier_detail", pk=pk)

    return render(request, "sourcing/add_procurement.html", {
        "supplier": supplier,
        "products": products
    })
    
    




def price_comparison(request):
    products = Product.objects.all()

    result = []

    for product in products:
        procurements = Procurement.objects.filter(product=product)

        suppliers = []
        for p in procurements:
            suppliers.append({
                "supplier": p.supplier.name,
                "price": p.price_per_unit,
                "quality": p.quality_score
            })

        # sort by best price
        suppliers.sort(key=lambda x: x['price'])

        result.append({
            "product": product.name,
            "suppliers": suppliers
        })

    return render(request, "sourcing/price_compare.html", {"data": result})




