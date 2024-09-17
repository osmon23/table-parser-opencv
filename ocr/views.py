import pytesseract
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from django.conf import settings
from main import main
import subprocess
from .forms import UploadFileForm


def process_file(file_path):
    try:
        # Вызов скрипта main.py с передачей аргумента (путь к файлу)
        result = subprocess.run(['python', 'main.py', file_path], capture_output=True, text=True)
        
        # Вывод результата выполнения скрипта
        if result.returncode == 0:
            return f"Скрипт выполнен успешно. Результат:\n{result.stdout}"
        else:
            return f"Ошибка выполнения скрипта:\n{result.stderr}"
    
    except Exception as e:
        return f"Произошла ошибка при запуске скрипта: {str(e)}"


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = process_file(request.FILES["file"])
            return HttpResponse(result)
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})
