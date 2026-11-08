class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError("Shift notes cannot be empty.")

        sections = "\n".join(self.REQUIRED_SECTIONS)

        prompt = f"""
Create a professional shift handoff brief using the notes below.

Include these required sections:
{sections}

Do not invent unsupported details.
Use "Unknown" when information is not provided.

Shift Notes:
{notes.strip()}
"""
        return prompt.strip()

    def build_revision_prompt(self, feedback):
        if not isinstance(feedback, str) or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty.")

        sections = "\n".join(self.REQUIRED_SECTIONS)

        prompt = f"""
Revise the previous shift handoff brief based on the
earlier conversation and the manager's feedback.

Keep the brief accurate and professional.

Include these required sections:
{sections}

Do not invent unsupported details.
Use "Unknown" when information is not provided.

Manager Feedback:
{feedback.strip()}
"""
        return prompt.strip()

    def is_usable_brief(self, response_text):
        if not isinstance(response_text, str) or not response_text.strip():
            return False

        return all(
            section in response_text
            for section in self.REQUIRED_SECTIONS
        )

    def format_brief(self, response_text):
        return f"\nShift Handoff Brief\n{response_text}"

    def create_brief(self, ai_client, notes):
        prompt = self.build_brief_prompt(notes)

        response = ai_client.send(prompt)

        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections"
            )

        return self.format_brief(response)

    def revise_brief(self, ai_client, feedback):
        prompt = self.build_revision_prompt(feedback)

        response = ai_client.send(prompt)

        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections"
            )

        return f"\nRevised Shift Handoff Brief\n{response}"