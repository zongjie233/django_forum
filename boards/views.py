from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import  Board,Topic,Post
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .forms import NewTopicForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request, pk):
    try:
        board = Board.objects.get(pk = pk)
    except Board.DoesNotExist:
        raise  Http404
    # board = Board.objects.get(pk = pk)
    return render(request, 'topics.html', {'board':board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()
    #Django表单方式
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  #
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})