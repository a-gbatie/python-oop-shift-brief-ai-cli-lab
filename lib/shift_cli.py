from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """
        Initialize the CLI application.

        Requirements:
        - Store the injected AI client.
        - Use the provided brief builder when one is passed in.
        - Create a HandoffBriefBuilder when one is not passed in.
        - Set self.running to True.
        """
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """
        Print a welcome message and command guidance.

        Requirements:
        - Mention that this is a shift handoff brief CLI.
        - Include the available commands.
        """
        # TODO: Print welcome text and command help.
        print("Welcome to the Shift Handoff Brief CLI!")
        print(self.command_help())

    def command_help(self):
        """
        Return command guidance as a string.

        Required commands:
        - brief <shift notes>
        - revise <feedback>
        - history
        - reset
        - help
        - exit
        - quit
        """
        # TODO: Return a string describing the available commands.
        return """
        Available commands:
        - brief <shift notes>
        - revise <feedback>
        - history
        - reset
        - help
        - exit
        - quit
        """.strip()

    def handle_command(self, raw_input):
        """
        Route a user command.

        Requirements:
        - Return a readable input error for blank input.
        - Commands should be case-insensitive.
        - Extra spaces around commands should not break the app.
        - brief <shift notes> should call the brief builder's create_brief().
        - revise <feedback> should call the brief builder's revise_brief().
        - history should return the current message count.
        - reset should clear conversation history.
        - help should return command guidance.
        - exit and quit should stop the application.
        - Unknown commands should return a readable input error.
        - ValueError should become a readable Input Error.
        - RuntimeError should become a readable Service Error.
        """
        # TODO: Validate raw_input.
        # TODO: Parse the command and payload.
        # TODO: Route supported commands.
        # TODO: Return helpful messages for errors and unknown commands.
        try:
            if not isinstance(raw_input, str) or not raw_input.strip():
                raise ValueError("Please enter a command.")

            parts = raw_input.strip().split(maxsplit=1)

            command = parts[0].lower()
            payload = parts[1].strip() if len(parts) > 1 else ""

            if command == "brief":
              if not payload:
                raise ValueError("Please provide shift notes.")
              
              return self.brief_builder.create_brief(
                    self.ai_client,
                    payload
                )

            elif command == "revise":
              if not payload:
                raise ValueError("Please provide revision feedback.")
              
              return self.brief_builder.revise_brief(
                  self.ai_client,
                  payload
              )

            elif command == "history":
                count = self.ai_client.message_count()
                return f"Conversation messages: {count}"

            elif command == "reset":
                self.ai_client.reset()
                return "Conversation history reset successfully."

            elif command == "help":
                return self.command_help()

            elif command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"

            else:
                raise ValueError(f"Unknown command: {command}. Type 'help' to see available commands.")

        except ValueError as error:
            return f"Input Error: {error}"

        except RuntimeError as error:
            return f"Service Error: {error}"

    def run(self):
        """
        Run the CLI input loop.

        Requirements:
        - Display the welcome message before the loop starts.
        - Continue while self.running is True.
        - Read user input.
        - Pass user input to handle_command().
        - Print returned messages.
        - Stop cleanly if EOFError occurs.
        """
        # TODO: Display welcome text.
        # TODO: Run the input loop.
        self.display_welcome()

        while self.running:
            try:
                user_input = input("\nEnter command: ")

                result = self.handle_command(user_input)

                if result is not None:
                    print(result)

            except EOFError:
                self.running = False
                print("\nGoodbye!")



def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()