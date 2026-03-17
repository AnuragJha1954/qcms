from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quality.models import Product, QualityCheck
from sourcing.models import Supplier
from khata.models import Party, KhataEntry

from django.utils.timezone import now

def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    
    # Quality stats
    today = now().date()
    quality_checks = QualityCheck.objects.filter(created_at__date=today).count()
    total_products = Product.objects.count()

    # Sourcing stats
    total_suppliers = Supplier.objects.count()


    recent_checks = QualityCheck.objects.order_by('-created_at')[:3]
    
    # Khata stats
    parties = Party.objects.all()
    total_due = 0

    for p in parties:
        last = p.entries.order_by('-created_at').first()
        if last and last.running_balance > 0:
            total_due += last.running_balance

    return render(request, "dashboard.html", {
        "quality_checks": quality_checks,
        "total_products": total_products,
        "total_suppliers": total_suppliers,
        "total_due": int(total_due),
        "recent_checks": recent_checks
    })