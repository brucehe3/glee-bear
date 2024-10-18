import os
import streamlit as st
from lib.google_place import GooglePlaceClient
from logic import ShopClient
from streamlit_chat import message
from streamlit_js_eval import get_geolocation

google_client = GooglePlaceClient(st.secrets["google_credentials"])
shop_client = ShopClient(google_client)

st.header("Glee Bear🐻")

if st.checkbox("Check my location"):
    location = get_geolocation()
    st.session_state['location'] = location

st.write("Just type: \"I want Chinese food\" or similar, and I'll recommend it for you!")

# if not ('latitude' in location and location['latitude']):
#     st.write("Please share your location to get started.")

if not ("user_prompt_history" in st.session_state
        and "chat_answers_history" in st.session_state
        and "chat_history" in st.session_state
        and "location" in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answers_history"] = []
    st.session_state["chat_history"] = []
    st.session_state["location"] = {}


def shop_response(shops):
    response = []
    shop_html = ("<div style='position:relative; background-image:url({photo}); "
                 "height:200px; width:240px; margin-bottom:10px;border-radius:20px;'>"
                 "<div style='position: absolute; bottom:0; border-bottom-left-radius: 20px;"
                 "border-bottom-right-radius: 20px; width:100%;"
                 "background: linear-gradient(to top, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0.6));'>"
                 "<h3 style='margin:8px;'>{name}</h3>"
                 "<p style='padding:4px 8px;font-size:14px'>{reason}</p>"
                 "<p style='font-size:12px;padding:0 8px 8px 0; text-align:right'>{distance:.2f} km</p>"
                 "</div>"
                 "</div>")
    for shop in shops:
        response.append(shop_html.format(**shop))

    return "".join(response)


prompt = st.text_input("What would you like to eat?", placeholder="Enter your thoughts..")

if prompt:

    if not st.session_state["location"]:
        st.write("Please share your location to get started.")
    else:
        with st.spinner("Generating response.."):
            coords = st.session_state["location"].get("coords")
            generated_response = shop_client.recommend_for_me(
                prompt, coords['latitude'], coords['longitude'], 5000, mock=False)

            if "message" in generated_response:
                st.write(generated_response["message"])
            else:
                formatted_response = shop_response(generated_response['shops'])

                st.session_state["user_prompt_history"].insert(0, prompt)
                st.session_state["chat_answers_history"].insert(0, formatted_response)
                # st.session_state["chat_history"].append(("human", prompt))
                # st.session_state["chat_history"].append(("ai", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    i = 0
    for user_query, generated_response in zip(st.session_state["user_prompt_history"],
                                              st.session_state["chat_answers_history"]):
        message(user_query, is_user=True, key=f"user_message_{i}")
        message(generated_response, key=f"response_message_{i}", allow_html=True)
        i += 1
