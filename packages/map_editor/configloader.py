import yaml 

def get_duckietown_types():
    with open('./doc/configApriltags.yaml') as file:
        content = yaml.load(file)
        return content