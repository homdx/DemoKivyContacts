from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty


class CallContact(FloatLayout):
    callback = ObjectProperty(lambda: None)
    avatar = StringProperty(None)
    name_contact = StringProperty(None)
    number_contact = StringProperty(None)

