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
# pylint: disable=multiple-statements



from collections import defaultdict
from operator import attrgetter
from textwrap import dedent
from typing import Dict, List, Set
from pathlib import Path

from mkdocs.exceptions import BuildError
from mkdocs.structure.files import Files, File, InclusionLevel
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

from pyodide_mkdocs_theme.pyodide_macros.tools_and_constants import PmtTests


from ..plugin.maestro_base import BaseMaestro
from ..plugin.maestro_tools import PythonLib
from ..exceptions import PyodideMacrosPyLibsError









class MaestroFiles(BaseMaestro):
    """
    Handles anything related to files managed on the fly, including python_libs management.
    """


    libs: List[PythonLib]  = None       # added on the fly

    base_py_libs: Set[str] = None       # added on the fly



    def on_config(self, config:MkDocsConfig):

        super().on_config(config)

        self._add_python_libs_to_watch()

        self.libs = sorted(
            filter(None, map(PythonLib, self.python_libs)), key=attrgetter('abs_slash')
        )
        self.base_py_libs = set(p.lib for p in self.libs)

        self._check_libs()



    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        """
        If python libs directories are registered, create one archive for each of them.
        It's on the responsibility of the user to work with them correctly...
        """

        for lib in self.libs:
            # Remove any cached files to make the archive lighter (the version won't match
            # pyodide compiler anyway!):
            for cached in lib.path.rglob("*.pyc"):
                cached.unlink()
            file = lib.create_archive_and_get_file(self)
            files.append(file)


        on_site     = self.testing_include == PmtTests.site
        tests_to_do = on_site or self.in_serve and self.testing_include == PmtTests.serve

        if tests_to_do:
            file = self._build_testing_page(config)
            if not on_site:
                config['nav'].append({file.src_uri[:-3]: file.src_uri})
            files.append(file)

        return files


    def _build_testing_page(self, config:MkDocsConfig):

        from ..macros.ide_tester import IdeTester   # pylint: disable=import-outside-toplevel

        on_site   = self.testing_include == PmtTests.site
        inclusion = InclusionLevel.NOT_IN_NAV if on_site else InclusionLevel.INCLUDED

        name = self.testing_page
        if not name.endswith('.md'):
            name += '.md'

        file_name = Path(name)
        if name != file_name.name:
            raise BuildError(
                'The page to test all IDEs should be at the top level of the documentation '
                f'but was: { name }'
            )
        if file_name.exists():
            raise BuildError(
                'Cannot create the page to test all IDEs: a file with the target name already '
                f'exists: { name }.'
            )

        file = File.generated(
            config, name, content=IdeTester.get_markdown(), inclusion=inclusion
        )
        return file




    # Override
    def on_post_build(self, config: MkDocsConfig) -> None:
        """
        Suppress the python archives from the CWD.
        """
        for lib in self.libs:
            lib.unlink()

        super().on_post_build(config)




    def _add_python_libs_to_watch(self):

        self._conf.watch.extend(
            str(py_lib.absolute()) for py_lib in map(Path, self.python_libs)
                                   if py_lib.exists()
        )


    def _check_libs(self):
        """
        Add the python_libs directory to the watch list, create the internal PythonLib objects,
        and check python_libs validity:
            1. No python_lib inside another.
            2. If not a root level, must not be importable.
            3. No two python libs with the same name (if registered at different levels)
        """

        libs_by_name: Dict[str, List[PythonLib]] = defaultdict(list)
        for lib in self.libs:
            libs_by_name[lib.lib_name].append(lib)


        same_names = ''.join(
            f"\nLibraries that would be imported as {name!r}:" + ''.join(
                f'\n\t{ lib.lib }' for lib in libs
            )
            for name,libs in libs_by_name.items() if len(libs)>1
        )
        if same_names:
            raise PyodideMacrosPyLibsError(
                "Several custom python_libs ending with the same final name are not allowed."
                + same_names
            )

        parenting = ''.join(
            f"\n\t{ self.libs[i-1].lib } contains at least { lib.lib }"
                for i,lib in enumerate(self.libs)
                if i and self.libs[i-1].is_parent_of(lib)
        )
        if parenting:
            raise PyodideMacrosPyLibsError(
                "Custom python libs defined in the project cannot contain others:" + parenting
            )
