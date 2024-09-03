"""DAT files for MegaDrive Enhanced Colors."""
import re

from datoso.configuration import config
from datoso.repositories.dat_file import XMLDatFile


class MdEnhancedDat(XMLDatFile):
    """MegaDrive Enhanced Colors Dat class."""

    seed: str = 'md_enhanced'

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        name = self.name

        name_array = name.split(' - ')
        match len(name_array):
            case 1:
                company = None
                system = name_array[0]
            case 2:
                company, system = name_array
            case 3 | 4 | 5:
                company, system, *suffix = name_array
                self.suffix = suffix
        self.company = company
        self.system = system
        self.overrides()

        if self.modifier or self.system_type:
            self.prefix = config.get('PREFIXES', self.modifier or self.system_type, fallback='')
        else:
            self.prefix = None

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self) -> str:
        """Get the date from the dat file."""
        if self.file:
            result = re.findall(r'\(.*?\)', str(self.file))
            self.date = result[len(result)-1][1:-1]
        return self.date
