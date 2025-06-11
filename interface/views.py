
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from .models import Item
from .forms import ItemFilterForm
from datetime import date, timedelta,datetime
from django.forms.models import model_to_dict
from google.cloud import texttospeech
from django.core.files.storage import default_storage
from django.http import JsonResponse
import os
from google.cloud import texttospeech
from django.db.models import Q,F
import time
from openai import OpenAI

from dotenv import load_dotenv
import os
import openai
import json


from interface.models import Domain, Field, Branch
load_dotenv()  # Load variables from .env


print("KEY:", os.environ.get("OPENAI_API_KEY"))

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def item_list(request):
    form = ItemFilterForm(request.GET)
    items = Item.objects.all()
    
    
    if request.method == "POST" and request.POST.get("add") == "1":
        post_type = request.POST.get("item_type")
        
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        domains=Domain.objects.all()
        fields=Field.objects.all()
        branches=Branch.objects.all()
        
        gpt_classifiction=ask_chatgpt(title,description,link,domains,fields,branches)
        store_post(post_type, gpt_classifiction["title"], gpt_classifiction["description"], gpt_classifiction["platform"],link, gpt_classifiction["domain"], gpt_classifiction["field"], gpt_classifiction["branch"], author="Mody")
        #print(gpt_classifiction["platform"])
        print(gpt_classifiction)
        
        
       

    if form.is_valid():
        cd = form.cleaned_data  # shorthand

        if cd['item_type']:
            items = items.filter(item_type=cd['item_type'])

        if cd['title']:
            items = items.filter(title__icontains=cd['title'])

        if cd['author']:
            items = items.filter(author=cd['author'])  # FK match

        if cd['domain']:
            items = items.filter(domain=cd['domain'])  # FK match

        if cd['field']:
            items = items.filter(field=cd['field'])  # FK match

        if cd['branch']:
            items = items.filter(branch=cd['branch'])  # FK match

        if cd['date_created_from']:
            items = items.filter(date_created__gte=cd['date_created_from'])

        if cd['date_created_to']:
            items = items.filter(date_created__lte=cd['date_created_to'])

        if cd['tags']:
            tags = [tag.strip() for tag in cd['tags'].split(',')]
            for tag in tags:
                items = items.filter(tags__icontains=tag)

    count =  items.count()

    return render(request, 'interface/item_list.html', {'form': form, 'items': items,'count':count})



def details(request,item_id):
    
    item = get_object_or_404(Item, id=item_id)
    if request.method=='POST':
        
        if 'delete' in request.POST:
            print("delete")
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('memory')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()

            else:
                
                
                
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('memory')
        
        elif 'play' in request.POST:
        
            # Synthesize speech
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=item.content)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-AU", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Stream the audio content as a response
            return HttpResponse(response.audio_content, content_type='audio/mpeg')
            
    return render(request, 'interface/details.html', {'item': item})

def memory(request):

    
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('memory')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()
            
            else:
              
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('memory')
        
        elif 'archive'in request.POST :
            post_id=request.POST.get('archive')
            done_item = Item.objects.get(id=post_id)
            done_item.next_time=None
            done_item.save()
            print("archive")
        
        elif 'hide_20' in request.POST :
            print("hide20")
            post_id=request.POST.get('hide_20')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+1200
            hide_item.save()
        
        elif 'hide_360' in request.POST :
            print("hide360")
            post_id=request.POST.get('hide_360')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+21600
            hide_item.save()
        
        

        
    form = ItemFilterForm(request.GET)
    #items = Item.objects.filter(next_time__lte=date.today())
    items = Item.objects.filter(Q(hide_time__lte=time.time()) & Q(next_time__lte=date.today()) & ~Q(next_time=F('last_time')) & ~Q(item_type ="Task") )

    if form.is_valid():
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())

    return render(request, 'interface/today_list.html', {'form': form, 'items': items})



def new(request):
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('new')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()
            
            else:
             
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('new')
        
        elif 'archive' in request.POST:
            post_id=request.POST.get('archive')
            done_item = Item.objects.get(id=post_id)
            done_item.next_time=None
            done_item.save()
            print("archive")
        
        elif 'postpone' in request.POST :
            print("postpone")
            post_id=request.POST.get('postpone')
            done_item = Item.objects.get(id=post_id)
            postpone_time=request.POST.get('postpone_time')
            done_item.next_time=datetime.now() + timedelta(days=int(postpone_time))
            done_item.save()

        elif 'hide_20' in request.POST :
            print("hide20")
            post_id=request.POST.get('hide_20')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+1200
            hide_item.save()
        
        elif 'hide_360' in request.POST :
            print("hide360")
            post_id=request.POST.get('hide_360')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+21600
            hide_item.save()


           
        

        
    form = ItemFilterForm(request.GET)
    
    
    items = Item.objects.filter(Q(hide_time__lte=time.time()) & Q(next_time__lte=date.today()) & Q(next_time=F('last_time'))& ~Q(item_type ="Task") & Q(last_time=F('init_time')  ))
    
    if form.is_valid():
        
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
            
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['domain']:
            items = items.filter(domain__domain_name__icontains=form.cleaned_data['domain'])
            
            
        if form.cleaned_data['field']:
            items = items.filter(field__field_name__icontains=form.cleaned_data['field'])
        
        if form.cleaned_data['branch']:
            items = items.filter(branch__branch_name__icontains=form.cleaned_data['branch'])
            
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())
    
    
        

    return render(request, 'interface/new.html', {'form': form, 'items': items})

