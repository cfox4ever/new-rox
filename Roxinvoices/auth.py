

def allow_authenticated(request, private_file):
# Allow access only to authenticated users
   return request.user.is_authenticated