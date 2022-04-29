class Screan(object):

    @property
    def width(self):
        return self._birth

    @property
    def height(self):
        return self._birth

    @width.setter
    def width(self, value):
        self._width = value

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def revolution(self):
        return self._width * self._height
        # if self._height*self._birth == 786432 :
        #    print("good setting")
        # else:
        #     raise ValueError("wrong setting")


s = Screan()
s.width = 1024
s.height = 768
print(s.revolution)



