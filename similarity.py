import joblib
import string
import re
import textdistance
import random

class FinalProject(object):
	def __init__(self, model, dataset):
		self.__model = joblib.load(model)
		self.__dataset = joblib.load(dataset)

	def _predict(self, masukan):
		if isinstance(masukan, list):
			return self.__model.predict(masukan)
		else:
			raise TypeError

	def __lv(self, masukan):
		if isinstance(masukan, dict):
			categorized_messages = list(enumerate(self.categorized_messages(masukan.get('category'))))
			return list(enumerate([textdistance.levenshtein.normalized_distance(masukan.get('processed'), 
				message[1]['message']) for message in categorized_messages]))
		else:
			raise TypeError

	def __sorted_lv(self, _):
		return sorted(_, key=lambda x:x[1])

	@classmethod
	def default(cls):
		return cls('model.fp1', 'dataset.fp1')

	def predict_category(self, x):
		if isinstance(x, str):
			return self._predict([x])[0]
		else:
			raise TypeError

	def categorized_messages(self, category):
		return [message for message in self.__dataset if message.get('category') == category]

	def predict(self, x, n):
		x['category'] = self.predict_category(x['processed'])
		categorized_messages = list(enumerate(self.categorized_messages(x['category'])))
		_  = self.__sorted_lv(self.__lv(x))
		return [categorized_messages[lv[0]][1] for lv in _[:n]]

if __name__ == '__main__':
	while True:
		fp = FinalProject.default()
		masukan_helper = input("Pesan: ")
		masukan = {
			'raw_input' : masukan_helper,
			'processed' : re.sub('['+string.punctuation+']', "", re.sub(r"[0-9]", "", masukan_helper.casefold()))
		}

		top = fp.predict(masukan, 2)
		selected = random.choice(top)

		print(f"Respon: {selected.get('response')}")
		
		print(fp.predict(masukan,2)) # Digunakan untuk melihat message apa saja yang mendekati

		# print(f"Pesan asli: \"{selected.get('message')}\"")

		# for message in top:
		# 	print(message)
		# 	print(f"Pesan: \"{message.get('message')}\", Respon: \"{message.get('response')}\"")