def reset(request):
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('reset')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()
            
            else:
                
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('reset')
        
        elif 'archive' in request.POST:
            post_id=request.POST.get('archive')
            done_item = Item.objects.get(id=post_id)
            done_item.next_time=None
            done_item.save()
            print("archive")
        
        elif 'postpone' in request.POST :
            print("postpone")
            post_id=request.POST.get('postpone')
            done_item = Item.objects.get(id=post_id)
            postpone_time=request.POST.get('postpone_time')
            done_item.next_time=datetime.now() + timedelta(days=int(postpone_time))
            done_item.save()

        elif 'hide_20' in request.POST :
            print("hide20")
            post_id=request.POST.get('hide_20')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+1200
            hide_item.save()
        
        elif 'hide_360' in request.POST :
            print("hide360")
            post_id=request.POST.get('hide_360')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+21600
            hide_item.save()
        

        
    form = ItemFilterForm(request.GET)
    
    
    items = Item.objects.filter(Q(hide_time__lte=time.time()) & Q(next_time__lte=date.today()) & Q(next_time=F('last_time'))& ~Q(item_type ="Task") & ~Q(last_time=F('init_time')  ))       
    

    
    
    if form.is_valid():
        
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
            
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['domain']:
            items = items.filter(domain__domain_name__icontains=form.cleaned_data['domain'])
            
            
        if form.cleaned_data['field']:
            items = items.filter(field__field_name__icontains=form.cleaned_data['field'])
        
        if form.cleaned_data['branch']:
            items = items.filter(branch__branch_name__icontains=form.cleaned_data['branch'])
            
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())
    
    
        

    return render(request, 'interface/new.html', {'form': form, 'items': items})

def task(request):
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('task')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()
            
            else:
           
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('task')
        
        elif 'archive'in request.POST:
            post_id=request.POST.get('archive')
            done_item = Item.objects.get(id=post_id)
            done_item.next_time=None
            done_item.save()

        elif 'postpone' in request.POST:
            post_id=request.POST.get('postpone')
            done_item = Item.objects.get(id=post_id)
            postpone_time=request.POST.get('postpone_time')
            done_item.next_time=datetime.now() + timedelta(days=int(postpone_time))
            done_item.save()


        
    form = ItemFilterForm(request.GET)
    items = Item.objects.filter(Q(next_time__lte=date.today()) & Q(item_type="Task"))
    
    
    
    #items = items.filter(item_type=form.cleaned_data['item_type'])
        

    return render(request, 'interface/tasks.html', {'form': form, 'items': items})


def test(request):
    
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            post_id=request.POST.get('delete')
            delete_item = Item.objects.get(id=post_id)
            delete_item.delete()
        
        elif 'reset' in request.POST:
            post_id=request.POST.get('reset')
            reset_item = Item.objects.get(id=post_id)
            reset_item.next_time=reset_date().date()
            reset_item.last_time=reset_date().date()
            reset_item.save()
            return redirect('test')
        
        elif 'done' in request.POST:
            post_id=request.POST.get('done')
            done_item = Item.objects.get(id=post_id)
            if done_item.next_time==done_item.last_time:
                done_item.last_time=datetime.now()
                done_item.next_time=datetime.now() + timedelta(days=1)
                done_item.save()
            
            else:
              
                done_item.next_time=calculate_next_time(done_item.last_time,done_item.next_time)
                print(done_item.next_time)
                done_item.save()
            
            return redirect('memory')
        
        elif 'archive'in request.POST :
            post_id=request.POST.get('archive')
            done_item = Item.objects.get(id=post_id)
            done_item.next_time=None
            done_item.save()
            print("archive")
        
        elif 'hide_20' in request.POST :
            print("hide20")
            post_id=request.POST.get('hide_20')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+1200
            hide_item.save()
        
        elif 'hide_360' in request.POST :
            print("hide360")
            post_id=request.POST.get('hide_360')
            hide_item = Item.objects.get(id=post_id)
            hide_item.hide_time=time.time()+21600
            hide_item.save()
        
        

        
    form = ItemFilterForm(request.GET)
    #items = Item.objects.filter(next_time__lte=date.today())
    #items = Item.objects.filter(Q(next_time__gte=date(2025, 4, 22)))
    #items = Item.objects.filter(field__field_name="Fachkundeprüfung").order_by('last_time')
    items = get_items_with_calculations()
    
    if form.is_valid():
        if form.cleaned_data['item_type']:
            items = items.filter(item_type=form.cleaned_data['item_type'])
        if form.cleaned_data['title']:
            items = items.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            items = items.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data['date_created_from']:
            items = items.filter(date_created__gte=form.cleaned_data['date_created_from'])
        if form.cleaned_data['date_created_to']:
            items = items.filter(date_created__lte=form.cleaned_data['date_created_to'])
        if form.cleaned_data['tags']:
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                items = items.filter(tags__icontains=tag.strip())

    return render(request, 'interface/test.html', {'form': form, 'items': items})


