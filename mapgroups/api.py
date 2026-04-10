"""DRF API views replacing the rpc4django /rpc endpoint for the mapgroups app.

Replaces these former XML-RPC methods:
    get_sharing_groups, update_map_group
"""
from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mapgroups.models import MapGroup


class SharingGroupListView(APIView):
    """GET /api/sharing-groups/

    Returns all map groups the authenticated user belongs to, plus any
    public sharing groups defined in settings.SHARING_TO_PUBLIC_GROUPS.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        data: list[dict[str, Any]] = []

        for membership in request.user.mapgroupmember_set.all():
            group = membership.map_group
            members = sorted(
                member.user_name_for_group()
                for member in group.mapgroupmember_set.all()
            )
            data.append({
                'group_name': group.name,
                'group_slug': group.permission_group.name,
                'members': members,
                'is_mapgroup': True,
            })

        for public_group in Group.objects.filter(name__in=settings.SHARING_TO_PUBLIC_GROUPS):
            data.append({
                'group_name': public_group.name,
                'group_slug': public_group.name,
                'members': [],
                'is_mapgroup': False,
            })

        return Response(data)


class MapGroupUpdateView(APIView):
    """PATCH /api/map-groups/<pk>/

    Selectively updates name, blurb, and/or is_open for a map group owned
    by the authenticated user.

    Body keys (all optional):
        update_name  (bool)  + name  (str)
        update_blurb (bool)  + blurb (str)
        update_is_open (bool) + is_open (bool)
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, pk: int) -> Response:
        mg = get_object_or_404(MapGroup, id=pk, owner=request.user)
        options: dict[str, Any] = request.data
        changed = False

        if options.get('update_name'):
            mg.name = options['name']
            changed = True

        if options.get('update_blurb'):
            mg.blurb = options['blurb']
            changed = True

        if options.get('update_is_open'):
            mg.is_open = options['is_open']
            changed = True

        if changed:
            mg.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
