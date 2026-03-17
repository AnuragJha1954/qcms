# khata/utils.py

def calculate_balance(party):
    credits = sum(e.amount for e in party.entries.filter(entry_type='credit'))
    debits = sum(e.amount for e in party.entries.filter(entry_type='debit'))
    payments = sum(p.amount for p in party.payment_set.all())

    return credits - debits - payments