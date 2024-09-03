"""TranslatedEnglish Dat class to parse different types of dat files."""
from datoso.configuration import config
from datoso.repositories.dat_file import XMLDatFile


class VPinMameDat(XMLDatFile):
    """Translated English Dat class."""

    seed: str = 't_en'

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        self.company = None
        self.system = 'VPinMAME' if self.name.startswith('VPinMAME') else self.name
        self.suffix = None

        self.overrides()

        if self.modifier or self.system_type:
            self.prefix = config.get('PREFIXES', self.modifier or self.system_type, fallback='Pinball')
        else:
            self.prefix = None

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]
