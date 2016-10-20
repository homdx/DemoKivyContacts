from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty


class EmptyScreen(FloatLayout):
    callback = ObjectProperty(lambda: None)
    image = StringProperty()
    text = StringProperty()
    disabled = BooleanProperty()

