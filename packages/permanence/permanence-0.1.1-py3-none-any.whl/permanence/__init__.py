from .namespace import ScopeNamespace
from .scope_type import RunScope, make_scope
from .object import ObjectPermanence
from .artifact import Arty
from .chunks import ChunkCollection

pr = ObjectPermanence.new_namespace("main_program_scope")
Scope = pr.Scope
new_scope = pr.new_scope
