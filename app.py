import os
import streamlit as st
from lib.google_place import GooglePlaceClient
from logic import ShopClient
from streamlit_chat import message
from streamlit_js_eval import get_geolocation
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_info(st.secrets["google_credentials"])

google_client = GooglePlaceClient(credentials)
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
                 "height:180px; width:240px; margin-bottom:10px;'>"
                 "<div style='position: absolute; bottom:0; width:100%;"
                 "background: linear-gradient(to top, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0.6));'>"
                 "<h3 style='margin:8px;'>{name} </h3>"
                 "<p style='padding:4px 8px;font-size:14px'>{reason}</p>"
                 "<p style='font-size:12px;padding:0 8px 8px 8px; text-align:left'>{distance:.2f} km "
                 "<a href='{google_map_uri}' target='_blank'>"
                 "<img style='width:24px;vertical-align: middle' src='https://storage.googleapis.com/support-kms-prod/sQ6yr8wryadBQXSDmVu6IHdmNF37Xn8IIBcn' /></a></p>"
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
