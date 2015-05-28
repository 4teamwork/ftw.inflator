from collections import defaultdict
from datetime import datetime
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.zipexport.generation import ZipGenerator
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from StringIO import StringIO
from zope.component import getMultiAdapter
from ZPublisher.Iterators import filestream_iterator
import json
import os


class InflatorExport(BrowserView):

    def __call__(self):
        if self.request.form.get('submitted'):
            return self.export()
        return super(InflatorExport, self).__call__()

    def export(self):
        with ZipGenerator() as generator:
            self.build_section_files(generator)
            return self.stream_for_downlaod(generator.generate())

    def stream_for_downlaod(self, zipfile):
        filename = 'content_creation-{0}.zip'.format(
            datetime.now().strftime('%Y%m%d%H%M'))
        self.request.response.setHeader(
            "Content-Disposition",
            'inline; filename="%s"' % filename.encode('utf-8'))
        self.request.response.setHeader("Content-type", "application/zip")
        self.request.response.setHeader(
            "Content-Length",
            os.stat(zipfile.name).st_size)
        return filestream_iterator(zipfile.name, 'rb')

    def build_section_files(self, generator):
        for section_id, objects in self.get_objects_by_sections().items():
            data = [self.get_data_for_object(obj, generator)
                    for obj in objects]
            path = u'content_creation/{0}.json'.format(
                section_id.decode('utf-8'))
            filedata = StringIO(json.dumps(data, sort_keys=True, indent=4))
            generator.add_file(path, filedata)

    def get_data_for_object(self, obj, generator):
        locals()['__traceback_info__'] = obj
        repr = getMultiAdapter((obj, self.request), IJSONRepresentation)

        def file_callback(context, key, fieldname, data, filename,
                          mimetype, jsondata):
            if not data:
                return

            if not isinstance(filename, unicode):
                filename = filename.decode('utf8')

            filepath = 'files/{0}-{1}/{2}'.format(
                '-'.join(obj.getPhysicalPath()[
                        len(self.context.getPhysicalPath()):]),
                fieldname,
                filename).decode('utf-8')
            generator.add_file(u'content_creation/' + filepath, StringIO(data))
            jsondata['{0}:file'.format(key)] = filepath

        return self.process_item(json.loads(repr.json(
                    file_callback=file_callback)))

    def get_objects_by_sections(self):
        sections = defaultdict(list)

        site_path = '/'.join(self.context.getPhysicalPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'sort_on': 'path'}
        brains = catalog.unrestrictedSearchResults(query)

        for brain in brains:
            section_id = brain.getPath().split('/')[site_path.count('/') + 1]
            obj = self.context.unrestrictedTraverse(brain.getPath())
            sections[section_id].append(obj)

        return sections

    def process_item(self, item):
        item['_path'] = '/'.join(
            item['_path'].split('/')[len(self.context.getPhysicalPath()):])

        properties = {}
        for name, value, type_ in item['_properties']:
            properties[name] = [type_, value]
        item['_properties'] = properties

        return item
