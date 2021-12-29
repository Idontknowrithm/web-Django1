from django.db import models

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length = 128,
                             verbose_name = '제목')
    contents = models.TextField(verbose_name = '내용')

    writer = models.ForeignKey('User.User', on_delete = models.CASCADE,
                               verbose_name = '작성자')
    registered_dttm = models.DateTimeField(auto_now_add = True,
                                           verbose_name = '등록시간')
    tags = models.ManyToManyField('tag.Tag', verbose_name = '태그')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'board'
        verbose_name = '게시글'
        verbose_name_plural = '게시글'

# TextField → 길이제한이 없는 필드
# on_delete = models.CASCADE → 사용자가 삭제되면 게시글 전부를 삭제
# (SET_DEFAULT → 기본값을 지정해주고 그것을 채움)
# ForeignKey → 디비에 ID를 직접 연결해줌
