from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from django.utils.timezone import localtime
from io import BytesIO
import os, zipfile
from django.core.mail import EmailMessage
from django.conf import settings


def upload_image(request):
    error_message = None  # エラーメッセージ用変数を追加

    if request.method == 'POST' and request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # アップロード時にファイル名を変更
            uploaded_image = form.save(commit=False)
            uploaded_image.uploaded_at = uploaded_image.uploaded_at
            uploaded_image.save()

            # メール送信の設定
            subject = "新しい画像がアップロードされました"
            message = f"""
            以下の内容で画像がアップロードされました：
            
            名前: {uploaded_image.name}
            メッセージ: {uploaded_image.message}
            """
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )
            # 添付ファイルを追加
            email.attach_file(uploaded_image.image.path)
            try:
                email.send()
            except Exception as e:
                error_message = f"送信中にエラーが発生しました: {e}" # エラーメッセージを格納

            if not error_message:  # エラーがない場合のみリダイレクト
                return redirect('image:complete')            
    else:
        form = ImageUploadForm()

    return render(request, 'image/upload_image.html', {'form': form, 'error_message': error_message})


""" 送信完了画面"""
def complete(request):
    return render(request, 'image/complete.html')



def list_images(request):
    images = UploadedImage.objects.all().order_by('-uploaded_at')
    return render(request, 'image/list_images.html', {'images': images})



def download_image(request, image_id):
    image = UploadedImage.objects.get(id=image_id)
    file_path = image.image.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
    return response



def download_images_in_range(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        images = UploadedImage.objects.filter(uploaded_at__range=[start_date, end_date])
    else:
        images = []

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for image in images:
            image_path = image.image.path
            zip_file.write(image_path, os.path.basename(image_path))
    
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    return response