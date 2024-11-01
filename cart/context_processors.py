from . cart import Cart

#Create context processor so our car cna

def cart(request):
    return {'cart':Cart(request)}

