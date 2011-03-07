class LogglyInput(object):
    def __init__(self, attributes):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])
    
    def __repr__(self):
        return "Input:%s" % self.name
