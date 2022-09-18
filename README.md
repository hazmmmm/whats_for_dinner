# What's for Dinner?

What's for Dinner is an ingredients-to-recipes recommender, which works by taking a user-submitted image, classifying it, and then looking up and returning information from a recipes dataset.

This was created as part of the final project in a Le Wagon Data Science bootcamp, with the following contributors (listed alphabetically):

- Clara Gholani
- Ibrahim Hazm Bin Amran
- Ido Azaria
- Viktor Chmilenko

## User Journey

1. The user uploads a photgraph of a food item (fruit / vegetable for now) via a Streamlit web application hosted on Heroku
2. The user receives the classification result
3. The user chooses the number of recipes to briefly view
4. The user views the titles and descriptions of recipes
5. The user makes the final choice of recipe to fully view
6. The user is shown a full list of ingredients and steps

## High Level Architecture

## Data Sources

- Recipes: 500,000+ recipes from [Food.com Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews),

- Images: ~3,600 photos of fruits and vegetables (2+GB) from [Fruits and Vegetables Image Recognition Dataset](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition)

# Startup the project

The initial setup.

Create virtualenv and install the project:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:

```bash
make clean install test
```

Check for whats_for_dinner in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/whats_for_dinner`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "whats_for_dinner"
git remote add origin git@github.com:{group}/whats_for_dinner.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
whats_for_dinner-run
```

# Install

Go to `https://github.com/hazmmmm/whats_for_dinner` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:hazmmmm/whats_for_dinner.git
cd whats_for_dinner
pip install -r requirements.txt
make clean install test                # install and test
```

Functional test with a script:

```bash
cd
mkdir tmp
cd tmp
whats_for_dinner-run
```
