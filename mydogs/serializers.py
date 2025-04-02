import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from. models import Mydogs


#class Mydogsmodel:
#    def __init__(self, name, breed, age, price, category):
#        self.name = name
#       self.breed = breed
#        self.age = age
#       self.price = price
#        self.category = category



class MydogsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Mydogs
        fields = '__all__'
   # name = serializers.CharField(max_length=100)
   # breed = serializers.CharField(max_length=100)
   # age = serializers.IntegerField()
   # price = serializers.DecimalField(max_digits=10, decimal_places=2)
   # category = serializers.CharField()

   # def create(self, validated_data):
       # return Mydogs.objects.create(**validated_data)

   # def update(self, instance, validated_data):
       # instance.name = validated_data.get('name', instance.name)
       # instance.breed = validated_data.get('breed', instance.breed)
       # instance.age = validated_data.get('age', instance.age)
       #instance.price = validated_data.get('price', instance.price)
       # instance.category = validated_data.get('category', instance.category)
       # instance.save()
       # return instance




#def encode():
#    model = Mydogsmodel('Motlik','breed: Korgy','age: 2','price: 3000', 'category: friendly')
#    model_sr = MydogsSerializer(model.__dict__)
#    print(model_sr.data, type(model_sr.data), sep='\n')
#    json = JSONRenderer().render(model_sr.data)
#    print(json)


#def decode():
#   stream = io.BytesIO(b'{"name": "Motlik","breed": "Korgi", "age": "2", "price": "3000", "category": "friendly"}')
#    data = JSONParser().parse(stream)
#   serializer = MydogsSerializer(data=data)
#   serializer.is_valid()
#   print(serializer.validated_data)



