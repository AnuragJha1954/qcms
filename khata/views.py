# khata/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Party, KhataEntry, Payment
from .utils import calculate_balance
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


from django.db.models import Q

def khata_home(request):
    query = request.GET.get("q")
    party_type = request.GET.get("type")
    balance_filter = request.GET.get("balance")

    parties = Party.objects.all()

    if query:
        parties = parties.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )

    if party_type:
        parties = parties.filter(type=party_type)

    data = []

    for p in parties:
        last_entry = p.entries.order_by('-created_at').first()
        balance = last_entry.running_balance if last_entry else 0

        # 🔥 balance filter
        if balance_filter == "positive" and balance <= 0:
            continue
        if balance_filter == "negative" and balance >= 0:
            continue

        data.append({
            "party": p,
            "balance": balance,
            "abs_balance": abs(balance)   # ✅ FIX HERE
        })

    return render(request, "khata/home.html", {"data": data})


def add_party(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        type_ = request.POST.get("type")

        Party.objects.create(name=name, phone=phone, type=type_)
        return redirect("khata_home")

    return render(request, "khata/add_party.html")


def party_detail(request, pk):
    party = get_object_or_404(Party, pk=pk)
    entries = party.entries.all().order_by('-created_at')
    balance = calculate_balance(party)

    return render(request, "khata/detail.html", {
        "party": party,
        "entries": entries,
        "balance": balance
    })


# khata/views.py

def add_entry(request, pk):
    party = get_object_or_404(Party, pk=pk)

    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        entry_type = request.POST.get("type")

        last_entry = party.entries.order_by('-created_at').first()
        last_balance = last_entry.running_balance if last_entry else 0

        if entry_type == 'credit':
            new_balance = last_balance + amount
        else:
            new_balance = last_balance - amount

        KhataEntry.objects.create(
            party=party,
            amount=amount,
            entry_type=entry_type,
            note=request.POST.get("note"),
            running_balance=new_balance
        )

        return redirect("party_detail", pk=pk)

    return render(request, "khata/add_entry.html", {"party": party})



# khata/views.py

def settle_payment(request, pk):
    party = get_object_or_404(Party, pk=pk)

    if request.method == "POST":
        amount = float(request.POST.get("amount"))

        last_entry = party.entries.order_by('-created_at').first()
        last_balance = last_entry.running_balance if last_entry else 0

        # Payment reduces balance
        new_balance = last_balance - amount

        # Save payment
        Payment.objects.create(
            party=party,
            amount=amount,
            note="Payment received"
        )

        # Also create ledger entry
        KhataEntry.objects.create(
            party=party,
            amount=amount,
            entry_type='debit',  # reduces balance
            note="Payment settled",
            running_balance=new_balance
        )

        return redirect("party_detail", pk=pk)

    return render(request, "khata/settle.html", {"party": party})








def export_pdf(request, pk):
    party = get_object_or_404(Party, pk=pk)
    entries = party.entries.all().order_by('created_at')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{party.name}_ledger.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Ledger - {party.name}", styles['Title']))

    for e in entries:
        line = f"{e.created_at.date()} | {e.note} | ₹{e.amount} | Bal: ₹{e.running_balance}"
        content.append(Paragraph(line, styles['Normal']))

    doc.build(content)
    return response





from django.db.models import Sum

def khata_analytics(request):
    parties = Party.objects.all()

    total_you_get = 0
    total_you_give = 0

    for p in parties:
        last = p.entries.order_by('-created_at').first()
        balance = last.running_balance if last else 0

        if balance > 0:
            total_you_get += balance
        else:
            total_you_give += abs(balance)

    return render(request, "khata/analytics.html", {
        "get": total_you_get,
        "give": total_you_give
    })


