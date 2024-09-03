import random

from pydantic import BaseModel, Field

from neat import Neat

neat = Neat()


class WeatherInfo(BaseModel):
    """Represents weather information for a specific location."""

    temperature: float = Field(..., description="Current temperature in Celsius")
    conditions: str = Field(..., description="Brief description of weather conditions")


class ClothingRecommendation(BaseModel):
    """Represents clothing recommendations based on weather."""

    top: str = Field(..., description="Recommended top clothing item")
    bottom: str = Field(..., description="Recommended bottom clothing item")
    accessories: str = Field(..., description="Recommended accessories, if any")


# You can register your custom tools as functions using one of 2 methods:
# 1. Using the @neat.tool() decorator
@neat.tool()
def get_weather(location: str) -> WeatherInfo:
    """Fetch current weather information for a given location."""
    # Simulating weather data for demonstration
    temp = round(random.uniform(-5, 35), 1)
    conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Windy", "Snowy"])
    return WeatherInfo(temperature=temp, conditions=conditions)


# 2. Using the neat.add_tool() method
def recommend_clothing(weather: WeatherInfo) -> ClothingRecommendation:
    """Recommend clothing based on weather conditions."""
    if weather.temperature < 10:
        return ClothingRecommendation(
            top="Warm coat", bottom="Thick pants", accessories="Scarf and gloves"
        )
    elif 10 <= weather.temperature < 20:
        return ClothingRecommendation(
            top="Light jacket", bottom="Jeans", accessories="Light scarf"
        )
    else:
        return ClothingRecommendation(
            top="T-shirt", bottom="Shorts", accessories="Sunglasses"
        )


# Register the function as a tool
neat.add_tool(recommend_clothing)


@neat.lm(tools=[get_weather, recommend_clothing])
def assistant():
    return [
        neat.system(
            "You are a helpful weather and fashion assistant. Use the get_weather tool to check the weather for specific locations, and the recommend_clothing tool to suggest appropriate outfits based on the weather."
        ),
        neat.user("What's the weather like in Paris today, and what should I wear?"),
    ]


def main():
    conversation = assistant()
    print("Weather and Fashion Assistant:")
    print(conversation)


if __name__ == "__main__":
    main()
