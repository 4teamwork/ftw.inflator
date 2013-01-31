from ftw.inflator.interfaces import IInflatorCustomization
from zope.interface import implements


class InflatorCustomization(object):
    """Inflator customization utility.
    """

    implements(IInflatorCustomization)

    def __init__(self, product=None, image=None, order=10):
        self.product = product
        self.image = image
        self.order = order
