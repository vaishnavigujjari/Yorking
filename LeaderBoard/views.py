from django.shortcuts import render
from CreateTeam.models import country_team, match_user, user_team, choosen_players, match_performance
from django.http import JsonResponse 
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def Leaderboard(request):
    if request.user.is_authenticated:
        p=match_user.objects.filter(status='Completed')
        return render(request,'leaderboard/leaderboard.html',{"matches":p})


# @login_required(login_url='login')
# def choosematch(request):
#     if request.user.is_authenticated:
#         return render(request, 'leaderboard/choosematch.html', name='choosematch')


@login_required(login_url='login')
def leaderboardeval(request):
    if request.user.is_authenticated:
        global master_match_id
        master_match_id=0
        if request.method=="POST":
            request.session['match'] = request.POST["match"]
            match = request.session['match']
            uteams=list(user_team.objects.filter(match_id=match).values())
            ut=[]
            cp=[]
            us=[]
            lst=[]
            d={}
            for i in uteams:
                ut.append(i['id'])
                cp.append(i['captain'])
                us.append(i['user_id'])
            for j in ut:
                st=[]
                st=list(choosen_players.objects.filter(user_match=j).values('stars'))
                st1=[]
                score=0
                for k in st:
                    st1.append(k['stars'])
                score=sum(st1)
                ind=ut.index(j)
                cap=cp[ind]
                s1=[]
                s1=list(choosen_players.objects.filter(player_id=cap,user_match_id=j).values())
                #print(s1,ind,cap,j)
                s2=s1[0]['stars']
                score+=s2
                lst.append(score)
                d[us[ind]]=score
            x={}
            x=sorted(d.items(),key =lambda kv:(kv[1],kv[0]),reverse=True)
            z=[]
            for h in x:
                print(h[0])
                y=[]
                y=list(user.objects.filter(user_id=h[0]).values())
                z.append(y)
            print(d)
            print(x)
            print(z)
            mylist=zip(x,z)
            mylist_2=zip(x,y)
            return render(request,'leaderboard/lbm1.html',{'d':mylist,'y':mylist_2})
        p=match_user.objects.filter(status='Completed')
        return render(request,'leaderboard/leaderboard.html',{"matches":p})


@login_required(login_url='login')
def pdm1(request):
    if request.user.is_authenticated:
        pass

@login_required(login_url='login')
@csrf_exempt
def get_points(request):
    if request.user.is_authenticated:
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
def update_scores_in_players(x):
    if request.user.is_authenticated:
        pass


@login_required(login_url='login')
def update_scores(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            request.session['selected_batsmen']=request.POST.getlist("batsmen_ids_1")
            request.session['selected_bowler'] = request.POST.getlist("bowler_ids_1")
            request.session['selected_all_rounder'] = request.POST.getlist("ar_ids_1")
            request.session['selected_wicket_keeper']= request.POST.getlist("wk_ids_1")
            request.session['selected_batsmen_2']=request.POST.getlist("batsmen_ids_2")
            request.session['selected_bowler_2'] = request.POST.getlist("bowler_ids_2")
            request.session['selected_all_rounder_2'] = request.POST.getlist("ar_ids_2")
            request.session['selected_wicket_keeper_2']= request.POST.getlist("wk_ids_2")
            
            return render(request,'dummy.html')
        p=match_user.objects.filter(status='Did not start')
        q=country_team.objects.values('country').distinct()
        return render(request,'form.html',{"matches":p,"countries":q})
