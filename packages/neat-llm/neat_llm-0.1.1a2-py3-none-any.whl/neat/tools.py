import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, ParamSpec, TypeVar

import litellm
from loguru import logger
from pydantic import Field, create_model
from pydantic.json_schema import model_json_schema

from neat.utils import recursive_purge_dict_key

T = TypeVar("T")
P = ParamSpec("P")


class ToolManager:
    def __init__(self):
        self.registered_tools: Dict[str, Dict[str, Any]] = {}

    def _register_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        threaded: bool = False,
    ) -> None:
        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise ValueError(
                "Only regular functions can be registered as tools. For class methods, wrap them in a regular function."
            )

        tool_name = name or func.__name__
        tool_description = description or func.__doc__

        if tool_name in self.registered_tools:
            raise ValueError(
                f"Tool '{tool_name}' is already registered. Use a different name or unregister the existing tool first."
            )

        try:
            parameters = litellm.utils.function_to_dict(func)["parameters"]
        except Exception as e:
            logger.warning(f"Error using litellm.utils.function_to_dict: {e}")
            logger.warning("Falling back to Pydantic schema generation.")
            parameters = self.generate_schema(func)

        self.registered_tools[tool_name] = {
            "function": func,
            "description": tool_description,
            "parameters": parameters,
            "is_async": asyncio.iscoroutinefunction(func),
            "threaded": threaded,
        }

        logger.info(f"Tool '{tool_name}' registered successfully.")

    def add_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        threaded: bool = False,
    ) -> None:
        self._register_tool(func, name, description, threaded)

    def decorate_tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        threaded: bool = False,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            self._register_tool(func, name, description, threaded)
            return func

        return decorator

    def generate_schema(self, func: Callable[..., Any]) -> Dict[str, Any]:
        signature = inspect.signature(func)
        fields = {}
        for name, param in signature.parameters.items():
            annotation = (
                param.annotation if param.annotation != inspect.Parameter.empty else Any
            )
            default = ... if param.default == inspect.Parameter.empty else param.default
            fields[name] = (annotation, Field(default=default))

        model = create_model(f"{func.__name__}Model", **fields)
        schema = model_json_schema(model)

        recursive_purge_dict_key(schema, "title")
        recursive_purge_dict_key(schema, "additionalProperties")

        return schema

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"],
                },
            }
            for tool_name, tool_info in self.registered_tools.items()
        ]

    async def use_tool(self, function_name: str, function_args: Dict[str, Any]) -> Any:
        if function_name not in self.registered_tools:
            logger.error(f"Tool '{function_name}' not found")
            return f"Error: Tool '{function_name}' not found"

        tool_info = self.registered_tools[function_name]
        function_to_call = tool_info["function"]
        is_async = tool_info["is_async"]
        is_threaded = tool_info["threaded"]

        try:
            logger.debug(
                f"Calling function '{function_to_call.__name__}' with args: {function_args}"
            )
            if is_async:
                function_response = await function_to_call(**function_args)
            elif is_threaded:
                function_response = await asyncio.to_thread(
                    function_to_call, **function_args
                )
            else:
                function_response = function_to_call(**function_args)
            logger.debug(f"Function result: {function_response}")
            return function_response
        except Exception as e:
            error_message = f"Error executing {function_name}: {str(e)}"
            logger.error(f"Error in function call: {error_message}")
            return error_message
