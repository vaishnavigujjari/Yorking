from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django .urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from CreateTeam.models import country_team, match_user, user_team, choosen_players, match_performance
import pymysql


#global declaration
points =100
admin_match_id=0
master_user_id=0
master_match_id=0
sel_players_user=[]



# Create your views here.
@login_required(login_url='login')
def select_match(request):
    if request.user.is_authenticated:
        p=match_user.objects.filter(status='Did not start')
        return render(request,'createteam/select_match.html',{"matches":p})



@login_required(login_url='login')
def players(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            global points
            global master_match_id
            points = 100
            request.session['match'] = request.POST["match"]
            match = request.session['match']
            master_match_id=match
            print(master_user_id)
            matches_already=list(user_team.objects.filter(match_id=match,user_id=master_user_id).values())
            if matches_already != []:
                error_msg='You have already created a team for this match choose another match'
                p=match_user.objects.filter(status='Did not start')
                return render(request,'createteam/select_match.html',{'error_msg':error_msg,'error':True,'matches':p})
            request.session['match'] = request.POST["match"]
            match = request.session['match']
            country1 = match_user.objects.filter(match_id=match)[0].country1 
            country2 = match_user.objects.filter(match_id=match)[0].country2

            request.session['batsmen'] = list(country_team.objects.filter(country__in=[country1,country2],category='batsmen').values())
            request.session['all_rounder'] = list(country_team.objects.filter(country__in=[country1,country2],category='all_rounder').values())
            request.session['bowler'] = list(country_team.objects.filter(country__in=[country1,country2],category='bowler').values())
            request.session['wicket_keeper']= list(country_team.objects.filter(country__in=[country1,country2],category__startswith='wicket').values())

            print(request.session['batsmen'])

            return  render(request,'createteam/players.html',{'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
        return render(request, 'createteam/players.html')

@csrf_exempt
def get_points(request):
    p_id = request.POST["id"]
    global points
    print("pid",p_id)
    print("points",points)
    p_points = country_team.objects.filter(player_id=p_id)
    if(int(request.POST["checked"])):
        new_points = int(points) - int(p_points[0].points)
        points = new_points
    else:
        new_points = int(points) + int(p_points[0].points)
        points = new_points

    return HttpResponse(new_points)




@login_required(login_url='login')
def congrats(request):
    global master_match_id
    global master_user_id
    master_user_id=1
    if request.method=="POST":
        if request.user.is_authenticated:
            request.session['captain_choosen']=request.POST.getlist("captain")
            uteam=user_team(user_id=master_user_id,match_id=master_match_id,captain=request.session['captain_choosen'][0])
            uteam.save()
            uteam_id=user_team.objects.filter(user_id=master_user_id,match_id=master_match_id).values('id')
            for i in sel_players_user:
                pid=country_team.objects.get(player_id=i)
                cp=choosen_players(player_id=pid,user_match_id=uteam_id,stars=0)
                cp.save()
        print(request.session['captain_choosen'][0],"is the captain choosen")
        p=match_user.objects.filter(status='Did not start')
        return HttpResponse('<h1> Congrats! </h1>')

@login_required(login_url='login')
def userteam(request):
    if request.user.is_authenticated:
        global sel_players_user
        global points
        request.session['selected_batsmen']=request.POST.getlist("batsmen")
        request.session['selected_bowler'] = request.POST.getlist("bowler")
        request.session['selected_all_rounder'] = request.POST.getlist("all_rounder")
        request.session['selected_wicket_keeper']= request.POST.getlist("wicket_keeper")
        min_batsmen=4
        min_bowlers=3
        min_wk=1
        min_all=1
        all_players=11
        total_points=100
        selected_points=0
        error_msg=[]
        print(request.session['selected_batsmen'])
        request.session['selected_players'] = request.session['selected_batsmen'] + request.session['selected_bowler'] + request.session['selected_all_rounder'] + request.session['selected_wicket_keeper']
        for i in request.session['selected_batsmen']:
            selected_points+=country_team.objects.filter(player_id=int(i))[0].points
        for i in request.session['selected_bowler']:
            selected_points+=country_team.objects.filter(player_id=int(i))[0].points
        for i in request.session['selected_all_rounder']:
            selected_points+=country_team.objects.filter(player_id=int(i))[0].points
        for i in request.session['selected_wicket_keeper']:
            selected_points+=country_team.objects.filter(player_id=int(i))[0].points
        all_selected=len(request.session['selected_batsmen'])+len(request.session['selected_bowler'])+len(request.session['selected_wicket_keeper'])+len(request.session['selected_all_rounder'])
        if len(request.session['selected_batsmen'])<min_batsmen:
            error_msg.append("select minimum 4 batsmen")
        if len(request.session['selected_bowler']) < min_bowlers:
            error_msg.append("select minimum 3 bowlers")
        if len(request.session['selected_wicket_keeper']) < min_wk:
            error_msg.append("select minimum 1 wicket keeper")
        if len(request.session['selected_all_rounder']) < min_all:
            error_msg.append("select minimum 1 all rounder")
        if all_selected != all_players:
            error_msg.append("select only 11 players")
        if selected_points>total_points:
            error_msg.append("Select players with points less than 100")
        if error_msg != []:
            points = 100
            return  render(request,'createteam/players.html',{'error_msg':error_msg,'error':True,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
        selected_batsmen = []
        selected_bowler = []
        selected_all_rounder = []
        selected_wicket_keeper = []
        for i in request.session['selected_batsmen']:
            selected_batsmen.append(country_team.objects.filter(player_id=int(i))[0])
            sel_players_user.append(int(i))
        for i in request.session['selected_bowler']:
            selected_bowler.append(country_team.objects.filter(player_id=int(i))[0])
            sel_players_user.append(int(i))
        for i in request.session['selected_wicket_keeper']:
            selected_wicket_keeper.append(country_team.objects.filter(player_id=int(i))[0])
            sel_players_user.append(int(i))
        for i in request.session['selected_all_rounder']:
            selected_all_rounder.append(country_team.objects.filter(player_id=int(i))[0])
            sel_players_user.append(int(i))
        # print("selected_batsmen",selected_batsmen)
        return render(request,'createteam/user_team.html',{'batsmen':selected_batsmen,'bowler':selected_bowler,'all_rounder':selected_all_rounder,'wicket_keeper':selected_wicket_keeper})

def select_team(request):
    global admin_match_id
    if request.method=="POST":
        request.session['match'] = request.POST["match"]
        match = request.session['match']
        admin_match_id=match
        # query = reduce(operator.or_,(Q(country=cn,category='bat') for cn in [country1,country2]))
        country1=match_user.objects.filter(match_id=match)[0].country1 
        country2 = match_user.objects.filter(match_id=match)[0].country2
        request.session['batsmen1'] = list(country_team.objects.filter(country=country1,category='Batsman').values())
        request.session['all_rounder1'] = list(country_team.objects.filter(country=country1,category='AllRounder').values())
        request.session['bowler1'] = list(country_team.objects.filter(country=country1,category='Bowler').values())
        request.session['wicket_keeper1']= list(country_team.objects.filter(country=country1,category__startswith='WicketKeeper').values())
        request.session['batsmen2'] = list(country_team.objects.filter(country=country2,category='Batsman').values())
        request.session['all_rounder2'] = list(country_team.objects.filter(country=country2,category='AllRounder').values())
        request.session['bowler2'] = list(country_team.objects.filter(country=country2,category='Bowler').values())
        request.session['wicket_keeper2']= list(country_team.objects.filter(country=country2,category__startswith='WicketKeeper').values())
        return  render(request,'players.html',{'batsman_1':request.session['batsmen1'],'bowler_1':request.session['bowler1'],'allrounder_1':request.session['all_rounder1'],'wicketkeeper_1':request.session['wicket_keeper1'],'batsman_2':request.session['batsmen2'],'bowler_2':request.session['bowler2'],'allrounder_2':request.session['all_rounder2'],'wicketkeeper_2':request.session['wicket_keeper2']})
    country_team_obj=country_team.objects.values('country').distinct()
    p=match_user.objects.filter(status='Did not start')
    error_msg="Sorry :( invalid selection "
    return render(request,'select_match.html',{'error':error,'countries':country_team_obj,"matches":p})

def update_scores(request):
    global admin_match_id
    print(admin_match_id)
    if request.method=="POST":
        request.session['selected_batsmen']=request.POST.getlist("batsmen_ids_1")
        request.session['selected_bowler'] = request.POST.getlist("bowler_ids_1")
        request.session['selected_all_rounder'] = request.POST.getlist("ar_ids_1")
        request.session['selected_wicket_keeper']= request.POST.getlist("wk_ids_1")
        request.session['selected_batsmen_2']=request.POST.getlist("batsmen_ids_2")
        request.session['selected_bowler_2'] = request.POST.getlist("bowler_ids_2")
        request.session['selected_all_rounder_2'] = request.POST.getlist("ar_ids_2")
        request.session['selected_wicket_keeper_2']= request.POST.getlist("wk_ids_2")
        runs_bat_1=request.POST.getlist("runs_bat_1")
        runs_bat_2=request.POST.getlist("runs_bat_2")
        runs_ball_1=request.POST.getlist("runs_ball_1")
        runs_ball_2=request.POST.getlist("runs_ball_2")
        runs_wk_1=request.POST.getlist("runs_wk_1")
        runs_wk_2=request.POST.getlist("runs_wk_2")
        runs_ar_1=request.POST.getlist("runs_ar_1")
        runs_ar_2=request.POST.getlist("runs_ar_2")
        catches_bat_1=request.POST.getlist("catches_bat_1")
        catches_bat_2=request.POST.getlist("catches_bat_2")
        catches_ball_1=request.POST.getlist("catches_ball_1")
        catches_ball_2=request.POST.getlist("catches_ball_2")
        catches_wk_1=request.POST.getlist("catches_wk_1")
        catches_wk_2=request.POST.getlist("catches_wk_2")
        catches_ar_1=request.POST.getlist("catches_ar_1")
        catches_ar_2=request.POST.getlist("catches_ar_2")
        wickets_bat_1=request.POST.getlist("wickets_bat_1")
        wickets_bat_2=request.POST.getlist("wickets_bat_2")
        wickets_ball_1=request.POST.getlist("wickets_ball_1")
        wickets_ball_2=request.POST.getlist("wickets_ball_2")
        wickets_wk_1=request.POST.getlist("wickets_wk_1")
        wickets_wk_2=request.POST.getlist("wickets_wk_2")
        wickets_ar_1=request.POST.getlist("wickets_ar_1")
        wickets_ar_2=request.POST.getlist("wickets_ar_2")
        print(request.session['selected_batsmen'])
        for i in range(len(request.session['selected_batsmen'])):
            mp=match_performance(player_id=int(request.session['selected_batsmen'][i]),runs=runs_bat_1[i],catches=catches_bat_1[i],wickets=wickets_bat_1[i],match_id=admin_match_id,category='Batsman')
            mp.save()
        for i in range(len(request.session['selected_bowler'])):
            mp=match_performance(player_id=int(request.session['selected_bowler'][i]),runs=runs_ball_1[i],catches=catches_ball_1[i],wickets=wickets_ball_1[i],match_id=admin_match_id,category='Bowler')
            mp.save()
        for i in range(len(request.session['selected_all_rounder'])):
            mp=match_performance(player_id=int(request.session['selected_all_rounder'][i]),runs=runs_ar_1[i],catches=catches_ar_1[i],wickets=wickets_ar_1[i],match_id=admin_match_id,category='AllRounder')
            mp.save()
        for i in range(len(request.session['selected_wicket_keeper'])):
            mp=match_performance(player_id=int(request.session['selected_wicket_keeper'][i]),runs=runs_wk_1[i],catches=catches_wk_1[i],wickets=wickets_wk_1[i],match_id=admin_match_id,category='WicketKeeper')
            mp.save()
        for i in range(len(request.session['selected_batsmen_2'])):
            mp=match_performance(player_id=int(request.session['selected_batsmen_2'][i]),runs=runs_bat_2[i],catches=catches_bat_2[i],wickets=wickets_bat_2[i],match_id=admin_match_id,category='Batsman')
            mp.save()
        for i in range(len(request.session['selected_bowler_2'])):
            mp=match_performance(player_id=int(request.session['selected_bowler_2'][i]),runs=runs_ball_2[i],catches=catches_ball_2[i],wickets=wickets_ball_2[i],match_id=admin_match_id,category='Bowler')
            mp.save()
        for i in range(len(request.session['selected_all_rounder_2'])):
            mp=match_performance(player_id=int(request.session['selected_all_rounder_2'][i]),runs=runs_ar_2[i],catches=catches_ar_2[i],wickets=wickets_ar_2[i],match_id=admin_match_id,category='AllRounder')
            mp.save()
        for i in range(len(request.session['selected_wicket_keeper_2'])):
            mp=match_performance(player_id=int(request.session['selected_wicket_keeper_2'][i]),runs=runs_wk_2[i],catches=catches_wk_2[i],wickets=wickets_wk_2[i],match_id=admin_match_id,category='WicketKeeper')
            mp.save()
        r=match_user.objects.get(match_id=admin_match_id)
        r.status='Completed'
        r.save()
        p=match_user.objects.filter(status='Did not start')
        q=country_team.objects.values('country').distinct()
        update_scores_in_players(admin_match_id)
        admin_match_id=0
        return render(request,'createteam/select_match.html',{"matches":p,"countries":q})
    p=match_user.objects.filter(status='Did not start')
    q=country_team.objects.values('country').distinct()
    return render(request,'createteam/select_match.html',{"matches":p,"countries":q})



def constraints(request):
    global master_user_id
    request.session['selected_batsmen']=request.POST.getlist("batsman_1")
    request.session['selected_bowler'] = request.POST.getlist("baller_1")
    request.session['selected_all_rounder'] = request.POST.getlist("allrounder_1")
    request.session['selected_wicket_keeper']= request.POST.getlist("wicketkeeper_1")
    request.session['selected_batsmen_2']=request.POST.getlist("batsman_2")
    request.session['selected_bowler_2'] = request.POST.getlist("baller_2")
    request.session['selected_all_rounder_2'] = request.POST.getlist("allrounder_2")
    request.session['selected_wicket_keeper_2']= request.POST.getlist("wicketkeeper_2")
    #print(request.session['selected_batsmen'])
    min_batsmen=4
    min_bowlers=3
    min_wk=1
    min_all=1
    all_players=11
    error_msg=[]
    all_selected_1=len(request.session['selected_batsmen'])+len(request.session['selected_bowler'])+len(request.session['selected_wicket_keeper'])+len(request.session['selected_all_rounder'])
    all_selected_2=len(request.session['selected_batsmen_2'])+len(request.session['selected_bowler_2'])+len(request.session['selected_wicket_keeper_2'])+len(request.session['selected_all_rounder_2'])
    if len(request.session['selected_batsmen'])<min_batsmen:
        error_msg.append("select minimum 4 batsmen for first country")
    if len(request.session['selected_bowler']) < min_bowlers:
        error_msg.append("select minimum 3 bowlers for first country")
    if len(request.session['selected_wicket_keeper']) < min_wk:
        error_msg.append("select minimum 1 wicket keeper for first country")
    if len(request.session['selected_all_rounder']) < min_all:
        error_msg.append("select minimum 1 all rounder for first country")
    if all_selected_1 != all_players:
        error_msg.append("select only 11 players for first country")
    if len(request.session['selected_batsmen_2'])<min_batsmen:
        error_msg.append("select minimum 4 batsmen for second country")
    if len(request.session['selected_bowler_2']) < min_bowlers:
        error_msg.append("select minimum 3 bowlers for second country")
    if len(request.session['selected_wicket_keeper_2']) < min_wk:
        error_msg.append("select minimum 1 wicket keeper for second country")
    if len(request.session['selected_all_rounder_2']) < min_all:
        error_msg.append("select minimum 1 all rounder for second country")
    if all_selected_2 != all_players:
        error_msg.append("select only 11 players for second country")
    if error_msg != []:
        return  render(request,'select_team.html',{'error_msg':error_msg,'error':True,'batsman_1':request.session['batsmen1'],'bowler_1':request.session['bowler1'],'allrounder_1':request.session['all_rounder1'],'wicketkeeper_1':request.session['wicket_keeper1'],'batsman_2':request.session['batsmen2'],'bowler_2':request.session['bowler2'],'allrounder_2':request.session['all_rounder2'],'wicketkeeper_2':request.session['wicket_keeper2']})
    print(request.session['selected_batsmen'])
    print(request.session['selected_bowler'])
    print(request.session['selected_all_rounder'])
    print(request.session['selected_wicket_keeper'])
    selected_batsmen_1 = []
    selected_bowler_1 = []
    selected_all_rounder_1 = []
    selected_wicket_keeper_1 = []
    for i in request.session['selected_batsmen']:
        selected_batsmen_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_bowler']:
        selected_bowler_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_wicket_keeper']:
        selected_wicket_keeper_1.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_all_rounder']:
        selected_all_rounder_1.append(country_team.objects.filter(player_id=int(i))[0])
    selected_batsmen_2 = []
    selected_bowler_2 = []
    selected_all_rounder_2 = []
    selected_wicket_keeper_2 = []
    for i in request.session['selected_batsmen_2']:
        selected_batsmen_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_bowler_2']:
        selected_bowler_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_wicket_keeper_2']:
        selected_wicket_keeper_2.append(country_team.objects.filter(player_id=int(i))[0])
    for i in request.session['selected_all_rounder_2']:
        selected_all_rounder_2.append(country_team.objects.filter(player_id=int(i))[0])
    print(admin_match_id)
    return render(request,'update_scores.html',{'batsmanone_selected':selected_batsmen_1,'ballerone_selected':selected_bowler_1,'wicketkeeperone_selected':selected_wicket_keeper_1,'allrounderone_selected':selected_all_rounder_1,'batsmantwo_selected':selected_batsmen_2,'ballertwo_selected':selected_bowler_2,'wicketkeepertwo_selected':selected_wicket_keeper_2,'allroundertwo_selected':selected_all_rounder_2})