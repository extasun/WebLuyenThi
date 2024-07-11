def user_full_name(request):
    full_name = request.session.get('full_name', '')
    return {'full_name': full_name}