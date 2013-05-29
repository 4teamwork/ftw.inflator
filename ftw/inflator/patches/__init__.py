from OFS.ObjectManager import ObjectManager
from ftw.inflator.customization import get_merged_customizations
from logging import getLogger


LOG = getLogger('ftw.inflator.patches')


def apply_patches():
    patch_ZMI_button()


def patch_ZMI_button():
    main = ObjectManager.manage_main
    orig = main.read()

    if 'ftw.inflator action' in orig:
        return False

    LOG.info('Patch install product button into ZMI.')

    main.inflator_customization = get_merged_customizations

    ADD_PLONE_SITE_HTML = '''
    <dtml-if "_.len(this().getPhysicalPath()) == 1 or this().meta_type == 'Folder' and 'PloneSite' not in [o.__class__.__name__ for o in this().aq_chain]">
      <!-- ftw.inflator action -->
      <form method="get"
            action="&dtml-URL1;/@@inflate"
            style="text-align: right; margin-top:0.5em; margin-bottom:0em;"
            target="_top">
        <input type="submit" value='Install <dtml-var expr="this().manage_main.inflator_customization().product">' style="font-size: 140%" />
      </form>
    </dtml-if>
    '''

    pos = orig.find('<!-- Add object widget -->')

    # Add in our button html at the right position
    new = orig[:pos] + ADD_PLONE_SITE_HTML + orig[pos:]

    # Modify the manage_main
    main.edited_source = new
    main._v_cooked = main.cook()

    return True

apply_patches()
