from core import Robot, State

class Debug:
    """
        This class is intended to use Window Class so that it
        is possible to debug some variables (ex. State, Emotion, etc)
        This class will also provide heads on debugging, so it is
        not necessary to code everything from scratch every time it is
        intented to debug
    """

    labels = []
    sliders = []
    y_position = 120

    def add_label(self, name:str, variable:float, display:bool):

        for label in self.labels:
            if label["name"] == name:
                label["value"] = variable
                return

        Debug.y_position += 40
        self.labels.append({'name':name,'value':variable,'display':display, 'position':Debug.y_position})
        return

    def list_labels(self):
        for label in self.labels:
            print(f'{label["name"]}: {label["value"]}')
        return

    def all_labels(self):
        return self.labels

    def add_slider(self, name:str, value:list, upperValue:float, downValue:float, step:float ):

        for slide in self.sliders:
            if slide["name"] == name:
                slide["value"] = value
                return

        Debug.y_position += 60
        self.sliders.append({'name':name,'value':value,
                            'upperValue':upperValue, 'downValue':downValue, 'step':step,'position':Debug.y_position})
        return

    def list_sliders(self):
        for slider in self.sliders:
            print(f'{slider["name"]}: {slider["value"]}')
        return

    def all_sliders(self):
        return self.sliders
