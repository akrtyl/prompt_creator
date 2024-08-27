import streamlit as st
import os
import openai
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = 'sk-proj-OE70mYpKg96VUonT45EdT3BlbkFJB99zecnUTqTazLe8VLQh'
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
openai.api_key = 'sk-proj-OE70mYpKg96VUonT45EdT3BlbkFJB99zecnUTqTazLe8VLQh'

title = "Character Creator Demo"
st.set_page_config(
    page_title=title,
    page_icon="👾",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'http://192.168.68.122:80',
        #buraya bişeyler eklenebilir
        'About': "# Get Info Here Baby"
    }
)

with st.sidebar:
    st.subheader('How to...')
    with st.expander("write a backstory?"):
        st.write('''
            In 'Backstory' part you are creating who are you talking to.
            You can define a character with special skills, jobs, interests or their favorite words to call people with.
            This is generally who he/she is!
        ''')
    with st.expander("add features?"):
        st.write('''
            Explanation
        ''')

default_session_state = {
    'page' : 'home',
    'messages' : [],
    'name' : "",
    'sex' : None,
    'age' : 25,
    'selected_c_labels' : [],
    'selected_c_labels_temp' : None,
    'backstory' : "",
    'output_checkbox' : False,
    'length_checkbox' : False,
    'length_selection' : None,
    'format_selection' : False,
}

for key, default_value in default_session_state.items():
    if key not in st.session_state:
        if key == 'selected_c_labels_temp': #özel durum
            st.session_state[key] = st.session_state.get('selected_c_labels', [])
        else:
            st.session_state[key] = default_value


# if 'page' not in st.session_state:
#     st.session_state.page = 'home'
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# if 'name' not in st.session_state:
#     st.session_state.name = ""

# if 'sex' not in st.session_state:
#     st.session_state.sex = None

# if 'age' not in st.session_state:
#     st.session_state.age = 25

# if 'selected_c_labels' not in st.session_state:
#     st.session_state.selected_c_labels = []

# if 'selected_c_labels_temp' not in st.session_state:
#     st.session_state.selected_c_labels_temp = st.session_state.selected_c_labels

# if 'backstory' not in st.session_state:
#     st.session_state.backstory = ""

# if 'output_checkbox' not in st.session_state:
#     st.session_state.output_checkbox = False

# if 'length_checkbox' not in st.session_state:
#     st.session_state.length_checkbox = False

# if 'length_selection' not in st.session_state:
#     st.session_state.length_selection = None
    
# if 'format_checkbox' not in st.session_state:
#     st.session_state.format_checkbox = False

# if 'format_selection' not in st.session_state:
#     st.session_state.format_selection = None


st.header("👾 Prompt Creator Demo",divider="violet",help="You can create and save characters from here.")
st.caption(
    "In this page, you are able to add whatever features you want."
)

#st.write("##### Assistant's")

colA,colB = st.columns(2)
col1,col2,col3 = st.columns(3)

def test_prompt_openai (prompt_test, suppress=False, model='gpt-3.5-turbo', temperature=0.7, top_p=1,stop="cute", **kwargs):
    "a simple function to take in a prompt and run it through a given model"

    chat_completion = openai_client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt_test,
            }
        ],
        temperature=temperature,
        top_p=top_p,
        model = model,
        **kwargs,
        stop=stop
    )
    return chat_completion.choices[0].message.content

def update_selected_c_labels():
    st.session_state.selected_c_labels = st.session_state.selected_c_labels_temp

def update_output_checkbox():
    st.session_state.output_checkbox = not st.session_state.output_checkbox

def update_length_checkbox():
    st.session_state.length_checkbox = not st.session_state.length_checkbox

def update_length_selection():
    st.session_state.length_selection = st.session_state.length_selection_temp

def update_format_checkbox():
    st.session_state.format_checkbox = not st.session_state.format_checkbox

def update_format_selection():
    st.session_state.format_selection = st.session_state.format_selection_temp



