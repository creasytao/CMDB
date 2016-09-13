#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : Api/views.py
# @author      : Li90.COM
# @revision    : 2016-08-1 18:44:51
# @brief       :

#from django.shortcuts import render
#from django.http import HttpResponse
#from django.http import Http404
#from django.views.decorators.csrf import csrf_exempt

from Api.serializer import *
from Api.models import *
from Api.permissions import *

from rest_framework import viewsets
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
#from rest_framework import status
#from rest_framework.decorators import api_view
#from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework.response import Response
#from rest_framework.reverse import reverse
#from rest_framework import mixins
#from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import detail_route

# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    查看、编辑用户的界面
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    查看、编辑组的界面
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#@api_view(['GET'])
#def api_root(request,format=None):
#    return Response({
#        'users':reverse('user-list',request=request,format=format),
#        'snippets':reverse('snippet-list',request=request, format=format)
#    })
#
#
#
#
#class SnippetHighlight(generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    renderer_classes = (renderers.StaticHTMLRenderer,)
#
#    def get(self, request, *args, **kwargs):
#        snippet = self.get_object()
#        return Response(snippet.highlighted)
#
#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#
#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#class SnippetList(generics.ListCreateAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
#
#class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                         IsOwnerOrReadOnly,)
#
#class SnippetList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#
#class SnippetDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)

#class SnippetList(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = SnippetSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#class SnippetDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return Snippet.objects.get(pk=pk)
#        except Snippet.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
#
#class JSONResponse(HttpResponse):
#    """
#    An HttpResponse that renders it's content into JSON.
#    """
#    def __init__(self,data,**kwargs):
#        content=JSONRenderer().render(data)
#        kwargs['content_type']='application/json'
#        super(JSONResponse,self).__init__(content,**kwargs)
#
#@api_view(['GET','POST'])
#def snippet_list(request, format=None):
#    """
#    展示或创建snippet.
#    """
#    if request.method == 'GET':
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets,many=True)
#        return Response(serializer.data)
#
#    elif request.method == 'POST':
#        serializer = SnippetSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data,status=status.HTTP_201_CREATED)
#        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#@csrf_exempt
#def snippet_detail(request, pk, format=None):
#    """
#    修改或删除一个snippet.
#    """
#    try:
#        snippet = Snippet.objects.get(pk=pk)
#    except Snippet.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#
#    if request.method == 'GET':
#        serializer = SnippetSerializer(snippet)
#        return Response(serializer.data)
#
#    elif request.method == 'PUT':
#        serializer = SnippetSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
#
#    elif request.method == 'DELETE':
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
