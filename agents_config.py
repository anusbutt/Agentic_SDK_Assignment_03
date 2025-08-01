from agents import Agent, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, OutputGuardrail, RunContextWrapper, Runner
from tools import refund_user, restart_service, greet_user
from context import Message_output, Apology_output
from shared import config

guardrail_agent:Agent = Agent(
    name="Guardrail_agent",
    instructions="check if the output includes any apology statement",
    output_type=Message_output
)

@OutputGuardrail
async def apology_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, output: Message_output
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context= ctx.context, run_config=config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_apology
    )

billing_agent:Agent = Agent(
    name="Billing Agent",
    instructions="Handle billing inquiries like refund.",
    tools=[refund_user],
)


general_agent:Agent = Agent(
    name="General agent",
    instructions="Handle general support questions.",
    tools=[greet_user]
)

technical_agent: Agent = Agent(
    name="Technical Agent",
    instructions="Handle technical issues like service restarts.",
    tools=[restart_service]
)


Traige_Agent: Agent = Agent(
    name="Traige Agent",
    instructions=(
        "You're the triage assistant. Route the query to the correct agent:\n"
        "- If it's about a refund or payment, hand off to the Billing Agent.\n"
        "- If it's about service not working, hand off to the Technical Agent.\n"
        "- Otherwise, handle it yourself as a general agent.\n"
        "Use these handoffs: billing_agent, technical_agent, general_agent."
    ),
    handoffs=[billing_agent, general_agent, technical_agent],
    output_guardrails=[apology_guardrail],
    output_type=Message_output
)