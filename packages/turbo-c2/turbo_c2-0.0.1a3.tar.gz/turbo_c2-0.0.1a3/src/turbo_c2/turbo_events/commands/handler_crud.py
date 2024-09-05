from turbo_c2.extra_api.command.crud_command import CrudCommand
from turbo_c2.turbo_events.handlers.handler_controller import HandlerController


class HandlerCrud(CrudCommand[HandlerController, HandlerController]):
    api_identifier = "event_based_boolean_scheduler"
    api_path = "handler"
