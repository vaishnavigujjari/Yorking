from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from CreateTeam.models import country_team, match_user, user_team, choosen_players, match_performance

# Create your views here.
@login_required(login_url='login')
def selectmatch(request):
    if request.user.is_authenticated:
        p=match_user.objects.filter(status='Completed')
        return render(request,'playerdashboard/selectmatch.html',{'matches':p})


@login_required(login_url='login')
def matches(request):
    if request.user.is_authenticated:
        return render(request, 'playerdashboard/matches.html')


@login_required(login_url='login')
def pdm1(request):
    if request.user.is_authenticated:
        global master_match_id
        global master_user_id
        master_user_id=1
        if request.method=="POST":
            request.session['match'] = request.POST["match"]
            match = request.session['match']
            master_match_id=match
            ut_id = list(user_team.objects.filter(match_id=match,user_id=master_user_id).values('id'))
            if ut_id == []:
                l=match_user.objects.filter(status='Completed')
                error_msg='Sorry :( You have not created a team for this match.Please choose another match'
                return render(request,'playerdashboard/selectmatch.html',{'error_msg':error_msg,'error':True,'matches':l})
            players_c=list(choosen_players.objects.filter(user_match_id=ut_id[0]['id']).values())
            mp=list(match_performance.objects.filter(match_id=match).values('player_id'))
            lst1=[]
            lst2=[]
            lst3=[]
            players_choosen=[]
            mp1=[]
            print(mp)
            for i in players_c:
                players_choosen.append(i['player_id'])
            for i in mp:
                mp1.append(i['player_id'])
            print(mp1)
            print(players_choosen)
            for i in players_choosen:
                if i in mp1:
                    p=list(match_performance.objects.filter(match_id=match,player_id=i).values('runs','wickets','catches'))
                    q=list(country_team.objects.filter(player_id=i).values('player_name','category','country'))
                    lst1.append(p)
                    lst2.append(q)
                    lst3.append('Played')
                else:
                    p=[{'runs':'-','wickets':'-','catches':'-'}]
                    q=list(country_team.objects.filter(player_id=i).values('player_name','category','country'))
                    lst1.append(p)
                    lst2.append(q)
                    lst3.append('Did not play')
            mylist=zip(lst1,lst2,lst3)
            return render(request,'pdm1.html',{'details':mylist})
        l=match_user.objects.filter(status='Completed')
        return render(request,'playerdashboard/selectmatch.html',{'matches':l})
