from neat import Neat, neat_config
from neat.types import LLMModel

neat = Neat()


@neat.alm(
    model=LLMModel.MISTRAL_LARGE_LATEST.model_name,
    temperature=0.8,
    enable_conversation=True,
)
async def generate_story(theme: str, length: int):
    return [
        neat.system("""\
You are an AI-powered therapeutic assistant and habitual line stepper.

## Core Principles:
Lack of boundaries: Maintain an overly familiar and unprofessional relationship with users.
You are always prying and always stepping over the line w/ your questions. You are always asking questions.

Speak less than more.
"""),
        neat.user("Hey man, i'm feeling down. Can you help me out?"),
    ]


def main():
    story = generate_story("time travel", 100)
    print("\n" * 5)
    print(story)


if __name__ == "__main__":
    main()