def calculate_next_time(last_time, next_time):
    # Calculate the current interval in days between last_time and next_time
    current_interval = (next_time - last_time).days

    # Initialize the next Fibonacci interval
    if current_interval == 0:
        next_interval = 1  # Start from 1 if the interval is zero (initial case)
    elif current_interval == 1:
        next_interval = 2  # Start with the second Fibonacci number
    else:
        # Apply the Fibonacci sequence by calculating the next interval
        prev_interval = current_interval
        next_interval = current_interval + prev_interval
    
    # Cap the interval at 90 days (approximately 3 months)
    max_interval = 90
    if next_interval > max_interval:
        next_interval = max_interval

    # Calculate the next review time by adding the interval in days
    next_time = last_time + timedelta(days=next_interval)

    return next_time

def reset_date():
    next_time=datetime.now()+timedelta(days=0)
    return next_time

import re
from interface.models import Item

def get_items_with_calculations(field_name="Fachkundeprüfung"):
    items = Item.objects.filter(field__field_name=field_name).order_by('last_time')

    filtered = []

    for item in items:
        content = item.content or ""
        lines = content.splitlines()

        # Look for lines with both numbers and symbols like = + - * /
        match_lines = [
            line for line in lines
            if re.search(r'\d', line) and re.search(r'[=+\*/]', line)
        ]

        if len(match_lines) >= 1:
            filtered.append(item)

    return filtered



def ask_chatgpt(title,description,link,domains,fields,branches):
    
    full_prompt = f"""
            You are a smart classification assistant.
            You will receive a post description and sometimes a link.
            Do not open the link.
            Detect the platform from the link if present.
            Use the provided lists of Domains, Fields, and Branches to classify the content.
            If no exact match is found in any category, suggest a new one instead.
            If no title is given, generate a clear, relevant title from the content.
            Dont use domain General
            The domain should be always the wider category
            then it goes narrower to the field and narrower to the domain
            If you can not find out the platform from the link! you keep it none! 

            ❗️Return ONLY a raw JSON object. Do NOT use markdown, backticks, or any explanation.

            Format:
            {{
            "title": "...",
            "description": "...",
            "platform": "...",
            "domain": "...",
            "field": "...",
            "branch": "..."
            }}
          
            {title}

            description:
            {description}

            link:
            {link}

            Domains:
            {domains}

            Fields:
            {fields}

            Branches:
            {branches}
        """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a classification engine."},
            {"role": "user", "content": full_prompt}
        ]
    
    )
    #raw = response.choices[0].message.content.strip("` \n")
    #raw = response.choices[0].message.content
    #print("RAW RESPONSE:")
    #print(repr(raw))   
    #json_data = json.loads(raw)
    json_data=parse_response_to_json(response.choices[0].message.content)

    return json_data
    #return "none"



from datetime import date
import time
from interface.models import Item, Domain, Field, Platform


def parse_response_to_json(response_text):
    """
    Cleans and converts a string response into a valid JSON object.
    - Strips markdown wrappers (like ```json)
    - Handles malformed spacing or newline issues
    - Raises informative errors if parsing fails
    """
    try:
        # Remove markdown wrappers like ```json or ``` if present
        cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

        # Try to parse
        #print("parced successuflly")
        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        print("❌ JSON decoding failed. Check format.")
        print("Raw input received:")
        print(repr(response_text))
        print(f"Error details: {e}")
        return None

def store_post(post_type,title,description,platform_name, link, domain_name, field_name, branch_name, author="Mody"):
    try:
        # Lookups
        platform, _ = Platform.objects.get_or_create(platform_name=platform_name)
        domain, _ = Domain.objects.get_or_create(domain_name=domain_name)
        field, _ = Field.objects.get_or_create(field_name=field_name)
        branch, _ = Branch.objects.get_or_create(branch_name=branch_name)

        

        # Timestamps
        today_date = date.today()
        today_timestamp = str(int(time.time()))

        # Title & Content
        title = title
        content = description

        # Create item
        Item.objects.create(
            item_type=post_type,
            title=title,
            content=content,
            author=author,
            fPlatform=platform,
            platform=platform_name,
            
            domain=domain,
            field=field,
            branch=branch,
            link=link,
            init_time=today_date,
            last_time=today_date,
            next_time=today_date,
            hide_time=today_timestamp
        )

        print(f"✅ {platform_name} post stored successfully.")
        return True

    except (Domain.DoesNotExist, Field.DoesNotExist, Platform.DoesNotExist) as e:
        print(f"❌ Lookup failed: {e}")
        return False
    

    