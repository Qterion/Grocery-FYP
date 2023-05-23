from .models import ScoreChoice

def score_decisions(request):
    return{
        "score_decisions":ScoreChoice.values,
    }