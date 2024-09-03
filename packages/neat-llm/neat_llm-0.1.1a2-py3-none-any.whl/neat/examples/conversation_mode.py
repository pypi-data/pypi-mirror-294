from neat import Neat

neat = Neat()


@neat.lm(conversation=True)
def chat_with_ai():
    return [
        neat.system(
            "You are a friendly and knowledgeable AI assistant. Engage in a conversation with the user, answering their questions and providing helpful information."
        ),
        neat.user(
            "Hello! I'd like to chat about various topics. What shall we discuss?"
        ),
    ]


def main():
    chat_with_ai()  # This will start an interactive conversation


if __name__ == "__main__":
    main()
