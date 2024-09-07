from typing import Any

from bolinette.core import meta
from bolinette.core.exceptions import InjectionError
from bolinette.core.injection.resolver import ArgResolverOptions
from bolinette.data.relational import AbstractDatabase, AsyncTransaction, EntityManager, EntitySession


class AsyncSessionArgResolver:
    def __init__(self, entities: EntityManager, transaction: AsyncTransaction) -> None:
        self.entities = entities
        self.transaction = transaction

    def supports(self, options: ArgResolverOptions) -> bool:
        return options.t.cls is EntitySession

    def resolve(self, options: ArgResolverOptions) -> Any:
        entity_type = options.t.vars[0]
        if not self.entities.is_entity_type(entity_type):
            raise InjectionError(
                f"Type {entity_type} is not registered as an entity",
                func=options.context.origin if options.context else None,
                param=options.context.arg_name if options.context else None,
            )
        engine = meta.get(entity_type, AbstractDatabase)
        return self.transaction.get(engine.name)
