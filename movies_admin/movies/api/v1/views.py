from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, RoleType


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def __agregate_film_crew(self, role_type: str):
        return ArrayAgg('person__full_name', filter=Q(personfilmwork__role=role_type), distinct=True)

    def get_queryset(self):
        queryset = FilmWork.objects.prefetch_related('genres', 'person')

        return queryset.values().annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self.__agregate_film_crew(RoleType.ACTOR),
            direcors=self.__agregate_film_crew(RoleType.DIRECTOR),
            writers=self.__agregate_film_crew(RoleType.WRITER),
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return {**kwargs.get("object")}
