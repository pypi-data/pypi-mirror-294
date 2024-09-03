import asyncio  # noqa: F401
import json
from pathlib import Path
from pprint import pprint

import click

from candore.errors import ModeError
from candore.modules.api_lister import APILister
from candore.modules.comparator import Comparator
from candore.modules.extractor import Extractor
from candore.modules.finder import Finder
from candore.modules.report import Reporting


class Candore:
    def __init__(self, settings):
        self.settings = settings
        self.api_lister = APILister(settings=self.settings)

    def list_endpoints(self):
        return self.api_lister.lister_endpoints()

    async def save_all_entities(
        self, mode, output_file, full, max_pages=None, skip_percent=None, resume=None
    ):
        """Save all the entities to a json file

        :param mode: Pre or Post
        :param output_file: Output file name
        :param full: If True, save entities from all pages of the components,
            else just saves first page
        :return: None
        """
        if mode not in ["pre", "post"]:
            raise ModeError("Extracting mode must be 'pre' or 'post'")

        async with Extractor(settings=self.settings, apilister=self.api_lister) as extractor:
            if full:
                extractor.full = True
            extractor.max_pages = max_pages
            extractor.skip_percent = skip_percent
            if resume:
                extractor.load_resume_info()
            data = await extractor.extract_all_entities()
            if hasattr(self.settings, 'rpms'):
                data.update({'installed_rpms': await extractor.extract_all_rpms()})

        if not data:
            click.echo("Entities data is not data found!")

        file_path = Path(output_file) if output_file else Path(f"{mode}_entities.json")
        with file_path.open(mode="w") as entfile:
            json.dump(data, entfile)
        click.echo(f"Entities data saved to {file_path}")

    def compare_entities(
        self,
        pre_file=None,
        post_file=None,
        inverse=None,
        output=None,
        report_type=None,
        record_evs=None,
    ):
        comp = Comparator(settings=self.settings)
        if record_evs:
            comp.record_evs = True
        results = comp.compare_json(pre_file=pre_file, post_file=post_file, inverse=inverse)
        reporter = Reporting(results=results)
        reporter.generate_report(output_file=output, output_type=report_type, inverse=inverse)

    def find_path(self, path, json_file, delimiter):
        finder = Finder()
        data = finder.find(path=path, json_file=json_file, delimiter=delimiter)
        if data:
            pprint(data)
