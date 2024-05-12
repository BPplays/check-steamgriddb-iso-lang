import requests
from api_info import key
import signal
import sys
from lang import iso_languages

def append_non_duplicates(arr1, arr2):
    unique_elements = set(arr1)
    for item in arr2:
        if item not in unique_elements:
            arr1.append(item)
            unique_elements.add(item)


def print_lang():
	print ()
	print ("=========")
	print("ISO Languages Matched:", f'{len(iso_languages_matched)}/184', iso_languages_matched)
	print("Non-ISO Languages:", non_iso_languages)
	print ("=========")
	print ()


def signal_handler(sig, frame):
    print('Exiting gracefully...')
    print_lang()
    # Perform cleanup operations here if needed
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def is_valid_language_code(input_code):
	for code, _ in iso_languages:
		if input_code == code:
			return True
	return False

def check_language(game_id, api_key, type):
	url = f'https://www.steamgriddb.com/api/v2/{type}/game/{game_id}'
	headers = {'Authorization': f'Bearer {api_key}'}
	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		data = response.json()
		iso_languages_matched = []
		non_iso_languages = []

		for game_data in data['data']:
			language = game_data['language']
			if is_valid_language_code(language):
				iso_languages_matched.append(language)
			else:
				non_iso_languages.append(language)

		return iso_languages_matched, non_iso_languages
	else:
		return None, None



apiopts = ["logos", "heroes", "grids" , "icons"]

# Example game ID and API key
game_id = 5361043
# game_id = 5361
api_key = key

if len(iso_languages) != 184:
	print("err iso_languages")
	print(len(iso_languages))
	sys.exit(1)

iso_languages_matched = []
non_iso_languages = []

to_disp_full = 0

while len(iso_languages_matched) < 184:
	for type in apiopts:
		iso_languages_matched_tmp, non_iso_languages_tmp = check_language(game_id, api_key, type)

		if (iso_languages_matched_tmp is not None) and (len(iso_languages_matched_tmp) != 0):
			to_disp_full -= 1
			append_non_duplicates(iso_languages_matched, iso_languages_matched_tmp)
			print(iso_languages_matched_tmp)
	
		if (non_iso_languages_tmp is not None) and (len(non_iso_languages_tmp) != 0):
			to_disp_full -= 1
			append_non_duplicates(non_iso_languages, non_iso_languages_tmp)
			print(non_iso_languages_tmp)
	
		if to_disp_full < 0:
			to_disp_full = 50
			print_lang()

	game_id -= 1
 

	
	# test = game_id
	# if test +5 >= game_id:
	# 	break
	
	
 

if iso_languages_matched is not None:
	print_lang()
else:
	print("Failed to retrieve data from the API.")