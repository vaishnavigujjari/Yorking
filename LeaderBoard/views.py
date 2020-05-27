from django.shortcuts import render
from CreateTeam.models import Players,Matches,User_team,Choosen_players
from django.http import JsonResponse 
from django.views.generic import View



def userPointCalculation(i):
    matchPerformanceObj = MatchPerformance.objects.filter(match_id=i)
    obj = UserTeam.objects.values('user_id').distinct()
    for u in obj:
        userTeamObj = UserTeam.objects.filter(user_id=u['user_id'])
        s = 0
        for u in userTeamObj:
            for m in matchPerformanceObj:
                if(m.player_id == u.player_id):
                    if(m.player_id.player_id==u.captain.player_id):
                        s += (m.runs + m.catches*20 + m.wickets*20)*2
                    else:
                        s += m.runs + m.catches*20 + m.wickets*20
        for u in userTeamObj:
            u.stars = s
            u.save()

def choosematch(request):
    return render(request,'leaderboard/choosematch.html')

def matchlist(request):
    matchObj = Matches.objects.values('matchid','coun1','coun2')
    match_ids = []
    country1s = []
    country2s = []
    if not(request.is_ajax()):
        for m in matchObj:
            match_ids.append(m['matchid'])
            country1s.append(m['coun1'])
            country2s.append(m['coun2'])
        return render(request,'leaderboard/matchlist.html',{'matchObj':matchObj,'match_ids':match_ids,'country1s':
        country1s,'country2s':country2s})
    else:
        i = request.GET.get('id')
        if request.method == 'GET':
            matchObj2 = Matches.objects.filter(match_id=i).values('matchid','coun1','coun2')
            for m in matchObj2:
                match_ids.append(m['matchid'])
                country1s.append(m['coun1'])
                country2s.append(m['coun2'])
            userTeamList = lb(i)
            print(userTeamList)
            mydict = {'seconds':i,'match_ids':match_ids,'country1s':country1s,
			'country2s':country2s,'userTeamList':userTeamList}
            return JsonResponse(mydict)

def lb(i):
    userPointCalculation(201)

	#LeaderBoard Evaluation
    userTeamObj = UserTeam.objects.order_by('-stars').values('stars','user_id').distinct()
    stars = []
    user_ids = []
    user_names = []
    for u in userTeamObj:
        stars.append(u['stars'])
        user_ids.append(u['user_id'])
    for u in user_ids:
        userObj = User.objects.filter(user_id=u)
        for o in userObj:
            user_names.append(o.user_name)
    userTeamList = []
    userTeamList.append(user_ids)
    userTeamList.append(user_names)
    userTeamList.append(stars)

    return userTeamList