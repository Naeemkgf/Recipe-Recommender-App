
import streamlit as st
import requests
from googleapiclient.discovery import build
from PIL import Image




# Function to get YouTube video recommendations
def get_youtube_videos(query):
    youtube = build("youtube", "v3", developerKey="AIzaSyBnXtSmCeJpN4b-pxfIi11QTdIj4N4x2l8")
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id",
        maxResults=1  # Number of videos to recommend
    ).execute()
    video_id = search_response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_url

# Function to display Recipe Details page
def recipe_details_page():
    st.title('App Details')
    # App Description
    st.markdown("Welcome to the Recipe Recommender App! This app is designed to help you discover and prepare delicious meals with the ingredients you have on hand.")
    image = Image.open('recipe.jpg')
    st.image(image, caption='Recipe')

    # Key Features
    st.header('Key Features')
    st.markdown("1. **Ingredient-Based Recommendations:** Enter the ingredients you have, and we'll recommend recipes you can make.")
    st.markdown("2. **Recipe Details:** Get step-by-step instructions, ingredient lists, and cooking times for each recommended recipe.")
    st.markdown("3. **Video Tutorials:** Watch video tutorials related to each recipe for visual guidance.")
   

    # How to Use
    st.header("How to Use")
    st.markdown("1. Navigate to the 'Recipe Recommender' page.")
    st.markdown("2. Enter the ingredients you have in your kitchen.")
    st.markdown("3. Click 'Recommend Recipes' to see a list of recipes you can prepare.")
    st.markdown("4. Select a recipe to view details, including step-by-step instructions, ingredients, and cooking times.")
    st.markdown("5. Watch video tutorials for additional guidance.")
   

# Function to display Recipe Recommender page
def recipe_recommender_page():
    st.title('Recipe Recommender App')
    

    col1, col2 = st.columns(2)

    # User input for ingredients
    with col1:
        user_input = st.text_area("Enter the ingredients you have (separated by commas)")

    # Check if the user has entered ingredients
    if user_input:
        # Convert user input into a list of ingredients
        user_ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

        # Call the Spoonacular API for recipe recommendations
        API_KEY = "45831b80631a4cedae4967cb57481b35"
        endpoint = "https://api.spoonacular.com/recipes/findByIngredients"

        params = {
            "apiKey": API_KEY,
            "ingredients": ','.join(user_ingredients),
            "number": 50  # Number of recipes to recommend
        }

        response = requests.get(endpoint, params=params)
        recipes = response.json()
        

        # Display recommended recipes
        with col2:
            st.write("Recommended Recipes:")
            for recipe in recipes:
                if st.button(recipe['title']):
                    st.write("###", recipe['title'])
                    st.image(recipe['image'], caption=recipe['title'], use_column_width=True)
                    st.write("Missing Ingredients:", ', '.join(ingredient['name'] for ingredient in recipe['missedIngredients']))
                    st.write("Used Ingredients:", ', '.join(ingredient['name'] for ingredient in recipe['usedIngredients']))
                    st.write("Instructions:", recipe.get('instructions', 'No instructions available'))

                    preparation_time = recipe.get('preparationMinutes', 'N/A')
                    cooking_time = recipe.get('cookingMinutes', 'N/A')
                    st.write("Preparation Time:", preparation_time)
                    st.write("Cooking Time:", cooking_time)
                    #implement the get_youtube_videos function here
                    video_url = get_youtube_videos(recipe['title'])
                    st.write("Tutorial Video:", video_url)

                    st.write("-" * 50)

# Function to display About the Creator page
def about_the_creator_page():
    st.title('About the Creator')
    # Creator's Information
    st.markdown("This app was created by Naeem Bozdar, a passionate food enthusiast and software developer.")
    st.markdown("Feel free to connect with the creator to share your thoughts or ask questions about the app.")


    st.subheader(' Social Media Links')
    SOCIAL_MEDIA = {
    "Fiverr":"https://www.fiverr.com/my_profile",
    "LinkedIn": "https://linkedin.com",
    "GitHub": "https://github.com",
    "Kaggel": "https://www.kaggle.com",
}
    
    # --- SOCIAL LINKS ---
    st.write('\n')
    cols = st.columns(len(SOCIAL_MEDIA))
    for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
        cols[index].write(f"[{platform}]({link})")

    
    st.write('\n')
    st.write('\n')
    # Support and Feedback
    st.header("Support and Feedback")
    st.markdown("If you have any questions, feedback, or encounter issues while using the app, please reach out to us.")
    st.markdown("For support and inquiries, contact us at [naeembozdar2005@gmail.com].")
    st.markdown("We value your feedback and are constantly working to improve your recipe-finding experience.")
     


# Main function to handle page navigation
def main():
    st.set_page_config(page_title='Recipe Recommand App',layout="wide")

    # Create a sidebar with navigation links
    page = st.sidebar.radio("Select Page", ("Recipe Details", "Recipe Recommender", "About the Creator"))

    # Display the selected page based on user's choice
    if page == 'Recipe Details':
        recipe_details_page()
    elif page == 'Recipe Recommender':
        recipe_recommender_page()
    elif page == 'About the Creator':
        about_the_creator_page()

if __name__ == '__main__':
    main()
