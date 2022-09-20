# What's for Dinner?

![image](https://user-images.githubusercontent.com/108480012/191253097-13373e0d-f527-444b-b85b-5c86be9299c5.png)

What's for Dinner is an ingredients-to-recipes recommender, that works by taking a user-submitted image, classifying it, and then looking up and returning information from a recipes dataset.

## User Journey

1. The user uploads a photgraph of a food item (fruit / vegetable for now) via a Streamlit web application hosted on Heroku
2. The user receives the classification result
3. The user chooses the number of recipes to briefly view
4. The user views the titles and descriptions of recipes
5. The user makes the final choice of recipe to fully view
6. The user is shown a full list of ingredients and steps

## High Level Architecture
<img width="1256" alt="Screen Shot 2022-09-20 at 21 48 17" src="https://user-images.githubusercontent.com/78719850/191281578-11b7fb72-589c-467a-970c-eb6d2e80b100.png">


## Data Sources

![image](https://user-images.githubusercontent.com/108480012/191256267-5bd21d51-d097-4071-8c4e-792b5073678b.png)

- Recipes: 500,000+ recipes from [Food.com Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews),

- Images: ~38.921 photos of fruits and vegetables (4.75GB) our own custom sourced image dataset augmented with images.cv and also the [Fruits and Vegetables Image Recognition Dataset](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition)

## Contributors
This was created as part of the final project in Le Wagon Data Science bootcamp (batch #991), with the following contributors (listed alphabetically):
- [Clara Gholani](https://github.com/Clara31100)
- [Ibrahim Hazm Bin Amran](https://github.com/hazmmmm/)
- [Ido Azaria](https://github.com/IdoKun)
- [Viktor Chmilenko]()

![image](https://user-images.githubusercontent.com/108480012/191254761-766bfbf1-cecc-4519-b7b0-b6de66558cb0.png)

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
