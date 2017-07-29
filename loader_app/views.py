from django.shortcuts import render
import hashlib
from django.http import JsonResponse

from loader_app.forms import UploadFileForm
from loader_app.models import FileName


def save_file(f):
    with open('data/' + f.name, 'wb+') as destination:
        for part in f.chunks():
            destination.write(part)


def count_hash_sum(f_, block_size=65536):
    sha256 = hashlib.sha256()
    with open('data/' + f_, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        f_name = request.FILES['file'].name
        if form.is_valid():
            save_file(request.FILES['file'])
            name = FileName.objects.create(name=f_name)
            name.save()
            hash_sum = count_hash_sum(f_name)
            files = FileName.objects.filter(name=f_name)
            count = files.count()
            return JsonResponse({'result': True, 'sum': hash_sum,
                                                 'count': count})
        else:
            return JsonResponse({'result': False, 'errors': form.errors})
    else:
        form = UploadFileForm()
    return render(request, 'main.html', context={'form': form})

