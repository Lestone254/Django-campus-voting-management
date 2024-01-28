from django import template
from index.models import *
register = template.Library()

@register.filter
def sort(cons):
	cons=cons.order_by('-Votes')
	return cons
@register.filter
def content(posts):
	p=[]
	for x in posts:
		if x.contestant_set.all().exists():
			p.append(x)
	return p
@register.filter
def activated(voters):
	voters=Voter.objects.all()
	count=0
	for x in voters:
		if x.Activated==True:
			count=count+1
	return count
@register.filter
def getvoters(school):
	school=School.objects.get(id=school)
	initials=school.Initials
	voters=Voter.objects.filter(School=initials)
	return voters
@register.filter
def macque(election):
	votes=Vote.objects.filter(Election=election)
	mvotes=[]
	for x in votes:
		vote=votes.filter(Voter=x.Voter).last()
		mvotes.append(vote.id)
	lvotes=list(dict.fromkeys(mvotes))
	return lvotes
@register.filter
def macquet(election):
	votes=Vote.objects.filter(Election=election)
	mvotes=[]
	for x in votes:
		vote=votes.filter(Voter=x.Voter).last()
		mvotes.append(vote.id)
	lvotes=list(dict.fromkeys(mvotes))
	return len(lvotes)
@register.filter
def pvote(id):
	return Vote.objects.get(id=id).Voter.RegNo
@register.filter
def nvote(id):
	return Vote.objects.get(id=id).Voter.FirstName+' '+Vote.objects.get(id=id).Voter.LastName