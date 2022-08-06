from django.shortcuts import render
from django.http import HttpResponse
from home.models import data
from django.template import loader

def home(request):
    # html = '''
    # <form action=scrape>
    # <input type="text" name="location" placeholder="Enter the location here"><br>
    # <input type="submit" value="SUBMIT">
    #  '''
    context ={}
    template = loader.get_template('home/home.html')
    return HttpResponse(template.render(context,  request))
    # return HttpResponse(html)



def scrape(request):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    result_list=[]
    result_list_final = []
    details_1=[]
    details_2=[]
    details_3=[]
    details_4=[]
    details_5=[]

    line=""
    website = "https://www.google.com/search?q=automobile+repair+shop+near+"
    user_location = (request.GET['location'])
    loacation_final = user_location.split(" ")
    for i in range(len(loacation_final)):
        line = line+"+"+loacation_final[i]

    website = website+line+"&rlz=1C1GIGM_enIN851d pIN851&oq=automobile+repair+shop+near+"+line+"&aqs=chrome.0.69i59j0i22i30l9.2803j0j4&sourceid=chrome&ie=UTF-8"

    # Open the website
    driver.get(website)

    #wait to load
    # time.sleep(3)

    #click more places
    fb_btn = driver.find_element(By.TAG_NAME, 'g-more-link')
    fb_btn.click()

    parentElementlist = driver.find_elements(By.CLASS_NAME, "rllt__details")

    for parentElement in parentElementlist:
        allChildDivElements = parentElement.find_elements(By.TAG_NAME, "div")
        for childDivEement in allChildDivElements:
            result_list.append(childDivEement.text)
        result_list_final.append(result_list)
        result_list= []

    driver.quit()

    for details in (result_list_final):
        while(len(details)<5):
            details.append(" ")
        details_1.append(details[0])
        details_2.append(details[1])
        details_3.append(details[2])
        details_4.append(details[3])
        details_5.append(details[4])

    for i in range (len(result_list_final)):
        d1 = details_1[i]
        d2 = details_2[i]
        d3 = details_3[i]
        d4 = details_4[i]
        d5 = details_5[i]
        dat = data(location=user_location,detail1 = d1,detail2 = d2,detail3 = d3,detail4 = d4,detail5 = d5)
        dat.save()

    # sh=""
    # sh += "<h1>the location enterd is "+user_location+"</h1>"
    # sh += "<h3>Your data is stored. Type of dat is "+str(type(dat))+"</h3><br/>"


    # ##### EXTRACTING DATA FROM DATABASE #####
    # html = '''
    # <h1 class="header">The services near your location are 
    # '''

    # result_size = data.objects.filter(location = user_location)
    # for i in range(len(data.objects.filter(location=user_location))):
    #     final_data = data.objects.filter(location=user_location)
    #     sh += '<h1 class="title">'+str(final_data.detail1)+'</h1><br/>'
    final_data = data.objects.all()
    context ={
        'final_data' :final_data,
        'user_location':user_location
    }
    template=loader.get_template('home/result.html')
    return HttpResponse(template.render(context, request))
