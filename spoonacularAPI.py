import requests
import json
from fuzzywuzzy import process as fp


####### TMP ########
CRED = {
	'X-Mashape-Key': "00c975NnVDmshPmrTwW4UqKNAWCap1GN1Fvjsnv1uIL1kTRiVo",
    'Accept': "application/json",
}


def match_input(input_): #this function matches the input from Remi to the available options in spoonacular

	diet_options = ['pescetarian', 'lacto vegetarian', 'ovo vegetarian', 'vegan', 'paleo', 'primal', 'vegetarian']
	intolerance_options = ['dairy', 'egg', 'gluten', 'peanut', 'sesame', 'seafood', 'shellfish', 'soy', 'sulfite', 'treenut', 'wheat']


	# type_options = ['main course', 'side dish', 'dessert', 'appetizer', 'salad', 'bread', 'breakfast', 'soup', 'beverage', 'sauce', 'drink']
	# cuisine_options = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican', 'spanish', 
	# 	'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']

	matched_diet = []
	matched_intolerance = []

	for var in input_['diet']:
		m_diet = fp.extractOne(var, diet_options)
		m_intolerance = fp.extractOne(var, intolerance_options)

		if m_diet[1] > 75:
			matched_diet.append(m_diet[0])
		if m_intolerance[1] > 75:
			matched_intolerance.append(m_intolerance[0])
		if m_diet[1] <= 75 and m_intolerance[1]<= 75:
			input_['food'] = var+' '+input_['food']

	input_.update({'diet': ','.join(matched_diet), 'intolerance': ','.join(matched_intolerance)})

	input_['Ingredients'] =','.join(input_['Ingredients'])
	return input_

def spoonacular_API(matched_input):

	headers = {}
	headers.update(CRED)

	endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/searchComplex'
	query = {
		'query': matched_input['food'],
		'includeIngredients': matched_input['ingredients'],
		'diet': matched_input['diet'],
		'intolerance': matched_input['intolerance'],
		'number' : 10,	#number of results
		'ranking' : 1, #Whether to maximize used ingredients (1) or minimize missing ingredients (2) first.
		'offset' : 0, #the number of results to skip
	}

	response = requests.get(endpoint, headers = headers, params = query)
	return json.loads(response.text)


def get_nutrition(id_):
	headers = {}
	headers.update(CRED)
	endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information'.format(str(id_))
	search = {
		'includeNutrition': True,
	}
	response = requests.get(endpoint, headers = headers, params = search)
	return (response.text)


def get_instruction(id_):
	headers = {}
	headers.update(CRED)
	endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/analyzedInstructions'.format(str(id_))
	search = {
		'stepBreakdown': True,
	}
	response = requests.get(endpoint, headers = headers, params = search)
	return response.text


if __name__ == '__main__':
	#sample input
	input_ = {
		'food' : 'chicken burger',

		'diet' : ['vegan','no peanut','no watermalon'],
		'Ingredients' : ['onions', 'lettuce'],

		# 'cuisine' : 'american',
		# 'type': 'main course',
		# 'fillIngredients': None,
		# 'limitLicense' : False, #Whether the recipes should have an open license that allows for displaying with proper attribution.
		# 'maxCalories' : None,
		# 'maxCarbs' : None,
		# 'maxFat' : None,
		# 'maxProtein' : None,
		# 'minClories' : None,
		# 'minCarbs' : None,
		# 'minFat' : None,
		# 'minProtein' : None,
	}

	print match_input(input_)
	# data = spoonacular_API(match_input(input_))

	# try:
	# 	for result in data['results']:
	# 		print ('title: %s\nresult id: %s, \nused ingredients count: %s\nmissed ingredients count: %s' %(result['title'],result['id'],result['usedIngredientCount'],result['missedIngredientCount']))
	# 		print ('====================')
	# except TypeError:
	# 	for result in data:
	# 		print ('title: %s\nresult id: %s, \nused ingredients count: %s\nmissed ingredients count: %s' %(result['title'],result['id'],result['usedIngredientCount'],result['missedIngredientCount']))
	# 		print ('====================')