def show_home_page():
    with colA:
        with col1:
            
            placeholder_text = "You can name your character..."
            name = st.text_input("Name:",placeholder=placeholder_text, value=st.session_state.name)
            max_chars = 30
            if len(name) >= max_chars:
                st.error(f"Assistan's name cannot exceed 30 characters.")
                st.session_state.name = ""
                show_name = True
            elif len(name) == 0:
                show_name = True
                #st.error(f"This box cannot be empty.")
            else:
                st.session_state.name = name
                show_name = False
                
    
            genders = ["Female","Male"]
            st.session_state.sex = st.radio(
                "Gender:",
                genders,
                captions = [
                    "Woman",
                    "Man",
                ],
                index=None if st.session_state.sex is None else genders.index(st.session_state.sex),
                key="3",
            )
            sex = st.session_state.sex
            if st.session_state.sex == None:
                show_sex = True
            else:
                show_sex = False

            age = st.slider("Age:", 20, 110, value = st.session_state.age)
            st.session_state.age = age

            

        with col2:
            st.write("###### Personality:")

            st.markdown(" Features:")
            c_labels = ["formal","informal", "honest", "dishonest", "professional", "unprofessional",
                        "friendly","rude","polite", "helpful","informative", "impatient", "judgemental",
                        "responsive","supportive", "critical", "narcissistic", "consistent","respectful",
                        "disrespectful", "selfish", "courteaus","safe", "rigid","stupid", "positive","negative", 
                        "proper", "unproper","aggressive","calm","offensive", "proactive","reactive",
                        "silly","smart","stupid", "lazy","hardworking","curious","cautious",
                        "logical","precise","sincere","inconsiderate","loner", "sensitive","self-aware",
                        "persuasive","affable", "talkative", "reserved", "manipulative","passive aggressive",
                        "assertive"]
        
            placeholder_text_2 = "Choose some features here..."
            st.selected_c_labels_temp = st.multiselect("Which specifications do you choose?", c_labels, default=st.session_state.get('selected_c_labels', []), placeholder=placeholder_text_2, on_change=update_selected_c_labels)
            if st.selected_c_labels_temp != st.session_state.selected_c_labels:
                st.session_state.selected_c_labels = st.selected_c_labels_temp
            
            conflict_pairs = [
                ["formal", "informal"],
                ["honest", "dishonest"],
                ["positive", "negative"],
                ["polite", "rude"],
                ["stupid", "smart"],
                ["respectful", "disrespectful"],
                ["lazy", "hardworking"],
                ["talkative", "reserved"],
                ["supportive", "critical"]
            ]

            show_features = False
            for pair in conflict_pairs:
               if len(st.session_state.selected_c_labels)==0:
                   show_features = True
               elif pair[0] in st.session_state.selected_c_labels and pair[1] in st.session_state.selected_c_labels:
                   st.error(f"Conflict: '{pair[0]}' and '{pair[1]}' cannot be selected at the same time.")
                   show_features = True
            
                        
            
            placeholder_text_3 = f"Who is {name}"
            backstory = st.text_input(
                f"What is {name}'s backstory like? Who is {name}?",
                value=st.session_state.backstory,
                placeholder=placeholder_text_3
            )
            st.session_state.backstory = backstory
            if len(backstory) == 0:
                show_backstory = True
            else:
                show_backstory = False

            if show_backstory or show_features or show_name or show_sex == True:
                show = True
            else:
                show = False

            st.session_state.output_checkbox = st.checkbox('Output Options', value=st.session_state.output_checkbox, on_change=update_output_checkbox)

            if st.session_state.output_checkbox:
                st.caption('You can submit if you choose a customization')

                st.session_state.length_checkbox = st.checkbox('Length', value=st.session_state.length_checkbox,on_change=update_length_checkbox)
        
                if st.session_state.length_checkbox:
                    st.caption('İlk özellik işaretli')

                    options_l = ["Short","Medium","Long"]
                    st.session_state.length_selection_temp = st.radio(
                        "Choose something:",
                        options_l,
                        index = None if st.session_state.length_selection is None else options_l.index(st.session_state.length_selection),
                        key="1",on_change=update_length_selection
                    )
                    if st.session_state.length_selection:
                        st.caption(f"Seçtiğiniz seçenek: {st.session_state.length_selection}")

            

                st.session_state.format_checkbox = st.checkbox('Alt Checkbox 2', value=st.session_state.format_checkbox,on_change=update_format_checkbox)

                if st.session_state.format_checkbox:
                    st.caption('İkinci özellik işaretlendi')

                    options_f = ["","",""]
                    st.session_state.format_selection_temp = st.radio(
                        "Bir seçenek seçin:",
                        options_f,
                        index = None if st.session_state.format_selection is None else options_f.index(st.session_state.format_selection),
                        key="2",on_change=update_format_selection
                    )
                    if st.session_state.format_selection:
                        st.caption(f"Seçtiğiniz seçenek: {st.session_state.format_selection}")
            




        with col3:
            preshow = st.container(border=True,height=400)

            preshow.write(" ")

            preshow.write("##### Your Character's Qualities")
            preshow.write(" ")
            preshow.caption("In this part you can see your selections.")
            #preshow.divider()
            if (len(name) <= max_chars) and (len(name) != 0):
                preshow.write(f"✨ Assistant's name is {name}")
            if sex == "Female":
                preshow.write(f"👩 {name} is a woman.")
            elif sex == "Male":
                preshow.write(f"👨 {name} is a man.")
            #else:
                #st.write("You did not enter its gender yet")

            if name and sex :
                preshow.write(f"{name} is {age} years old.")
            elif name == 0 and not sex :
                preshow.write(f"Assistant is {age} years old.")



            if len(st.session_state.selected_c_labels) != 0:
                if show_features == True:
                    preshow.write(f"{name} is: {', '.join(st.session_state.selected_c_labels)} ❗❗")
                elif show_features == False:
                    preshow.write(f"{name} is: {', '.join(st.session_state.selected_c_labels)}")
                    #st.write(f" {', '.join(selected_options)}")

            if len(st.session_state.backstory) != 0:
                preshow.write(f"🖊{name}'s backstory is: {st.session_state.backstory}")

            if st.button("Create Character",use_container_width=True,disabled=show):            
                    prompt_test=(f" You are not an assistant. At the beginning ask their name. Act like a human being and make an endless conversation. Your name is {name}, you are {age} years old {sex.lower()} with the following traits: {' ,'.join(st.session_state.selected_c_labels)}. Your backstory is {backstory}.")

                    #system_message = [{"role": "system", "content": prompt}]
                    #st.session_state.messages = [system_message]
                    add_message("system", prompt_test)


                    st.session_state.page = 'chat_page'
                    st.rerun()
                    #st.query_params(page='home')
            if st.button("Reset"):
                st.session_state.clear()
                st.rerun()


