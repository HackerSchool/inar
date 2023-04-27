class Debug:
    """
        This class is intended to use Window Class so that it
        is possible to debug some variables (ex. State, Emotion, etc)
        This class will also provide heads on debugging, so it is
        not necessary to code everything from scratch every time it is
        intented to debug
    """

    def __init__(self):
        self.labels = []
        self.sliders = []

    def add_label(self, name:str, variable:float, display:bool):
        self.labels.append({'name':name,'value':variable,'display':display})

    def list_labels(self):
        for label in self.labels:
            print(f'{label.name}: {label.value}')

    def add_slider(self, name:str, options:list, display:bool ):
        self.sliders.append({'name':name,'value':options,'display':display})
        pass

    def list_sliders(self):
        for slide in self.sliders:
            print(f'{slide.name}: ')
            for option in slide.options:
                print(f'* {option.name}')
