def scheme(request):
    return 'https' if request and request.is_secure() else 'http'
