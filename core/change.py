# change.py
from dataclasses import dataclass, field
from typing import List
from core.converter import Converter
from core.recipe import Recipe

empty = lambda: field(default_factory=list)

@dataclass
class Change:
    converter: Converter
    needs: List[Recipe] = empty()
    makes: List[Recipe] = empty()

    def apply(self):
        def _upgrade(current_recipes,upgrade_recipes):
            if upgrade_recipes is not None:
                for upgrade in upgrade_recipes:
                    for i,current in enumerate(current_recipes):
                        if upgrade.resource == current.resource:
                            if self.delta:
                                current_recipes[i] += upgrade
                            else:
                                current_recipes[i] = upgrade
        _upgrade(self.converter.needs,self.needs)
        _upgrade(self.converter.makes,self.makes)

    def __repr__(self):
        change_type = 'by' if self.delta else 'to'
        s = []
        if self.needs:
            s += ['Needs: ' + ', '.join(map(str,self.needs))]
        if self.makes:
            s += ['Makes: ' + ', '.join(map(str,self.makes))]
        return f'{self.converter.name} {change_type} {{{" | ".join(s)}}}'

@dataclass
class ChangeTo(Change):
    delta: bool = False

    def __repr__(self):
        return super().__repr__()

@dataclass
class ChangeBy(Change):
    delta: bool = True

    def __repr__(self):
        return super().__repr__()