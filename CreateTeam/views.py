from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django .urls import reverse
from django.db import IntegrityError
from CreateTeam.models import Players,Matches,User_team,Choosen_players
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



# Create your views here.
@login_required(login_url='login')
def select_match(request):
    if request.user.is_authenticated:
        c1=Matches.objects.all().values_list('coun1')
        c2=Matches.objects.all().values_list('coun2')
        l=[1,2,3,4,5]
        l.sort()
        r1=[l[0], c1[0], c2[0]]
        r2=[l[1], c1[1], c2[1]]
        r3=[l[2], c1[2], c2[2]]
        r4=[l[3], c1[3], c2[3]]
        r5=[l[4], c1[4], c2[4]]
        return render(request, 'createteam/select_match.html', {'error':False, 'r1':r1, 'r2':r2, 'r3':r3, 'r4':r4, 'r5':r5})


@login_required(login_url='login')
def players(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            request.session['match'] = request.POST["match"]
            match = request.session['match']

            country1 = Matches.objects.filter(matchid=match)[0].coun1 
            country2 = Matches.objects.filter(matchid=match)[0].coun2

            request.session['batsmen'] = list(Players.objects.filter(country__in=[country1,country2],category='batsmen').values())
            request.session['all_rounder'] = list(Players.objects.filter(country__in=[country1,country2],category='all_rounder').values())
            request.session['bowler'] = list(Players.objects.filter(country__in=[country1,country2],category='bowler').values())
            request.session['wicket_keeper']= list(Players.objects.filter(country__in=[country1,country2],category__startswith='wicket').values())

            print(request.session['batsmen'])

            return  render(request,'createteam/players.html',{'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
        return render(request, 'createteam/players.html')


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        captain_id = request.POST["captain"]
        match_id = Matches.objects.get(matchid = request.session['match'])
        user_team = User_team(user_id =5 ,matchid = match_id,captain = captain_id)
        user_team.save() 
        user_match = User_team.objects.get(matchid = request.session['match'],user_id = 5)
        for i in request.session['selected_players']:
            player_id = Players.objects.get(pid = i)
            cp = Choosen_players(user_match = user_match, pid = player_id )
            cp.save()
        return render(request,'createteam/congrats.html',{'match_id':match_id})


@login_required(login_url='login')
def user_team(request):
    if request.user.is_authenticated:
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
            # print("hello",i)
            selected_points+=Players.objects.filter(pid=int(i))[0].points
        for i in request.session['selected_bowler']:
            selected_points+=Players.objects.filter(pid=int(i))[0].points
        for i in request.session['selected_all_rounder']:
            selected_points+=Players.objects.filter(pid=int(i))[0].points
        for i in request.session['selected_wicket_keeper']:
            selected_points+=Players.objects.filter(pid=int(i))[0].points
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
            return  render(request,'createteam/players.html',{'error_msg':error_msg,'error':True,'batsmen':request.session['batsmen'],'bowler':request.session['bowler'],'all_rounder':request.session['all_rounder'],'wicket_keeper':request.session['wicket_keeper']})
        selected_batsmen = []
        selected_bowler = []
        selected_all_rounder = []
        selected_wicket_keeper = []
        for i in request.session['selected_batsmen']:
            selected_batsmen.append(Players.objects.filter(pid=int(i))[0])
        for i in request.session['selected_bowler']:
            selected_bowler.append(Players.objects.filter(pid=int(i))[0])
        for i in request.session['selected_wicket_keeper']:
            selected_wicket_keeper.append(Players.objects.filter(pid=int(i))[0])
        for i in request.session['selected_all_rounder']:
            selected_all_rounder.append(Players.objects.filter(pid=int(i))[0])
        # print("selected_batsmen",selected_batsmen)
        return render(request,'createteam/user_team.html',{'batsmen':selected_batsmen,'bowler':selected_bowler,'all_rounder':selected_all_rounder,'wicket_keeper':selected_wicket_keeper})