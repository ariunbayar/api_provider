from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from table.models import Table
from .models import Column
from .forms import ColumnForm
from notification.utils import notify


@login_required
def new(request, table_pk):
    table = get_object_or_404(Table.obs, pk=table_pk, user=request.user)

    if request.method == 'POST':

        form = ColumnForm(request.POST)

        if form.is_valid():

            column = form.save()

            notify(request.user, '"%s" хүснэгтийн "%s" баганыг амжилттай үүсгэлээ' % (table.name, column.name))

            return redirect('table-detail', table.pk)
    else:
        form = ColumnForm(initial={'table': table})

    context = {
            'table': table,
            'form': form
        }
    return render(request, 'column/form.html', context)


@login_required
def edit(request, table_pk, pk):
    table = get_object_or_404(Table.obs, pk=table_pk, user=request.user)
    column = get_object_or_404(Column.obs, table=table, pk=pk)

    if request.method == 'POST':

        values = {**request.POST, 'table': table}
        form = ColumnForm(request.POST, instance=column)

        if form.is_valid():

            column = form.save()

            notify(request.user, '"%s" хүснэгтийн "%s" баганыг амжилттай хадгаллаа' % (table.name, column.name))

            return redirect('table-detail', table.pk)
    else:
        form = ColumnForm(instance=column)

    context = {
            'table': table,
            'form': form
        }
    return render(request, 'column/form.html', context)


@login_required
def delete(request, table_pk, pk):

    table = get_object_or_404(Table.obs, pk=table_pk, user=request.user)
    column = get_object_or_404(Column.obs, table=table, pk=pk)
    column.is_deleted = True
    column.save()

    notify(request.user, '"%s" хүснэгтийн "%s" баганыг амжилттай устгалаа' % (table.name, column.name))

    return redirect('table-detail', column.table.pk)
