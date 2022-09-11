from rest_framework import serializers

from textdata.models import Tags, Snippet


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'title']


class TagSerializer(serializers.ModelSerializer):
    snippets = serializers.SerializerMethodField()

    class Meta:
        model = Tags
        fields = ['id', 'title', 'description', 'snippets']

    def get_snippets(self, obj):
        print(obj.tag_snippets.all())
        return SnippetListSerializer(obj.tag_snippets.all(), many=True).data


class SnippetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'content']


class SnippetCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    tag = serializers.IntegerField(required=True)

    class Meta:
        model = Snippet
        fields = ['title', 'tag', 'content']

    def validate_tag(self, value):
        if Tags.objects.filter(id=value).count() == 0:
            raise serializers.ValidationError('Invalid tag')
        return value


class SnippetDetailSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ['title', 'content', 'tag', 'created', 'updated']

    def get_tag(self, obj):
        return obj.tag.title


class SnippetListsSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    hyperlink = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'content', 'tag', 'created', 'updated', 'hyperlink']

    def get_tag(self, obj):
        return obj.tag.title

    def get_hyperlink(self, obj):
        return 'data/snippet/' + str(obj.pk)




