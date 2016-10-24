from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty


class CallContact(FloatLayout):
    callback = ObjectProperty(lambda: None)
    avatar = StringProperty(None)
    name_contact = StringProperty(None)
    number_contact = StringProperty(None)
    size_avatar = ListProperty(150, 150)

