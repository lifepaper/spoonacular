import requests
import json
from fuzzywuzzy import process as fp


####### TMP ########
CRED = {
	'X-Mashape-Key': "00c975NnVDmshPmrTwW4UqKNAWCap1GN1Fvjsnv1uIL1kTRiVo",
    'Accept': "application/json",
}


def match_input(input_): #this function matches the input from Remi to the available options in spoonacular
	cuisine_options = ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican', 'spanish', 
		'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
	diet_options = ['pescetarian', 'lacto vegetarian', 'ovo vegetarian', 'vegan', 'paleo', 'primal', 'vegetarian']
	intolerance_options = ['dairy', 'egg', 'gluten', 'peanut', 'sesame', 'seafood', 'shellfish', 'soy', 'sulfite', 'tree nut', 'wheat']
	type_options = ['main course', 'side dish', 'dessert', 'appetizer', 'salad', 'bread', 'breakfast', 'soup', 'beverage', 'sauce', 'drink']

	matched_diet = []
	
	if input_['diet']:
		for variable in input_['diet']:
			match = fp.extractOne(variable, diet_options)
			if match[1] > 75:
				matched_diet.append(match[0])
				input_['diet'].remove(variable)

	matched_intolerance = []
	if input_['intolerance']:
		for variable in input_['intolerance']:
			match = fp.extractOne(variable, intolerance_options)
			if match[1] > 75:
				matched_intolerance.append(match[0])
				input_['intolerance'].remove(variable)

	final_query_list = []
	if input_['cuisine']:
		match = fp.extractOne(input_['cuisine'], cuisine_options)
		if match[1] > 75:
			input_['cuisine'] = match[0]
		else:
			final_query_list.append(input_['cuisine'])
			input_['cuisine'] = None

	if input_['type']:
		match = fp.extractOne(input_['type'], type_options)
		if match[1] > 75:
			input_['type'] = match[0]
		else:
			final_query_list.append(input_['type'])
			input_['type'] = None


	final_query_list = input_['intolerance'] + input_['diet'] + [input_['query']]
	if input_['query']:
		input_['query'] = ' '.join(final_query_list)

	input_.update({'diet': ','.join(matched_diet), 'intolerance': ','.join(matched_intolerance)})

	input_['excludeIngredients'] = ','.join(input_['excludeIngredients'])
	input_['includeIngredients'] =','.join(input_['includeIngredients'])

	return input_

def spoonacular_API(matched_input):

	headers = {}
	headers.update(CRED)

	if matched_input['query']:
		endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/searchComplex'
		search = { #search content with some 4 default values
			'number' : 10,	#number of results
			'ranking' : 1, #Whether to maximize used ingredients (1) or minimize missing ingredients (2) first.
			'offset' : 0, #the number of results to skip

			'cuisine' : None,
			'diet' : None,
			'excludeIngredients' : None,
			'fillIngredients': None,
			'includeIngredients' : None,
			'intolerance' : None,
			'limitLicense' : False, #Whether the recipes should have an open license that allows for displaying with proper attribution.
			'maxCalories' : None,
			'maxCarbs' : None,
			'maxFat' : None,
			'maxProtein' : None,
			'minClories' : None,
			'minCarbs' : None,
			'minFat' : None,
			'minProtein' : None,
			'type' : None,
		}
		search.update(matched_input)

	elif matched_input['includeIngredients']:
		endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients'
		search = {
			'ingredients' : matched_input['includeIngredients'],
			'fillIngredients': False,
			'limitLicense': False,
			'number': 10,
			'ranking': 1,
		}



	response = requests.get(endpoint, headers = headers, params = search)
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
		'query' : None,

		'diet' : ['vegan'],
		'intolerance' : ['peanut'],

		'excludeIngredients' : ['coconut'],
		'includeIngredients' : ['onions', 'lettuce'],

		'cuisine' : 'american',
		'type': 'main course',
	}
	data = spoonacular_API(match_input(input_))
	try:
		for result in data['results']:
			print ('title: %s\nresult id: %s, \nused ingredients count: %s\nmissed ingredients count: %s' %(result['title'],result['id'],result['usedIngredientCount'],result['missedIngredientCount']))
			print ('====================')
	except TypeError:
		for result in data:
			print ('title: %s\nresult id: %s, \nused ingredients count: %s\nmissed ingredients count: %s' %(result['title'],result['id'],result['usedIngredientCount'],result['missedIngredientCount']))
			print ('====================')




