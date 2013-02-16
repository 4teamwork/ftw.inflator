from Products.CMFPlone.browser.admin import AddPloneSite
from Products.CMFPlone.browser.admin import Overview
from ftw.inflator import _
from ftw.inflator.bundle import get_bundle_by_name
from ftw.inflator.bundle import get_bundles
from ftw.inflator.customization import get_merged_customizations
from ftw.inflator.interfaces import EXTENSION_PROFILES


class InflateView(AddPloneSite):

    default_extension_profiles = EXTENSION_PROFILES

    def __call__(self):
        form = self.request.form
        submitted = form.get('form.submitted', False)

        if submitted:
            site_id = form.get('site_id', 'platform')

            bundle = get_bundle_by_name(form.get('bundle'))

            site = bundle.install(
                self.context,
                site_id,
                title=form.get('title', ''),
                language=form.get('default_language', 'en'),
                extension_profiles=self.default_extension_profiles)

            self.request.response.redirect(site.absolute_url())

        return self.index()

    def get_site_id(self):
        id = self.request.get('site_id', 'platform')
        while id in self.context.objectIds():
            try:
                num = int(id[-1])
            except ValueError:
                id = id + str(1)
            else:
                num += 1
                id = id[:-1] + str(num)

        return id

    def get_customization(self):
        return get_merged_customizations()

    def get_bundle_options(self):
        def option(item):
            index, bundle = item
            return {
                'name': bundle.title.encode('utf-8'),
                'title': bundle.title,
                'description': bundle.description,
                'index': index}

        return map(option, enumerate(get_bundles()))


class InflateOverview(Overview):

    def get_bundle_title(self):
        customization = get_merged_customizations()
        return _(u'Create a new ${product} site',
                 mapping={'product': customization.product})

    def get_customization(self):
        return get_merged_customizations()
