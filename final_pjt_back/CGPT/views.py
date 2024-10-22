from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from .models import ChatHistory
from django.conf import settings
from openai import OpenAI
GPT_API_KET=settings.GPT_API_KET


client = OpenAI(
    api_key = GPT_API_KET,
)
@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        
        client = OpenAI(
            api_key = GPT_API_KET,
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message}]
        )
        
        answer = response.choices[0].message.content
        
        # # 대화 내용 저장
        # ChatHistory.objects.create(
        #     user_id=request.user.id,
        #     message=message,
        #     response=answer,
        #     timestamp=timezone.now()
        # )
        
        return JsonResponse({'response': answer})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_chat_history(request):
    if request.method == 'POST':
        # 사용자의 모든 대화 내용 삭제
        ChatHistory.objects.filter(user_id=request.user.id).delete()
        return JsonResponse({'message': 'Chat history deleted'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
