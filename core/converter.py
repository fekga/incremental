# converter.py
from dataclasses import dataclass, field
from typing import List
from core.recipe import Recipe

empty = lambda: field(default_factory=list)

@dataclass
class Converter:
    name: str
    needs: List[Recipe] = empty()
    makes: List[Recipe] = empty()
    converters = list()
    OK,STOPPED,NO_INPUT,MAX_OUTPUT = range(4)
    state = STOPPED

    def __post_init__(self):
        Converter.converters.append(self)

    def start(self):
        self.state = Converter.OK

    def stop(self):
        self.state = Converter.STOPPED

    def is_stopped(self):
        return self.state == Converter.STOPPED

    def stay_hidden(self):
        if self.needs is not None:
            for recipe in self.needs:
                if recipe.resource.amount <= 0:
                    return True
        return False

    def update(self):
        if self.state == Converter.STOPPED:
            return
        for recipe in self.makes:
            resource = recipe.resource
            if resource.amount >= resource.max_amount:
                self.state = Converter.MAX_OUTPUT
                return
        for recipe in self.needs:
            resource = recipe.resource
            if (not resource.can_take(recipe.amount)
                or resource.amount < recipe.at_least
                or resource.amount > recipe.at_most):
                self.state = Converter.NO_INPUT
                return
        self.state = Converter.OK
        for recipe in self.needs:
            recipe.resource.take(recipe.amount)
        for recipe in self.makes:
            recipe.resource.give(recipe.amount)

    def change_by(self, *, needs=None, makes=None):
        return ChangeBy(self,needs,makes)

    def change_to(self, *, needs=None, makes=None):
        return ChangeTo(self,needs,makes)

    def __repr__(self):
        s = []
        if self.needs:
            s += ['Needs: ' + ', '.join(map(str,self.needs))]
        if self.makes:
            s += ['Makes: ' + ', '.join(map(str,self.makes))]
        return f'{self.name} {{{" | ".join(s)}}}'