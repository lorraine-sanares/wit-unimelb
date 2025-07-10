import uuid
import json
import asyncio
from typing import Any, Optional
from dataclasses import dataclass

from llmgine.bus.bus import MessageBus
from llmgine.llm.context.memory import SimpleChatHistory
from llmgine.llm.models.openai_models import Gpt41Mini
from llmgine.llm.providers.providers import Providers
from llmgine.llm.tools.tool_manager import ToolManager
from llmgine.llm.tools import ToolCall
from llmgine.llm.models.openai_models import OpenAIResponse
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from llmgine.messages.commands import Command, CommandResult
from llmgine.messages.events import Event
from llmgine.llm import SessionID, AsyncOrSyncToolFunction


@dataclass
class DiscordEngineCommand(Command):
    """Command for the Discord Engine."""
    prompt: str = ""
    user_id: str = ""
    channel_id: str = ""


@dataclass
class DiscordEngineStatusEvent(Event):
    """Event emitted when the status of the engine changes."""
    status: str = ""


@dataclass
class DiscordEngineToolResultEvent(Event):
    """Event emitted when a tool is executed."""
    tool_name: str = ""
    result: Any = None


class DiscordEngine:
    def __init__(
        self,
        session_id: SessionID,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the Discord LLM engine.

        Args:
            session_id: The session identifier
            system_prompt: Optional system prompt to set
        """
        self.message_bus: MessageBus = MessageBus()
        self.engine_id: str = str(uuid.uuid4())
        self.session_id: SessionID = SessionID(session_id)

        # Create tightly coupled components
        self.context_manager = SimpleChatHistory(
            engine_id=self.engine_id, session_id=self.session_id
        )
        self.llm_manager = Gpt41Mini(Providers.OPENAI)
        self.tool_manager = ToolManager(
            engine_id=self.engine_id, session_id=self.session_id, llm_model_name="openai"
        )

        # Set system prompt if provided
        if system_prompt:
            self.context_manager.set_system_prompt(system_prompt)

    async def handle_command(self, command: DiscordEngineCommand) -> CommandResult:
        """Handle a Discord message command following OpenAI tool usage pattern.

        Args:
            command: The Discord command to handle

        Returns:
            CommandResult: The result of the command execution
        """
        try:
            # 1. Add user message to history
            self.context_manager.store_string(command.prompt, "user")

            # Loop for potential tool execution cycles
            while True:
                # 2. Get current context (including latest user message or tool results)
                current_context = await self.context_manager.retrieve()

                # 3. Get available tools
                tools = await self.tool_manager.get_tools()

                # 4. Call LLM
                await self.message_bus.publish(
                    DiscordEngineStatusEvent(
                        status="calling LLM", session_id=self.session_id
                    )
                )
                response: OpenAIResponse = await self.llm_manager.generate(
                    messages=current_context, tools=tools
                )
                assert isinstance(response, OpenAIResponse), (
                    "response is not an OpenAIResponse"
                )

                # 5. Extract the first choice's message object
                response_message: ChatCompletionMessage = response.raw.choices[0].message
                assert isinstance(response_message, ChatCompletionMessage), (
                    "response_message is not a ChatCompletionMessage"
                )

                # 6. Add the assistant message object to history
                await self.context_manager.store_assistant_message(response_message)

                # 7. Check for tool calls
                if not response_message.tool_calls:
                    # No tool calls, break the loop and return the content
                    final_content = response_message.content or ""

                    # Notify status complete
                    await self.message_bus.publish(
                        DiscordEngineStatusEvent(
                            status="finished", session_id=self.session_id
                        )
                    )
                    return CommandResult(
                        success=True, result=final_content, session_id=self.session_id
                    )

                # 8. Process tool calls
                for tool_call in response_message.tool_calls:
                    tool_call_obj = ToolCall(
                        id=tool_call.id,
                        name=tool_call.function.name,
                        arguments=tool_call.function.arguments,
                    )
                    try:
                        # Execute the tool
                        await self.message_bus.publish(
                            DiscordEngineStatusEvent(
                                status="executing tool", session_id=self.session_id
                            )
                        )

                        result = await self.tool_manager.execute_tool_call(tool_call_obj)

                        # Convert result to string if needed for history
                        if isinstance(result, dict):
                            result_str = json.dumps(result)
                        else:
                            result_str = str(result)

                        # Store tool execution result in history
                        self.context_manager.store_tool_call_result(
                            tool_call_id=tool_call_obj.id,
                            name=tool_call_obj.name,
                            content=result_str,
                        )

                        # Publish tool execution event
                        await self.message_bus.publish(
                            DiscordEngineToolResultEvent(
                                tool_name=tool_call_obj.name,
                                result=result_str,
                                session_id=self.session_id,
                            )
                        )

                    except Exception as e:
                        error_msg = f"Error executing tool {tool_call_obj.name}: {str(e)}"
                        print(error_msg)  # Debug print
                        # Store error result in history
                        self.context_manager.store_tool_call_result(
                            tool_call_id=tool_call_obj.id,
                            name=tool_call_obj.name,
                            content=error_msg,
                        )
                # After processing all tool calls, loop back to call the LLM again
                # with the updated context (including tool results).

        except Exception as e:
            print(f"ERROR in handle_command: {e}")  # Simple print for now
            import traceback
            traceback.print_exc()  # Print stack trace

            return CommandResult(success=False, error=str(e), session_id=self.session_id)

    async def register_tool(self, function: AsyncOrSyncToolFunction):
        """Register a function as a tool.

        Args:
            function: The function to register as a tool
        """
        await self.tool_manager.register_tool(function)
        print(f"Tool registered: {function.__name__}")

    async def clear_context(self):
        """Clear the conversation context."""
        self.context_manager.clear()

    def set_system_prompt(self, prompt: str):
        """Set the system prompt.

        Args:
            prompt: The system prompt to set
        """
        self.context_manager.set_system_prompt(prompt) 