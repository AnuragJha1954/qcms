# quality/views.py

from django.shortcuts import render, redirect, get_object_or_404
from quality_match.models import Product, QualityCheck
from .models import QualityParameter
from .utils import calculate_grade


def quality_home(request):
    products = Product.objects.all()

    data = []
    for p in products:
        last_check = QualityCheck.objects.filter(product=p).order_by('-created_at').first()

        data.append({
            "product": p,
            "score": last_check.score if last_check else 0,
            "grade": last_check.grade if last_check else "-"
        })

    return render(request, "quality/home.html", {"data": data})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    params = product.parameters.all()
    checks = QualityCheck.objects.filter(product=product).order_by('-created_at')

    return render(request, "quality/detail.html", {
        "product": product,
        "params": params,
        "checks": checks
    })


def add_parameter(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        QualityParameter.objects.create(
            product=product,
            name=request.POST.get("name"),
            min_value=request.POST.get("min"),
            max_value=request.POST.get("max"),
            ideal_value=request.POST.get("ideal")
        )
        return redirect("product_detail", pk=pk)

    return render(request, "quality/add_param.html", {"product": product})


def add_check(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        score = float(request.POST.get("score"))

        QualityCheck.objects.create(
            product=product,
            supplier_name=request.POST.get("supplier"),
            score=score,
            grade=calculate_grade(score),
            notes=request.POST.get("notes")
        )

        return redirect("product_detail", pk=pk)

    return render(request, "quality/add_check.html", {"product": product})




def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            Product.objects.create(name=name)

        return redirect("quality_home")

    return render(request, "quality/add_product.html")