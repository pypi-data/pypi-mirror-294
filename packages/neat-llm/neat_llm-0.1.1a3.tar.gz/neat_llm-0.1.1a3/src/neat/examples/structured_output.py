import asyncio

from pydantic import BaseModel, Field

from neat import Neat
from neat.types import LLMModel

neat = Neat()


class MovieRecommendation(BaseModel):
    """Represents a movie recommendation with details."""

    title: str = Field(..., description="The title of the recommended movie")
    year: int = Field(..., description="The release year of the movie")
    genre: str = Field(..., description="The primary genre of the movie")
    reason: str = Field(
        ..., description="A brief explanation for why this movie is recommended"
    )


@neat.lm(model=LLMModel.MISTRAL_LARGE_LATEST, response_model=MovieRecommendation)
def recommend_movie(preferences: str):
    return [
        neat.system(
            "You are a movie recommendation expert. Provide recommendations based on user preferences."
        ),
        neat.user(f"Recommend a movie based on these preferences: {preferences}"),
    ]


@neat.alm(model=LLMModel.MISTRAL_LARGE_LATEST, response_model=MovieRecommendation)
async def recommend_movie_async(preferences: str):
    return [
        neat.system(
            "You are a movie recommendation expert. Provide recommendations based on user preferences."
        ),
        neat.user(f"Recommend a movie based on these preferences: {preferences}"),
    ]


def print_movie_recommendation(movie: MovieRecommendation) -> None:
    print("Movie Recommendation:")
    print(f"Title: {movie.title} ({movie.year})")
    print(f"Genre: {movie.genre}")
    print(f"Reason: {movie.reason}")


def main_sync() -> None:
    preferences = (
        "I like sci-fi movies with mind-bending plots and strong character development"
    )
    movie = recommend_movie(preferences)
    print_movie_recommendation(movie)


async def main_async() -> None:
    preferences = (
        "I like sci-fi movies with mind-bending plots and strong character development"
    )
    movie = await recommend_movie_async(preferences)
    print_movie_recommendation(movie)


if __name__ == "__main__":
    import nest_asyncio

    print("Synchronous recommendation:")
    main_sync()

    nest_asyncio.apply()
    print("\nAsynchronous recommendation:")
    asyncio.run(main_async())
