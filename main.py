from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from kivy.utils import get_color_from_hex
from kivy.core.window import Window, Keyboard


class BaseWidget(Widget):
	def load_tileable(self, name):
		t = Image('media/{}.png'.format(name)).texture
		t.wrap = 'repeat'
		setattr(self, 'tx_{}'.format(name), t)

class Background(BaseWidget):
	tx_floor = ObjectProperty(None)
	tx_grass = ObjectProperty(None)
	tx_cloud = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Background, self).__init__(**kwargs)
		for name in ('floor', 'grass', 'cloud'):
			self.load_tileable(name)

	def set_background_size(self, tx):
		tx.uvsize = (self.width / tx.width, -1)
	
	def on_size(self, *args):
		for tx in (self.tx_floor, self.tx_grass, self.tx_cloud):
			self.set_background_size(tx)
	
	def update(self, nap):
		self.set_background_uv('tx_floor', 2 * nap)
		self.set_background_uv('tx_grass', 0.5 * nap)
		self.set_background_uv('tx_floor', 0.1 * nap)

	def set_background_uv(self, name, val):
		t = getattr(self, name)
		t.uvpos = ((t.uvpos[0] + val) % self.width, t.uvpos[1])
		self.property(name).dispatch(self)


class AlienTecApp(App):
	def on_start(self):
		self.background = self.root.ids.background
		Clock.schedule_interval(self.update, 0.016)
		
	def update(self, nap):
		self.background.update(nap)

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('00bfff')
    AlienTecApp().run()