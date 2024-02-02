from django.http import HttpResponse,JsonResponse

def home_page(request):
    print("home page requested")
    friends=[
        "apple",
        "apple",
        "apple"
    ]
    # return HttpResponse("This is home page")
    return JsonResponse(friends,safe=False)

