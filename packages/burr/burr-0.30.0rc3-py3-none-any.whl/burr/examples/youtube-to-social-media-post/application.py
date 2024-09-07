import textwrap
from typing import Union

import instructor
import openai
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from youtube_transcript_api import YouTubeTranscriptApi

from burr.core import Application, ApplicationBuilder
from burr.integrations.pydantic import PydanticTypingSystem, pydantic_action


class Concept(BaseModel):
    term: str = Field(description="A key term or concept mentioned.")
    definition: str = Field(description="A brief definition or explanation of the term.")
    timestamp: float = Field(description="Timestamp when the concept is explained.")

    def display(self):
        minutes, seconds = divmod(self.timestamp, 60)
        return f"{int(minutes)}:{int(seconds)} - {self.term}: {self.definition}"


class SocialMediaPost(BaseModel):
    """A social media post about a YouTube video generated its transcript"""

    topic: str = Field(description="Main topic discussed.")
    hook: str = Field(
        description="Statement to grab the attention of the reader and announce the topic."
    )
    body: str = Field(
        description="The body of the social media post. It should be informative and make the reader curious about viewing the video."
    )
    concepts: list[Concept] = Field(
        description="Important concepts about Hamilton or Burr mentioned in this post.",
        min_items=1,
        max_items=3,
    )
    key_takeaways: list[str] = Field(
        description="A list of informative key takeways for the reader.",
        min_items=1,
        max_items=4,
    )
    youtube_url: SkipJsonSchema[Union[str, None]] = None

    def display(self) -> str:
        formatted_takeways = " ".join([t for t in self.key_takeaways])
        formatted_concepts = "CONCEPTS\n" + "\n".join([c.display() for c in self.concepts])
        link = f"link: {self.youtube_url}\n\n" if self.youtube_url else ""

        return (
            textwrap.dedent(
                f"""\
            TOPIC: {self.topic}

            {self.hook}

            {self.body}

            {formatted_takeways}

            """
            )
            + link
            + formatted_concepts
        )


class ApplicationState(BaseModel):
    # Make these have defaults as they are only set in actions
    transcript: str = Field(description="The full transcript of the YouTube video.", default=None)
    post: SocialMediaPost = Field(description="The generated social media post.", default=None)


@pydantic_action(reads=[], writes=["transcript"])
def get_youtube_transcript(state: ApplicationState, youtube_url: str) -> ApplicationState:
    """Get the official YouTube transcript for a video given it's URL"""
    _, _, video_id = youtube_url.partition("?v=")

    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    state.transcript = " ".join([f"ts={entry['start']} - {entry['text']}" for entry in transcript])
    return state

    # store the transcript in state


@pydantic_action(reads=["transcript"], writes=["post"])
def generate_post(state: ApplicationState, llm_client) -> ApplicationState:
    """Use the Instructor LLM client to generate `SocialMediaPost` from the YouTube transcript."""

    # read the transcript from state
    transcript = state.transcript

    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=SocialMediaPost,
        messages=[
            {
                "role": "system",
                "content": "Analyze the given YouTube transcript and generate a compelling social media post.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    state.post = response

    # store the chapters in state
    return state


def build_application() -> Application[ApplicationState]:
    llm_client = instructor.from_openai(openai.OpenAI())
    app = (
        ApplicationBuilder()
        .with_actions(
            get_youtube_transcript,
            generate_post.bind(llm_client=llm_client),
        )
        .with_transitions(
            ("get_youtube_transcript", "generate_post"),
        )
        # .with_state_persister(SQLLitePersister(db_path=".burr.db", table_name="state"))
        .with_entrypoint("get_youtube_transcript")
        .with_typing(PydanticTypingSystem(ApplicationState))
        .with_tracker(project="youtube-post")
        .build()
    )
    return app


if __name__ == "__main__":
    app = build_application()
    app.visualize(output_file_path="statemachine.png")
    _, _, state = app.run(
        halt_after=["generate_post"],
        inputs={"youtube_url": "https://www.youtube.com/watch?v=hqutVJyd3TI"},
    )
    print(state.data.transcript)
    print(state.data.post.display())
