from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ProjectViewSet, ContributorViewSet
from issues.views import IssueViewSet
from comments.views import CommentViewSet


# Routeur principal :  gère  /projects/
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

# Routeur imbriqué dans projects ; lookup='project' génère une variable d'URL appelée project_pk
projects_router = NestedDefaultRouter(router, r'projects', lookup='project')

# Routes générées :  /projects/{project_pk}/contributors/
projects_router.register(r'contributors', ContributorViewSet, basename='contributors')
# Routes générées :  /projects/{project_pk}/issues/
projects_router.register(r'issues', IssueViewSet, basename='issues')

# Routeur imbriqué dans issues ; lookup='issue' génère une variable d'URL appelée issue_pk
issues_router = NestedDefaultRouter(projects_router, r'issues', lookup='issue')

# Routes générées :  /projects/{project_pk}/issues/{issue_pk}/comments/
issues_router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]