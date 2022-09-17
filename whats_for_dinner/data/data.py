import os
import numpy as np
import pandas as pd
from whats_for_dinner.ml_logic.params import RUN_TYPE


csv_path2 = "./whats_for_dinner/data/recipes_cleaned.csv"

if RUN_TYPE == 'local':
    csv_path2 = os.path.join(os.environ.get("LOCAL_DATA_PATH"),'recipes_cleaned.csv')
# if RUN_TYPE == 'docker':
#     csv_path2 = ('./whats_for_dinner/data/recipes_cleaned.csv')

# Load dataframe with cleaned recipes
recipes_cleaned = pd.read_csv(csv_path2)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # Remove useless/redundant columns and reorganize
    recipe_cols = [
        "Name",
        "AuthorName",
        "AggregatedRating",
        "ReviewCount",
        "Description",
        "RecipeCategory",
        "TotalTime",
        "CookTime",
        "PrepTime",
        "Calories",
        "RecipeIngredientParts",
        "RecipeInstructions",
        "Images",
    ]

    df = df[recipe_cols]

    # Remove missing values transactions
    recipes_cleaned = df.drop_duplicates()
    recipes_cleaned.CookTime.replace(np.nan, "0M", inplace=True)
    recipes_cleaned.ReviewCount.replace(np.nan, 0, inplace=True)
    recipes_cleaned.RecipeCategory.replace(np.nan, "Others", inplace=True)
    recipes_cleaned.Description.replace(np.nan, "No description", inplace=True)
    recipes_cleaned = recipes_cleaned.dropna(subset=["Images"])

    # remove
    recipes_cleaned = recipes_cleaned.dropna(subset=["AggregatedRating"])
    recipes_cleaned = recipes_cleaned[recipes_cleaned.AggregatedRating > 3]

    # time cleaning
    recipes_cleaned["CookTime"] = recipes_cleaned["CookTime"].str.replace("PT", "")
    recipes_cleaned["PrepTime"] = recipes_cleaned["PrepTime"].str.replace("PT", "")
    recipes_cleaned["TotalTime"] = recipes_cleaned["TotalTime"].str.replace("PT", "")

    print("\n✅ data cleaned")

    return recipes_cleaned


def score_recipes(user_input, best_num):
    """
    Function to return a dataframe with a <best_num> number of recipes, based
    on an ingredient choice of <user_input>.
    user_input: list of strings
    df: our list of recipes
    best_num: number of results to return
    """
    df = recipes_cleaned

    def score(ingredient_list):  # the score will provide the best related recipes
        """
        Function to score recipes based on number of ingredients
        matching user requests
        """
        score = 0
        for ingredient in user_input:
            if ingredient in ingredient_list:
                score += 1
        return score


    df["score"] = df["RecipeIngredientParts"].apply(lambda x: score(x))
    df = df.sort_values(
        by=["score", "AggregatedRating"], ascending=[False, False]
    ).iloc[:best_num]

    return df[
        [
            "Name",
            "AuthorName",
            "AggregatedRating",
            "ReviewCount",
            "Description",
            "RecipeCategory",
            "TotalTime",
            "CookTime",
            "PrepTime",
            "Calories",
            "RecipeIngredientParts",
            "RecipeInstructions",
        ]
    ]
