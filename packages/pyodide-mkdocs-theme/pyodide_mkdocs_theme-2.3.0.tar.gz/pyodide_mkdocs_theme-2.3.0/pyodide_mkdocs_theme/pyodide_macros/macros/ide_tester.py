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


from dataclasses import dataclass
import json
from textwrap import dedent
from typing import ClassVar, Dict, List, Tuple, TYPE_CHECKING


from .. import html_builder as Html
from ..tools_and_constants import HtmlClass, Kinds, PageUrl, PmtTests, Prefix, ScriptKind, ScriptSection
from ..plugin.maestro_tools_tests import IdeToTest
from .ide_ide import Ide


if TYPE_CHECKING:
    from ..plugin.pyodide_macros_plugin import PyodideMacrosPlugin




@dataclass
class IdeTester(Ide):

    MACRO_NAME: ClassVar[str] = "IDE_tester"

    ID_PREFIX: ClassVar[str] = Prefix.tester_

    NEEDED_KINDS: ClassVar[Tuple[ScriptKind]] = (
        Kinds.pyodide,
        Kinds.terms,
        Kinds.ides,
        Kinds.ides_test,
    )


    @property
    def has_check_btn(self):
        """ Tester always has... """
        return True

    def register_ide_for_tests(self):
        """ IdeTester are never registered for testing... """

    def list_of_buttons(self):
        return super().list_of_buttons()[:2]

    def counter_txt(self):
        return ""


    def build_corr_and_rems(self):
        """
        No corr/REMs visible here. Replace with an extra button to trigger all the tests.
        """
        btn = self.create_button('test_ides')
        return (
            '<br>\n\n'
            f'<div class="inline" id="test-ide-results">{ btn }<ul>'
                '<li>IDEs found : <span id="cnt-all"></span></li>'
                '<li>Skip :       <span id="cnt-skipped" style="color:gray;"></span></li>'
                '<li>To do :      <span id="cnt-remaining"></span></li>'
                '<li>Success :    <span id="cnt-success" style="color:green;"></span></li>'
                '<li>Error :      <span id="cnt-failed" style="color:red;"></span></li>'
            '</ul>'
            '<button type="button" class="cases-btn" id="select-all">Select all</button>'
            '<br><button type="button" class="cases-btn" id="unselect-all">Unselect all</button>'
            '</div>'
            '\n\n'
        )






    #-----------------------------------------------------------------------------------



    @classmethod
    def get_markdown(cls):
        return dedent("""
            # Testing all IDEs in the documentation

            <br>

            {{ IDE_tester(MAX='+', MERMAID=True) }}

        """)



    @classmethod
    def build_html_for_tester(
        cls,
        env:'PyodideMacrosPlugin',
        pages_with_ides: Dict[PageUrl, List[IdeToTest]],
    ) -> str :
        """
        Build all the html base elements holding the results/information for each IDE to test.
        """

        use_load_button = env.testing_include == PmtTests.serve
        if env.testing_load_buttons is not None:
            use_load_button = env.testing_load_buttons

        script_data = {}
        table_like  = ''.join(
            row for url,lst in pages_with_ides.items()
                for item in lst
                for row in cls._build_one_ide_items(env, url, item, use_load_button, script_data)
        )
        div_table = Html.div(
            table_like,
            kls = HtmlClass.py_mk_tests_results
        )
        cases_script = f"<script>const CASES_DATA={ json.dumps(script_data) }</script>"

        return Html.div( div_table + cases_script, kls=HtmlClass.py_mk_tests_table)


    @classmethod
    def _build_one_ide_items(
        cls,
        env:'PyodideMacrosPlugin',
        url:str,
        item:IdeToTest,
        use_load_button:bool,
        script_data: List[str],
    ):
        def description(dump:dict, is_top=False):
            if is_top and 'description' not in dump:
                return ""
            desc = Html.div(dump['description'], kls="pmt_note_tests" + ' top_test'*is_top)
            if is_top:
                desc = '<br>' + desc
            return desc

        def dive(*a, id=None, kls=None,**kw):
            return Html.div(
                *a,
                id  = id and f"{ item.editor_id }-{ id }",
                kls = f"{ HtmlClass.py_mk_test_element } { kls or '' }".strip(),
                **kw
            )

        js_dump  = item.as_dict(env, url)
        ide_name = js_dump['ide_name']

        # Store for dump so script tag:
        script_data[ js_dump['editor_id'] ] = js_dump

        # Link + main test description
        a_href = Html.a(ide_name, href=js_dump['ide_link'], target="_blank")
        link   = dive( a_href + description(js_dump, True) )

        # Empty div that WILL hold the test's status svg indicator (filled in JS):
        svg_status = dive( '', id=HtmlClass.status, kls=HtmlClass.status + ' top_test')

        # Buttons
        load_btn  = cls.cls_create_button(env, 'load_ide') * use_load_button
        play_1    = cls.cls_create_button(env, 'test_1_ide')
        main_btns = dive( load_btn + play_1, id="test-btns")

        # sections indicators:
        sections = dive( ''.join([
            Html.checkbox(
                item.has_section[section],
                id=f"{ item.editor_id }_{ section }", tip_txt=section+"?",
                tip_shift=90,
            )
            for section in ScriptSection.sections()
        ]), kls='sections')


        yield link + svg_status + main_btns + sections      # Main line


        # Generate subtests if any:
        empty = '<div></div>'
        for i,sub_case in enumerate(js_dump.get('then', ()), 1):

            if 'then' in sub_case:
                raise ValueError("Case.then should go down one level at most.")

            div_svg = dive('', id=HtmlClass.status+str(i), kls=HtmlClass.status)
            yield dive(description(sub_case)) + div_svg + empty * 2
