from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.api_post.models import LikeDislike


class LikeDislikeMixins:
    def _make_vote(self, user, obj, vote):
        """GenericForeignKey does not support get_or_create"""
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=self.kwargs['pk'],
                user=user.pk
            )
            if vote == likedislike.vote:
                likedislike.delete()
            else:
                likedislike.vote = vote
                likedislike.save(update_fields=['vote'])
            response_status = status.HTTP_200_OK
        except LikeDislike.DoesNotExist:
            likedislike = obj.votes.create(user=user, vote=vote)
            response_status = status.HTTP_201_CREATED
        return Response({
            'liked': likedislike.vote == LikeDislike.LIKE,
            'disliked': likedislike.vote == LikeDislike.DISLIKE,
            'like_count': obj.votes.likes().count(),
            'dislike_count': obj.votes.dislikes().count(),
            'sum_rating': obj.votes.sum_rating()
        }, status=response_status)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def like(self, request, *args, **kwargs):
        return self._make_vote(request.user,
                               self.get_queryset().get(pk=self.kwargs['pk']),
                               LikeDislike.LIKE)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def dislike(self, request, *args, **kwargs):
        return self._make_vote(request.user,
                               self.get_queryset().get(pk=self.kwargs['pk']),
                               LikeDislike.DISLIKE)
