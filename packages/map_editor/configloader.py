import yaml 

def get_duckietown_types():
    with open('./doc/apriltagsDB.yaml') as file:
        content = yaml.load(file)
        types = {}
        for tag in content:
            if not tag["tag_type"]:
                continue
            if tag["tag_type"] not in types.keys():
                types[tag["tag_type"]] = []
            types[tag["tag_type"]].append(tag["tag_id"])
                
        return types