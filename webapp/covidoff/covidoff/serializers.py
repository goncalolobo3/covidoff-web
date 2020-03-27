from django.core.serializers.json import Serializer as DjangoSerializer

class Serializer(DjangoSerializer):

	def get_dump_object(self, obj):
		return self._current
