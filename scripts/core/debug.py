from core import Robot, State

class Debug:
    """
        This class is intended to use Window Class so that it
        is possible to debug some variables (ex. State, Emotion, etc)
        This class will also provide heads on debugging, so it is
        not necessary to code everything from scratch every time it is
        intented to debug
    """

    def __init__(self, _robot:Robot, _state:State):
        self.robot = _robot
        self.state = _state

        self.labels = []
        self.sliders = []
        self.y_position = 150

    def add_label(self, name:str, variable:float, display:bool):
        self.labels.append({'name':name,'value':variable,'display':display, 'position':self.y_position})
        self.y_position += 50

    def list_labels(self):
        for label in self.labels:
            print(f'{label.name}: {label.value}')

    def all_labels(self):
        return self.labels
    
    def updateLabel(self):
        # Create thread that listens and updates
        # the values of the variable
        pass

    def add_slider(self, name:str, options:list, upperValue:float, downValue:float, step:float ):
        self.sliders.append({'name':name,'value':options,
                            'upperValue':upperValue, 'downValue':downValue, 'step':step})
        return

    def list_sliders(self):
        pass

    def all_sliders(self):
        pass
