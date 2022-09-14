import numpy as np
import pandas as pd
import os
from whats_for_dinner.ml_logic.params import RUN_TYPE


#TO UPDATE url = 'https://sample.com/file.csv'
#recipes_df = pd.read_csv(url)
#csv_path = os.path.join('raw_data','food_dot_com')
#recipes_df = pd.read_csv(os.path.join(csv_path, 'recipes.csv'))


if RUN_TYPE == 'local':
    csv_path2 = os.path.join(os.path.expanduser(os.environ.get("LOCAL_DATA_PATH")),'recipes_cleaned.csv')
if RUN_TYPE == 'docker':
    csv_path2 = ('whats_for_dinner/data/recipes_cleaned.csv')


recipes_cleaned = pd.read_csv(csv_path2)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """

    # remove useless/redundant columns and reorganize
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

    # remove missing values transactions
    recipes_cleaned = df.drop_duplicates()
    recipes_cleaned.CookTime.replace(np.nan, "0M", inplace=True)
    recipes_cleaned.ReviewCount.replace(np.nan, 0, inplace=True)
    recipes_cleaned.RecipeCategory.replace(np.nan, "Others", inplace=True)
    recipes_cleaned.Description.replace(np.nan, "No description", inplace=True)
    recipes_cleaned = recipes_cleaned.dropna(subset=["Images"])


    #remove
    recipes_cleaned = recipes_cleaned.dropna(subset=["AggregatedRating"])
    recipes_cleaned = recipes_cleaned[recipes_cleaned.AggregatedRating > 3]


    # time cleaning
    recipes_cleaned["CookTime"] = recipes_cleaned["CookTime"].str.replace("PT", "")
    recipes_cleaned["PrepTime"] = recipes_cleaned["PrepTime"].str.replace("PT", "")
    recipes_cleaned["TotalTime"] = recipes_cleaned["TotalTime"].str.replace("PT", "")


    print("\n✅ data cleaned")

    return recipes_cleaned


def score_recipes(user_input=input("What should it include? "),
best_num=(int(input("How many recipes you want? "))),
more_filters=input("Did you want more filters? Y | N: ")):
    '''
    user_input: list of strings
    df: our list of recipes
    best_num: number of best matching result to return
    more_filter: ask user if he want to have more filters
    '''
    df = recipes_cleaned

    def time_converter(x):
        if "0S" in x:
            return 0

        if "H" in x:
            one = x.replace("H", " * 60 + ")
            two = one.replace("M", "")
            if two[-2:] == "+ ":
                two = two.replace("+ ", "")
            three = str(eval(two))

            return three

        return x.replace("M", "")


    if more_filters.lower() == "y" or "yes":
        print("🚀 Adding more filters")
        filters = input("Choose filters you want to use: ReviewCount, TotalTime(number must be in minutes), Calories (sign and number: > or <, use a comma between filters): ").split(",")

        added = "NotWork"
        for filter in filters:
            filter = filter.split()
            try:
                if filter[0].lower() == "ReviewCount".lower():
                    df = eval(f"df[df['ReviewCount'] {filter[1]} {filter[2]}]")
                    added = "Work"

                if filter[0].lower() == "Calories".lower():
                    df = eval(f"df[df['Calories'] {filter[1]} {filter[2]}]")
                    added = "Work"

                if filter[0].lower() == "TotalTime".lower():
                    df[["TotalTime"]] = df[["TotalTime"]].applymap(lambda x: time_converter(x))
                    df["TotalTime"] = pd.to_numeric(df["TotalTime"])
                    df = eval(f"df[df['TotalTime'] {filter[1]} {filter[2]}]")
                    df[["TotalTime"]] = df[["TotalTime"]].applymap(lambda x: str(x) + "M")
                    added = "Work"

            except:
                print("No filters added, invalid input format.🤖")

        if added == "NotWork":
            print("No filters added, invalid input format.🤖")

    def score(ingredient_list): #the score will provide the best related recipes
        score = 0
        for w in user_input:
            if w in ingredient_list:
                score += 1
            return score

    df['score'] = df['RecipeIngredientParts'].apply(lambda x: score(x))
    df = df.sort_values(by=['score','AggregatedRating'], ascending=[False,False]).iloc[:best_num]

    return df


food_label = {
    0: "apple",
    1: "banana",
    2: "beetroot",
    3: "bell pepper",
    4: "cabbage",
    5: "capsicum",
    6: "carrot",
    7: "cauliflower",
    8: "chilli pepper",
    9: "corn",
    10: "cucumber",
    11: "eggplant",
    12: "garlic",
    13: "ginger",
    14: "grapes",
    15: "jalepeno",
    16: "kiwi",
    17: "lemon",
    18: "lettuce",
    19: "mango",
    20: "onion",
    21: "orange",
    22: "paprika",
    23: "pear",
    24: "peas",
    25: "pineapple",
    26: "pomegranate",
    27: "potato",
    28: "radish",
    29: "soy beans",
    30: "spinach",
    31: "sweetcorn",
    32: "sweet potato",
    33: "tomato",
    34: "turnip",
    35: "watermelon",
}