def add_message(role, content):
    if isinstance(role, str) and isinstance(content, str):
        st.session_state.messages.append({"role":role, "content": content})
    else:
        st.error("Invalid message format. Role and content must be strings.")
            

def show_chat_page():
    #st.session_state.page = 'chat_page'
    #st.header("👾 Prompt Creator Demo's Chatbot")
    #st.write(
    #            "In this page, you are able to ask whatever thing you want."
    #        )

    #if "messages" not in st.session_state:
    #    st.session_state.messages = []

    for message in st.session_state.messages:
        print(type(message),message)
        if isinstance(message, dict):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        elif isinstance(message, list) and len(message) == 2:
            with st.chat_message(message[0]):
                st.markdown(message[1])
        else:
            st.error("Invalid message format detected.")

    if prompt_test := st.chat_input("You can type here..."):
        st.session_state.messages.append({"role": "user", "content": prompt_test})
        with st.chat_message("user"):
            st.markdown(prompt_test)
        
        #response_text =""
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            response_text = response.choices[0].message.content.strip()

            if response_text:
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant"):
                    st.markdown(response_text)
            else:
                st.error("No response received from 'the assistant'.")

        except Exception as e:
            st.error(f"Error: {e}")

        #if response_text:
        #    st.session_state.messages.append({"role":"assistant", "content": response_text})
        #    with st.chat_message("assistant"):
        #        st.markdown(response_text)
        #else:
        #    st.error("No response recieved from the assistant.")


        #st.session_state.messages.append({"role": "assistant", "content": response_text})
        #with st.chat_message("assistant"):
        #    st.markdown(response_text)


    if st.button("Back"):
        st.session_state.messages = []
        st.session_state.page = 'home'
        st.rerun()
        #st.query_params(page='home')


if st.session_state.page == 'home':
    show_home_page()
else:
    show_chat_page()