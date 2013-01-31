from ftw.inflator.interfaces import IInflatorCustomization
from zope.component import getUtilitiesFor
from zope.interface import implements


def get_merged_customizations():
    customizations = sorted(getUtilitiesFor(IInflatorCustomization))

    custom_data = {}

    for _order, cust in customizations:
        data = vars(cust).copy()
        del data['order']
        data = dict([(key, value) for key, value
                     in data.items()
                     if value is not None])
        custom_data.update(data)

    return InflatorCustomization(**custom_data)


class InflatorCustomization(object):
    """Inflator customization utility.
    """

    implements(IInflatorCustomization)

    def __init__(self, product=None, image=None, order=10):
        self.product = product
        self.image = image
        self.order = order
