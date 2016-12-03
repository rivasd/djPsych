'''
Created on Dec 3, 2016

@author: Daniel Rivas
'''

from rest_framework import permissions


class ExperimentPermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return permissions.BasePermission.has_permission(self, request, view)
    
    def has_object_permission(self, request, view, obj):
        return obj.is_researcher(request) or request.user.is_superuser()