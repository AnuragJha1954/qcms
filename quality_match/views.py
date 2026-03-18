import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, QualityCheck
from .services import compare_images


def quality_match_page(request):
    products = Product.objects.all()
    return render(request, "quality_match.html", {"products": products})

@csrf_exempt
def quality_match_api(request):

    if request.method == "POST":

        product_id = request.POST.get("product_id")
        image = request.FILES.get("image")

        if not product_id or not image:
            return JsonResponse({"error": "Missing data"}, status=400)

        product = Product.objects.get(id=product_id)

        qc = QualityCheck.objects.create(
            product=product,
            uploaded_image=image
        )

        ai_result = compare_images([], image)

        try:
            parsed = json.loads(ai_result)
        except:
            parsed = {
                "match_score": 75,
                "result": "ACCEPTABLE",
                "reason": "AI fallback result"
            }

        qc.match_score = parsed.get("match_score")
        qc.result = parsed.get("result")
        qc.ai_response = parsed
        qc.save()

        return JsonResponse({
            "match_score": qc.match_score,
            "result": qc.result,
            "reason": parsed.get("reason")
        })
        
        
def quality_camera_view(request):
    return render(request, "quality_camera.html")