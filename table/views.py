from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Table
from .forms import TableForm
from column.models import Column
from notification.models import Notification


@login_required
def list(request):
    tables = Table.obs.filter(user=request.user)

    context = {
            'tables': tables,
        }
    return render(request, 'table/list.html', context)


@login_required
def detail(request, pk):
    table = get_object_or_404(Table.obs, pk=pk, user=request.user)
    context = {
            'table': table,
            'columns': table.column_set.all(),
        }
    return render(request, 'table/detail.html', context)


@login_required
def new(request):

    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = Table.obs.create(
                    user=request.user,
                    name=form.cleaned_data.get('name'),
                )
            Notification.objects.create(
                    user=request.user,
                    message='"%s" нэртэй хүснэгтийг амжилттай үүсгэлээ' % table.name,
                )
            return redirect('table-detail', table.pk)
    else:
        form = TableForm()

    context = {
            'form': form
        }
    return render(request, 'table/form.html', context)


@login_required
def edit(request, pk):
    table = get_object_or_404(Table.obs, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            table.name = form.cleaned_data.get('name')
            table.save()
            # TODO notify
            return redirect('table-detail', table.pk)
    else:
        form = TableForm(instance=table)

    context = {
            'form': form
        }
    return render(request, 'table/form.html', context)


@login_required
def delete(request, pk):
    table = get_object_or_404(Table.obs, pk=pk, user=request.user)

    Column.obs.filter(table=table).update(is_deleted=True)

    table.is_deleted = True
    table.save()
    # TODO make create notification
    return redirect('table-list')
