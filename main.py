import asyncio
from agents import (OutputGuardrailTripwireTriggered, Runner)
from openai.types.responses import ResponseTextDeltaEvent
from agents_config import Traige_Agent
from context import Message_output, UserContext
from shared import config


context = UserContext(
    name="Alice",
    uid=123,
    is_premium_user=False,
    issue_type="general"
)

async def main():
    print("🧠 Console Support System\n(Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        try:
            result = Runner.run_streamed(
                starting_agent=Traige_Agent,
                input=user_input,
                context=context,
                run_config=config
            )

            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

        except OutputGuardrailTripwireTriggered as e:
            print("\n⚠️ Guardrail triggered.")
            if e.guardrail_result and hasattr(e.guardrail_result.output, "response"):
                print(f"🤖 Bot (guarded output): {e.guardrail_result.output.response}")
            else:
                print("No response returned.")


        print()

if __name__ == "__main__":
    asyncio.run(main())
