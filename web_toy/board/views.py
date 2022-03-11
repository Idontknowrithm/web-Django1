from django.shortcuts import render
from .models import Board
from .forms import BoardForm
from django.shortcuts import render, redirect
from User.models import User
from tag.models import Tag
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.
def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = request.GET.get('p', 1)
    paginator = Paginator(all_boards, 4)
    
    boards = paginator.get_page(page)
    
    return render(request, 'board_list.html', {'boards' : boards})

# all() : 모두 가져오겠다
# order_by('-id') : -가 역순. 시간 역순으로 정렬하여 가져오겠다

def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk = user_id)

            tags = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user
            board.save()
            
            
            for tag in tags:
                if not tag:
                    continue
                
                _tag, _ = Tag.objects.get_or_create(name = tag)
                # 태그가 있으면 가져오고, 없으면 만들기
                board.tags.add(_tag)

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form' : form})

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk = pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
        
    board = Board.objects.get(pk = pk)
    return render(request, 'board_detail.html', {'board' : board})
# pk: 몇 번째 글을 상세보기 할 건지에 대한 정보가 필요함
