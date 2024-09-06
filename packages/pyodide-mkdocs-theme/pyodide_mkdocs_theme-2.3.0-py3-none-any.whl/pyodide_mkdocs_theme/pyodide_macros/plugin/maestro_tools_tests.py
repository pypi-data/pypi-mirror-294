"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""
# pylint: disable=multiple-statements, no-member



from pathlib import Path
from typing import ClassVar, Dict, List, Optional, TYPE_CHECKING, Union
from dataclasses import dataclass, field, fields

from pyodide_mkdocs_theme.pyodide_macros.parsing import items_comma_joiner


if TYPE_CHECKING:
    from .pyodide_macros_plugin import PyodideMacrosPlugin
    from ..macros.ide_ide import Ide






@dataclass
class Case:
    """
    Represent a test case for an IDE TEST argument (or profile).
    """

    # Globals for string definitions (public interface)
    DEFAULT: ClassVar['Case'] = None     # Defined after class declaration
    SKIP:    ClassVar['Case'] = None     # Defined after class declaration
    FAIL:    ClassVar['Case'] = None     # Defined after class declaration
    NO_CLEAR:ClassVar['Case'] = None     # Defined after class declaration
    CODE:    ClassVar['Case'] = None     # Defined after class declaration


    skip: bool = False
    """ Don't test this IDE """

    fail: bool = False
    """ This IDE has to fail the test """

    no_clear: bool = False
    """ Don't clear the scope for this test
        NOTE: this is useless unless all the tests are run in order...
    """

    code: bool = False
    """ Run the `code` section instead of the `corr` one. """

    description: str = ""
    """ Quick description of the test (optional). """



    #-------------------------------------------------------------------------
    # Private interface:

    run_play: bool = False
    """
    Runs the public tests only. Here, it's still possible to run either the code or the
    corr section, along with the tests section.
    """

    keep_profile: bool = False
    """ If True, the "mode" of the IDE is kept during the tests. """

    then: List['Case'] = field(default_factory=list)

    in_error_msg:      str = ""

    not_in_error_msg:  str = ""

    std_capture_regex: str = ""
    """ WARNING: this will work on content already formatted for jQuery.terminal output. """



    def __post_init__(self):
        self.then = self.then and [*map(self.ensure_conversion, self.then)]


    def as_dict(self, merge_with:dict=None):
        """
        Convert recursively to a dict, removing falsy values.
        """
        dct = { f.name: v for f in fields(self) if (v := getattr(self, f.name)) }
        if merge_with:
            dct = {**merge_with, **dct}
            dct.pop('then',())

        if self.then:
            dct['then'] = [ case.as_dict(merge_with=dct) for case in self.then ]

        elif not self.description:
            dct['description'] = ', '.join(f"{k}={v}" for k,v in dct.items() if k!='then')

        return dct



    @classmethod
    def ensure_conversion(cls, case: Union[str,'Case']) -> 'Case':
        """ Convert a string to the related Case instance, or just return the instance. """
        if isinstance(case, Case):
            return case
        if not case:
            return cls.DEFAULT
        return getattr(cls, case.upper())


    @classmethod
    def options_as_yaml_str(cls):
        """ Documentation purpose (macros config) """
        options = list(CASES_OPTIONS)
        options = [ f'`#!py "{ opt }"`' for opt in options ]
        return items_comma_joiner(options)



CASES_OPTIONS = '', 'skip', 'fail', 'no_clear', 'code'

Case.DEFAULT  = Case()
Case.FAIL     = Case(fail=True)
Case.SKIP     = Case(skip=True)
Case.NO_CLEAR = Case(no_clear=True)
Case.CODE     = Case(code=True)






@dataclass
class IdeToTest:

    name: str
    """ Python script name (guessed from the py_name argument...) """

    ID: Optional[int]
    """ ID argument for the IDE or None """

    editor_id: str
    """ editor_xxx """

    test: Case
    """ This IDE must not be tested if True """

    has_section: Dict[str,bool]
    """ Dict section_name -> existence """

    src_uri: str
    """ uri of the source file """


    @classmethod
    def from_(cls, ide:'Ide'):
        return cls(
            ide.py_name,
            ide.id,
            ide.editor_name,
            ide.test_config,
            dict(
                (name, bool(data))
                for name,data in ide.files_data.get_sections_data(as_sections=True)
            ),
            ide.env.page.file.src_uri,
        )


    def as_dict(self, env:'PyodideMacrosPlugin', url:str):
        """
        Data that will be transferred to the JS layer though various html attributes.

        WARNING: when this method is called env.page is the test_ides one, NOT the one of
                 the IDE we're interested in...
        """
        site_url  = env.site_url
        linker    = '/' * ( not site_url.endswith('/') )

        page_url = f"{ site_url }{ linker }{ url }"
        ide_link = f"{ page_url }#{ self.editor_id }"

        dir_step_up = not env.use_directory_urls or not self.src_uri.endswith('index.md')
        rel_dir_url = str(Path(url).parent) if dir_step_up else url

        ide_name = f"{ Path(url) / self.name }"
        if self.ID is not None:
            ide_name += f', ID={ self.ID }'

        return dict(
            **self.test.as_dict(),
            rel_dir_url  = rel_dir_url,
            page_url     = page_url,
            ide_link     = ide_link,
            ide_name     = ide_name,
            editor_id    = self.editor_id,
        )
