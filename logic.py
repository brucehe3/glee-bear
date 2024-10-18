from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from geopy.distance import geodesic
from lib.google_place_type import restaurant
from lib.mock.data import final_shops
from lib.prompt_template import place_prompt_string, recommend_prompt_string


class PlaceType(BaseModel):
    place_types: str = Field(description="matched items")


class Shop(BaseModel):
    index: int = Field(description="index number")
    name: str = Field(description="shop name")
    reason: str = Field(description="reason for recommendation")


class ShopList(BaseModel):
    shops: List[Shop]


def format_shop(shop_list):
    """
    1. Shop A: Rating 4.5, Review: 'Great environment, friendly service, but the price is a bit high.'
    2. Shop B: Rating 4.8, Review: 'Food is very delicious, prices are reasonable, but sometimes there is a wait.'
    :param shop_list:
    :return:
    """
    return "\n\n".join(
        f"Index: {shop['index']}. {shop['name']}: Rating {shop['rating']}, Reviews: {shop['reviews']}" for shop in shop_list)


class ShopClient:

    def __init__(self, google_client):
        self.google_client = google_client

    def shop_result_parser(self, original_shops, shops, latitude, longitude):

        shop_dict = {shop["index"]: shop for shop in original_shops}

        for item in shops:
            shop = shop_dict.get(item["index"])
            item["google_map_uri"] = shop["google_map_uri"]
            item["distance"] = geodesic((latitude, longitude), (shop["latitude"], shop["longitude"])).kilometers
            if shop["photos"]:
                item["photo"] = self.google_client.get_photo(shop["photos"][0].name)
            else:
                item["photo"] = ""

        return shops

    def place_type_tool(self, prompt):
        """from prompt understand customer's needs"""

        parser = JsonOutputParser(pydantic_object=PlaceType)
        prompt_template = PromptTemplate(
            template=place_prompt_string,
            input_variables=["user_input"],
            partial_variables={
                "place_type": restaurant,
                "format_instructions": parser.get_format_instructions(),
            }
        )
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", timeout=10)
        chain = prompt_template | llm | parser

        result = chain.invoke(input={
            "user_input": prompt
        })

        return result

    def recommend_for_me(self, prompt, latitude, longitude, radius, chat_history=[], mock=False):
        """let llm to decide which shops should recommend me"""

        if mock:
            return final_shops

        # from prompt to split business type first
        place_result = self.place_type_tool(prompt)

        if not place_result["place_types"]:
            return {
                "message": "Please enter your thoughts"
            }

        shops = self.google_client.sample_search_nearby(place_result["place_types"], latitude, longitude, radius, mock)
        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

        parser = JsonOutputParser(pydantic_object=ShopList)
        # 创建 PromptTemplate 实例
        prompt_template = PromptTemplate(
            template=recommend_prompt_string,
            input_variables=["action"],
            partial_variables={
                "context": format_shop(shops),
                "format_instructions": parser.get_format_instructions(),
            }
        )
        # 使用 LLM 生成结果
        chain = prompt_template | llm | parser
        result = chain.invoke(input={
            "action": prompt
        })

        # result parser
        result['shops'] = self.shop_result_parser(shops, result['shops'], latitude, longitude)
        return result


if __name__ == "__main__":
    pass
    # print(recommend_for_me("我想吃海南鸡饭", 1.3920613, 103.913496, 2000))
    # print(place_type_tool("我想吃酸辣土豆丝"))