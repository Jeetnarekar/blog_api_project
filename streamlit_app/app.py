import streamlit as st
import requests

# Base URL of FastAPI
BASE_URL = "http://127.0.0.1:8000"

# --- Helper Functions ---

def register(username, email, password):
    url = f"{BASE_URL}/users/register"
    data = {"username": username, "email": email, "password": password}
    return requests.post(url, json=data).json()

def login(email, password):
    url = f"{BASE_URL}/users/login"
    data = {"username": email, "password": password}  # username instead of email
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(url, data=data, headers=headers).json()

def get_posts(token):
    url = f"{BASE_URL}/posts"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers).json()

def create_post(token, title, content, published=True):
    url = f"{BASE_URL}/posts"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": title, "content": content, "published": published}
    return requests.post(url, headers=headers, json=data).json()

def delete_post(token, post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.delete(url, headers=headers).json()


# --- Streamlit App ---

st.title("📚 Blog App (FastAPI + Streamlit)")

menu = ["Login", "Register", "View Posts", "Create Post"]
choice = st.sidebar.selectbox("Menu", menu)

if "token" not in st.session_state:
    st.session_state.token = None

# --- Register ---
if choice == "Register":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = register(username, email, password)
        st.write(response)

# --- Login ---
elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = login(email, password)
        st.write("Login payload:", {"email": email, "password": password})
        if "access_token" in response:
            st.session_state.token = response["access_token"]
            st.success("Logged in successfully!")
        else:
            st.error(response.get("detail", "Login failed"))

# --- View Posts ---
elif choice == "View Posts":
    st.subheader("All Blog Posts")
    if st.session_state.token is None:
        st.warning("Please login first")
    else:
        posts = get_posts(st.session_state.token)
        for post in posts:
            st.markdown(f"### {post['title']}")
            st.markdown(post['content'])
            st.write(f"Published: {post['published']} | ID: {post['id']} | User ID: {post['user_id']}")
            if st.button(f"Delete Post {post['id']}"):
                delete_resp = delete_post(st.session_state.token, post['id'])
                st.write(delete_resp)
                st.rerun()

# --- Create Post ---
elif choice == "Create Post":
    st.subheader("Create a New Post")
    if st.session_state.token is None:
        st.warning("Please login first")
    else:
        title = st.text_input("Title")
        content = st.text_area("Content")
        published = st.checkbox("Published", value=True)

        if st.button("Create Post"):
            response = create_post(st.session_state.token, title, content, published)
            st.write(response)
            st.rerun()
            