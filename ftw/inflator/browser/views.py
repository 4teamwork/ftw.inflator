from Products.CMFPlone.browser.admin import AddPloneSite
from Products.CMFPlone.browser.admin import Overview
from Products.CMFPlone.factory import addPloneSite
from ftw.inflator import _
from ftw.inflator.bundle import get_bundles
from ftw.inflator.customization import get_merged_customizations


# these profiles will be installed automatically
EXTENSION_PROFILES = (
    'plonetheme.classic:default',
    'plonetheme.sunburst:default',
    )


class InflateView(AddPloneSite):

    default_extension_profiles = EXTENSION_PROFILES

    def __call__(self):
        context = self.context
        form = self.request.form
        submitted = form.get('form.submitted', False)

        if submitted:
            site_id = form.get('site_id', 'platform')

            bundle = self.get_bundle_by_name(form.get('bundle'))

            extensions = list(self.default_extension_profiles)
            extensions.extend(bundle.profiles)

            site = addPloneSite(
                context, site_id,
                title=form.get('title', ''),
                profile_id=bundle.base,
                extension_ids=extensions,
                setup_content=False,
                default_language=form.get('default_language', 'en'))

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

    def get_bundle_by_name(self, name):
        matches = filter(lambda bundle: bundle.title == name,
                         get_bundles())

        if len(matches) == 0:
            raise ValueError('No bundle found with name %s' % name)
        elif len(matches) > 1:
            raise ValueError('Too many bundles found with name %s' % name)

        return matches[0]


class InflateOverview(Overview):

    def get_bundle_title(self):
        customization = get_merged_customizations()
        return _(u'Create a new ${product} site',
                 mapping={'product': customization.product})

    def get_customization(self):
        return get_merged_customizations()
