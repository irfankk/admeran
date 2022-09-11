from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, authentication, status
from rest_framework.response import Response

from textdata.models import Tags, Snippet
from textdata import serializers as sz


class TagView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = sz.TagListSerializer

    def retrieve(self, request, pk=None):
        queryset = Tags.objects.filter(pk=pk)[0]
        serializer = sz.TagSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SnippetView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        user = request.user
        serializer = sz.SnippetCreateSerializer(data=request.data)
        if serializer.is_valid():
            tag = Tags.objects.get(id=serializer.data.get('tag'))
            snippet = Snippet(title=serializer.data.get('title'), created=datetime.now(), user=user,
                              updated=datetime.now(), tag=tag)
            snippet.save()
            return Response({'message': 'Created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        snippet = Snippet.objects.filter(id=pk)[0]
        serializer = sz.SnippetDetailSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        serializer = sz.SnippetCreateSerializer(data=request.data)
        if serializer.is_valid() and Snippet.objects.filter(id=pk).count() == 1:
            snippet = Snippet.objects.filter(id=pk)[0]
            snippet.title = serializer.data.get('title')
            snippet.content = serializer.data.get('content')
            snippet.tag = Tags.objects.filter(id=serializer.data.get('tag'))[0]
            snippet.updated = datetime.now()
            snippet.save()
            nsz = sz.SnippetDetailSerializer(snippet)
            return Response(nsz.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid data"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if Snippet.objects.filter(id=pk).count() == 0:
            return Response({"message": "invalid id"},  status=status.HTTP_204_NO_CONTENT)
        snippet = Snippet.objects.filter(id=pk)[0]
        snippet.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)

    def list(self, request):
        user = request.user
        snippets = user.user_snippets.all()
        count = user.user_snippets.all().count()
        serializer = sz.SnippetListsSerializer(snippets, many=True)
        return Response({"total": count, "data": serializer.data}, status=status.HTTP_200_OK)

