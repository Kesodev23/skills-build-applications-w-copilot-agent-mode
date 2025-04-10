from django.http import JsonResponse
from django.views import View
from .models import UserProfile, Leaderboard, FitnessTracking
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        # Retrieve all user profiles
        profiles = UserProfile.objects.all()
        profiles_list = [model_to_dict(profile) for profile in profiles]
        return JsonResponse(profiles_list, safe=False)

    def post(self, request):
        # Handle duplicates and blanks interactively
        data = request.POST
        if not data.get('name') or not data.get('email'):
            return JsonResponse({'error': 'Name and email are required.'}, status=400)

        if UserProfile.objects.filter(email=data.get('email')).exists():
            return JsonResponse({'error': 'A user with this email already exists.'}, status=400)

        # Create a new user profile
        profile = UserProfile.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            age=data.get('age'),
            height=data.get('height'),
            weight=data.get('weight'),
            target=data.get('target', 0.0)  # Default target to 0.0 if not provided
        )
        return JsonResponse(model_to_dict(profile), status=201)

@method_decorator(csrf_exempt, name='dispatch')
class LeaderboardView(View):
    def get(self, request):
        # Retrieve all leaderboard entries ordered by rank
        leaderboard_entries = Leaderboard.objects.all().order_by('rank')
        leaderboard_list = [model_to_dict(entry) for entry in leaderboard_entries]
        return JsonResponse(leaderboard_list, safe=False)

    def post(self, request):
        # Handle duplicates and blanks interactively
        data = request.POST
        if not data.get('user_id') or not data.get('total_points') or not data.get('rank'):
            return JsonResponse({'error': 'User ID, total points, and rank are required.'}, status=400)

        # Create or update a leaderboard entry
        user_id = data.get('user_id')
        total_points = data.get('total_points')
        rank = data.get('rank')

        leaderboard_entry, created = Leaderboard.objects.update_or_create(
            user_id=user_id,
            defaults={
                'total_points': total_points,
                'rank': rank
            }
        )
        return JsonResponse(model_to_dict(leaderboard_entry), status=201)

@method_decorator(csrf_exempt, name='dispatch')
class FitnessTrackingView(View):
    def get(self, request):
        # Retrieve all fitness tracking records
        tracking_records = FitnessTracking.objects.all()
        tracking_list = [model_to_dict(record) for record in tracking_records]
        return JsonResponse(tracking_list, safe=False)

    def post(self, request):
        # Handle duplicates and blanks interactively
        data = request.POST
        if not data.get('user_id') or not data.get('activity_type') or not data.get('duration') or not data.get('date'):
            return JsonResponse({'error': 'User ID, activity type, duration, and date are required.'}, status=400)

        # Check for duplicate entries for the same user and date
        if FitnessTracking.objects.filter(user_id=data.get('user_id'), date=data.get('date')).exists():
            return JsonResponse({'error': 'A fitness tracking record for this user and date already exists.'}, status=400)

        # Create a new fitness tracking record
        tracking_record = FitnessTracking.objects.create(
            user_id=data.get('user_id'),
            activity_type=data.get('activity_type'),
            duration=data.get('duration'),
            calories_burned=data.get('calories_burned'),
            date=data.get('date')
        )
        return JsonResponse(model_to_dict(tracking_record), status=201)
