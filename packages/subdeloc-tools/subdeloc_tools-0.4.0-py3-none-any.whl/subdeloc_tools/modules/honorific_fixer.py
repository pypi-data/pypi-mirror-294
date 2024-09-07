import pysubs2

def load_ass(file_path):
    try:
        subs = pysubs2.load(file_path)
        return subs
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        return None

def prepare_edit_dict(dt):
	result = {}
	for i in dt:
		for j in i["original"]:
			result[str(j["nl"])] = j["text"]

	return result

def fix_original(file, fixed, new_name="edited.ass"):
	try:
		subs = load_ass(file)
		res = prepare_edit_dict(fixed)

		ks = res.keys()

		for nl,line in enumerate(subs):
			if str(nl) in ks:
				line.text = res[str(nl)]

		subs.save(new_name)
	except Exception as e:
		print(e)
