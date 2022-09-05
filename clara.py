import numpy as np
import pandas as pd
import os


#TO UPDATE url = 'https://sample.com/file.csv'
#recipes_df = pd.read_csv(url)
csv_path = os.path.join('raw_data','food_dot_com')
csv_path
recipes_df = pd.read_csv(os.path.join(csv_path, 'recipes.csv'))
recipes_df.head()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns
    recipe_cols = ['RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime', 'Description', 'Images',\
              'RecipeCategory', 'RecipeIngredientParts', \
              'AggregatedRating','ReviewCount', 'Calories', 'RecipeInstructions','AuthorName']
    
    rp_df = df[recipe_cols]

    # remove missing values transactions
    df = df.drop_duplicates()
    rp_df.CookTime.replace(np.nan, '0M', inplace=True)
    rp_df.AggregatedRating.replace(np.nan, 'Norating', inplace=True)
    rp_df.ReviewCount.replace(np.nan,0, inplace=True)
    rp_df.RecipeCategory.replace(np.nan, 'Others', inplace=True)
    rp_df.Description.replace(np.nan, 'No description', inplace=True)
    rp_df = rp_df.dropna(subset = ['Images'])
    
    #time cleaning
    rp_df['CookTime'] = rp_df['CookTime'].str.replace('PT','')
    rp_df['PrepTime'] = rp_df['PrepTime'].str.replace('PT','')
    rp_df['TotalTime'] = rp_df['TotalTime'].str.replace('PT','')


    #reorganize columns
    recipes_cleaned = rp_df.drop(columns=['RecipeId'])
    recipes_cleaned = recipes_cleaned[['Name','AuthorName','AggregatedRating','ReviewCount','Description','RecipeCategory','TotalTime','CookTime','PrepTime','Calories','RecipeIngredientParts','RecipeInstructions','Images']]
    

    print("\n✅ data cleaned")

    return recipes_cleaned

def score_recipes(user_input, df, best_num):
    pass
     '''
    user_input: list of strings
    df: our list of recipes
    best_num: number of best matching result to return
    '''
    df = recipes_cleaned.copy()
    
    def score(ingredient_list):
        score = 0
        for w in user_input:
            if w in ingredient_list:
                score += 1
        return score
    
    df['score'] = df['RecipeIngredientParts'].apply(lambda x: score(x))
    df = df.sort_values(by='score', ascending=False).iloc[:best_num] #this is sorted bycorresponding score (not only the rating)
    return df

    