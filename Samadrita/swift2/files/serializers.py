from rest_framework import serializers
from .models import Container, Object


class ContainerSerializer(serializers.ModelSerializer):

    name = serializers.HyperlinkedIdentityField(many=True, view_name='cont_info', format='html')

    class Meta:
        model = Container
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=True, queryset=Stock.objects.all())
    name = serializers.HyperlinkedRelatedField(many=True, view_name='obj_info', read_only=True)


    class Meta:
        model = Object
        fields = '__all__'
