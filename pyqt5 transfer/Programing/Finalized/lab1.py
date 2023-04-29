class animal():
    def __init__(self,name,color):
        self.name = name
        self.color = color
    def speak(self):
        return self.name+" is speaking"

class dog(animal):
    def __init__(self, name, color):
        super().__init__(name, color)
    def speak(self):
        b = super().speak()
        return super().speak() + " gav"

a=animal("dog","black")
print(a.speak())
print(a.color)

b=dog("dog", "white")
print(b.speak())
print(b.color)



