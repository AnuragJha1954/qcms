from google import genai
from PIL import Image
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def compare_images(reference_images, uploaded_image):

    img = Image.open(uploaded_image)

    prompt = """
    Analyze this product image for quality.

    Check:
    - Freshness
    - Color consistency
    - Defects (rot, damage)
    - Overall grade

    Return STRICT JSON:

    {
      "match_score": number,
      "result": "GOOD or ACCEPTABLE or REJECT",
      "reason": "short explanation"
    }
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, img]
    )

    return response.text