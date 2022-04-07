from decimal import Decimal
from django.conf import settings
from store.models import Artifact


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, artifact):
        artifact_id = str(artifact.id)
        if artifact_id not in self.cart:
            self.cart[artifact_id] = {'quantity': 0, 'price': str(artifact.price)}
            self.cart[artifact_id]['quantity'] = 1
        else:    
            if self.cart[artifact_id]['quantity'] < 10:
                self.cart[artifact_id]['quantity'] += 1

            

        self.save()

    def update(self, artifact, quantity):
        artifact_id = str(artifact.id)
        self.cart[artifact_id]['quantity'] = quantity
        
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, artifact):
        artifact_id = str(artifact.id)
        if artifact_id in self.cart:
            del self.cart[artifact_id]
            self.save()

    def __iter__(self):
        artifact_ids = self.cart.keys()
        artifacts = artifact.objects.filter(id__in=artifact_ids)
        for artifact in artifacts:
            self.cart[str(artifact.id)]['artifact'] = artifact

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
