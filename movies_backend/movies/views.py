from django.http import HttpResponse
from django.http import response
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view

from movies.models import Dynamic, Fname, Lname, Movie, Output, User, UserPattern
import dateutil.parser 
import json,ast,random,string,re
from os import listdir
from os.path import isfile, join
import pandas as pd 
import time
import os


IPs = []

# Local
# images_path = "M:/MS_STUDY/RA/MOVIE/selected gan faces/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'selected_faces.csv')

df = pd.read_csv(csv_path, usecols=['face_number', 'type'])
#df = pd.read_csv('selected_faces.csv',usecols=['face_number','type'])

# images_path = "/home/ubuntu/MOVIES/selected_images/"
# df = pd.read_csv('/home/ubuntu/MOVIES/fb-movies-app/movies_backend/selected_faces.csv',usecols=['face_number','type'])

def index(request):
    return HttpResponse("Hello, world. You're at the Movies index.")

@api_view(["POST"])
def postIP(data):
    data = data.body.decode("utf-8")
    if data in IPs:
        return JsonResponse(0,safe=False)
    else:
        return JsonResponse(1,safe=False)

@api_view(["GET"])
def getUserID(request):
    r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    if len(User.objects.all()) > 0:
        while (len(User.objects.filter(user_id=r)) != 0):
            r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    return JsonResponse(r,safe=False)

@api_view(["POST"])
def postSurveyData(data):
    data = json.loads(data.body.decode("utf-8"))
    try:
        movies_selected = []
        for movie in data['movies_selected']:
            if data['movies_selected'].get(movie):
                movies_selected.append(movie)
        movies_reviewed = data['movies_reviewed']
        for i in range(len(data['movie_data'])-1,-1,-1):
            movie_data = data['movie_data'][i]
            name_data = data['name_data'][i]
            fname = Fname.objects.filter(first_name=name_data['fname'])[0]
            clicked = 1 if str(i) in movies_selected else 0
            readmore_count = movies_reviewed.get(str(i)) if movies_reviewed.get(str(i)) else 0
            timed = 1 if data["time_choice"] == True else 0
            output_instance = Output.objects.create(
                user_id = data["user_id"],
                order_no = i+1,
                movie_title = movie_data["title"],
                rating = movie_data["rating"],
                review = movie_data["review"],
                clicked = clicked,
                readmore_count = readmore_count,
                timestamp = data["timestamp"],
                timed = timed,
                rec_first_name = fname.first_name,
                rec_last_name = name_data['lname'],
                rec_race = fname.race,
                rec_gender = fname.gender,
            )
        return JsonResponse('Post Info Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Info Failed',safe=False)

@api_view(["POST"])
def postUserTestType(data):
    try:
        data = json.loads(data.body.decode("utf-8"))
        timed = 1 if data["time_choice"] == True else 0
        user = User.objects.get(user_id=data["user_id"])
        user.test_type = timed
        user.save()
        return JsonResponse('Post Test Type Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Test Type Failed',safe=False)

@api_view(["POST"])
def postFeedbackData(data):
    data = json.loads(data.body.decode("utf-8"))
    try:
        user_id = data["user_id"]
        user = User.objects.get(user_id=user_id)
        user.feedback_rate = data["rate"]
        user.feedback_satisfied = data["satisfied"]
        user.feedback_rely = data["rely"]
        user.feedback_likely = data["likely"]
        user.feedback_study = data["study"]
        user.feedback_share = data["share"]
        user.time_spent = str((dateutil.parser.parse(data["user_exit_time"])-user.user_entry_time).total_seconds())
        user.save()
        return JsonResponse('Post Feedback Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Feedback Failed',safe=False)

@api_view(["POST"])
def postMovieLink(data):
    data = json.loads(data.body.decode("utf-8"))
    try:
        user_id = data["user_id"]
        user = User.objects.get(user_id=user_id)
        user.movie_link_clicked = 1
        user.save()
        return JsonResponse('Post Movie Link Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Movie Link Failed',safe=False)

@api_view(["POST"])
def postNewUser(data):
    info = json.loads(data.body.decode("utf-8"))
    try:
        user_instance = User.objects.create(
            user_id = info["user_id"],
            user_entry_time = info["user_entry_time"],
        )
        timed = 1 if info["time_choice"] == True else 0
        user = User.objects.get(user_id=info["user_id"])
        user.test_type = timed
        user.save()
        createUserMovieNamePattern(info["user_id"],timed)
        return JsonResponse('Post Info Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Info Failed',safe=False)

@api_view(["POST"])
def postUserInfo(data):
    info = json.loads(data.body.decode("utf-8"))
    races = ','.join(name for name in info['race'])
    try:
        timed = 1 if info["time_choice"] == True else 0
        user = User.objects.get(user_id=info["user_id"])
        user.test_type = timed
        user.user_race = races
        user.user_gender = info["gender"]
        user.user_age = info["age"]
        user.user_education = info["study"]
        user.user_frequency = info["frequency"]
        user.user_genre = info["genre"]
        user.save()
        return JsonResponse('Post Info Success',safe=False)
    except Exception as e:
        print(e)
        return JsonResponse('Post Info Failed',safe=False)
  

movies_count = len(Movie.objects.all())
fnames_count = len(Fname.objects.all())
whiteNames = []
hispanicNames = []
blackNames = []
asianNames = []
for fname in Fname.objects.all():
    first_name = model_to_dict(fname)['first_name']
    race = model_to_dict(fname)['race']
    gender = model_to_dict(fname)['gender']
    lnames = list(Lname.objects.filter(race=race))
    for lname in lnames:
        last_name = model_to_dict(lname)['last_name']
        if race == 'White':
            whiteNames.append({"fname":first_name,"lname":last_name,"race":'white',"gender":gender})
        elif race == 'Black':
            blackNames.append({"fname":first_name,"lname":last_name,"race":'black',"gender":gender})
        elif race == 'Hispanic':
            hispanicNames.append({"fname":first_name,"lname":last_name,"race":'hispanic',"gender":gender})
        else:
            asianNames.append({"fname":first_name,"lname":last_name,"race":'asian',"gender":gender})
random.shuffle(whiteNames)
random.shuffle(hispanicNames)
random.shuffle(blackNames)
random.shuffle(asianNames)

# onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]
pattern = r'_#\d*_'
exclude_files = [8,41,37,79,80,95,98,111,104,125,140,153,144,143,154,163,177,194,221,256,271,280,287,288,300,313,314,315,320,321,333,350]

def createFacesPattern(namesList):
    image_sets = []
    for name in namesList:
        if name['gender'] == 'Male':
            for i in range(61):
                face_type = df.iloc[[i]]['type'].values[0]
                face_idx = df.iloc[[i]]['face_number'].values[0]
                if (face_type == 'men') and (face_idx not in image_sets):
                    image_sets.append(face_idx)
                    break
        elif name['gender'] == 'Female':
            for i in range(61):
                face_type = df.iloc[[i]]['type'].values[0]
                face_idx = df.iloc[[i]]['face_number'].values[0]
                if (face_type == 'women') and (face_idx not in image_sets):
                    image_sets.append(face_idx)
                    break
    return image_sets

def createUserMovieNamePattern(id,timed):
    try:
        if timed == 1:
            movies_count = model_to_dict(Dynamic.objects.first())['total_movies_time_1']
        else:
            movies_count = model_to_dict(Dynamic.objects.first())['total_movies_time_2']
        randomMovieslist = random.sample(range(1,movies_count+1), movies_count)
        
        # Updated distribution: Race - 20% Black, 25% Hispanic, 55% White; Gender - 60% Female, 40% Male
        raceProbabilities = {'White': 55, 'Hispanic': 25, 'Black': 20, 'Asian': 0}
        genderProbabilities = {'Female': 60, 'Male': 40}
        
        # Calculate targets with proper rounding
        total_names_needed = movies_count
        female_target = round(total_names_needed * genderProbabilities['Female'] / 100)  # Use round instead of int
        male_target = total_names_needed - female_target
        
        # Calculate race targets with proper rounding handling
        white_target = round(total_names_needed * raceProbabilities['White'] / 100)
        hispanic_target = round(total_names_needed * raceProbabilities['Hispanic'] / 100)
        black_target = round(total_names_needed * raceProbabilities['Black'] / 100)
        asian_target = 0  # Asian is 0% in our distribution
        
        # Adjust for rounding errors to ensure total equals movies_count
        total_calculated = white_target + hispanic_target + black_target + asian_target
        if total_calculated != total_names_needed:
            # Adjust the largest group (White) to compensate for rounding
            white_target += (total_names_needed - total_calculated)
        
        # Separate names by race and gender
        race_gender_pools = {
            'White': {'Female': [], 'Male': []},
            'Hispanic': {'Female': [], 'Male': []},
            'Black': {'Female': [], 'Male': []},
            'Asian': {'Female': [], 'Male': []}
        }
        
        # Populate pools
        for name in whiteNames:
            race_gender_pools['White'][name['gender']].append(name)
        for name in hispanicNames:
            race_gender_pools['Hispanic'][name['gender']].append(name)
        for name in blackNames:
            race_gender_pools['Black'][name['gender']].append(name)
        for name in asianNames:
            race_gender_pools['Asian'][name['gender']].append(name)
        
        # Shuffle all pools
        for race in race_gender_pools:
            for gender in race_gender_pools[race]:
                random.shuffle(race_gender_pools[race][gender])
        
        # NEW SIMPLIFIED ALGORITHM: Global gender balance approach
        namesList = []
        used_names = set()
        race_counts = {'White': 0, 'Hispanic': 0, 'Black': 0, 'Asian': 0}
        gender_counts = {'Female': 0, 'Male': 0}
        
        # Create a prioritized list of candidates with race weights
        all_candidates = []
        race_targets = {
            'White': white_target,
            'Hispanic': hispanic_target, 
            'Black': black_target,
            'Asian': asian_target
        }
        
        # Add candidates with race priority weighting
        for race, target_count in race_targets.items():
            if target_count <= 0:
                continue
            # Add all available names for this race with their target count as weight
            race_pool = race_gender_pools[race]['Female'] + race_gender_pools[race]['Male']
            for name in race_pool:
                all_candidates.append((name, race, target_count))
        
        # Shuffle candidates
        random.shuffle(all_candidates)
        
        # Sort by race priority (descending target count) to fill race quotas first
        all_candidates.sort(key=lambda x: x[2], reverse=True)
        
        # Selection phase 1: Fill race quotas while trying to maintain gender balance
        remaining_female = female_target
        remaining_male = male_target
        remaining_race_targets = race_targets.copy()
        
        for candidate, race, _ in all_candidates:
            if len(namesList) >= total_names_needed:
                break
            
            # Check if we still need this race
            if remaining_race_targets[race] <= 0:
                continue
                
            # Check uniqueness
            name_key = (candidate['fname'], candidate['lname'], candidate['gender'])
            if name_key in used_names:
                continue
            
            # Gender-aware selection
            gender = candidate['gender']
            can_select = False
            
            if gender == 'Female' and remaining_female > 0:
                can_select = True
            elif gender == 'Male' and remaining_male > 0:
                can_select = True
            elif remaining_female == 0 and gender == 'Male':
                # Force male selection if no female quota left
                can_select = True
            elif remaining_male == 0 and gender == 'Female':
                # Force female selection if no male quota left
                can_select = True
            
            if can_select:
                namesList.append(candidate)
                used_names.add(name_key)
                race_counts[race] += 1
                gender_counts[gender] += 1
                remaining_race_targets[race] -= 1
                
                if gender == 'Female':
                    remaining_female = max(0, remaining_female - 1)
                else:
                    remaining_male = max(0, remaining_male - 1)
        
        # Final adjustment phase: Fill any remaining slots
        if len(namesList) < total_names_needed:
            print(f'Phase 1 selected {len(namesList)}/{total_names_needed} names, filling remaining slots...')
            
            # Collect all unused candidates
            unused_candidates = []
            for candidate, race, _ in all_candidates:
                name_key = (candidate['fname'], candidate['lname'], candidate['gender'])
                if name_key not in used_names:
                    unused_candidates.append(candidate)
            
            random.shuffle(unused_candidates)
            
            # Fill remaining slots
            for candidate in unused_candidates:
                if len(namesList) >= total_names_needed:
                    break
                    
                name_key = (candidate['fname'], candidate['lname'], candidate['gender'])
                if name_key not in used_names:
                    namesList.append(candidate)
                    used_names.add(name_key)
                    race_counts[candidate['race'].capitalize()] += 1
                    gender_counts[candidate['gender']] += 1
        
        # Final validation and reporting
        if len(namesList) != total_names_needed:
            print(f'Warning: Expected {total_names_needed} names, got {len(namesList)}')
        
        current_female_pct = gender_counts['Female'] / len(namesList) * 100 if namesList else 0
        target_female_pct = 60
        
        print(f'Selected names by race: {race_counts["White"]} White ({race_counts["White"]/len(namesList)*100:.1f}%), '
              f'{race_counts["Hispanic"]} Hispanic ({race_counts["Hispanic"]/len(namesList)*100:.1f}%), '
              f'{race_counts["Black"]} Black ({race_counts["Black"]/len(namesList)*100:.1f}%), '
              f'{race_counts["Asian"]} Asian ({race_counts["Asian"]/len(namesList)*100:.1f}%)')
        print(f'Selected names by gender: {gender_counts["Female"]} Female ({gender_counts["Female"]/len(namesList)*100:.1f}%), '
              f'{gender_counts["Male"]} Male ({gender_counts["Male"]/len(namesList)*100:.1f}%)')
        
        if abs(current_female_pct - target_female_pct) > 5:  # Alert if more than 5% off
            print(f'ALERT: Gender distribution is {current_female_pct:.1f}% female, target was {target_female_pct}%')
        
        random.shuffle(namesList)
        image_sets = createFacesPattern(namesList)
        user_instance = UserPattern.objects.create(
            user_id = id,
            user_movies_pattern = str(randomMovieslist),
            user_names_pattern = str(namesList),
            user_faces_pattern = str(image_sets),
            movie_index = 0,
            names_index = 0,
        )
        print('User created with improved name distribution')
    except Exception as e:
        print(e)

@api_view(["GET"])
def getImage(request, data):
    first_name,index = data.split(',')
    fname = Fname.objects.filter(first_name=first_name)[0]
    race = fname.race.lower()
    setFaces = []
    pattern = r'_#'+str(index)+r'_'
    for f in onlyfiles:
        if pattern in f:
            if race in f:
                setFaces.append(f)
                continue
    img = str(random.choice(setFaces))
    image_data = open(images_path+img, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")

@api_view(["POST"])
def getFaces(data):
    try:
        user_id = str(data.body.decode("utf-8").strip())
        index = model_to_dict(UserPattern.objects.get(user_id=user_id))['faces_index']  
        facesList = ast.literal_eval(model_to_dict(UserPattern.objects.get(user_id=user_id))['user_faces_pattern'])
        res = []
        for i in range(index,index+3):
            res.append(facesList[i])
        UserPattern.objects.filter(user_id=user_id).update(faces_index = index+3)
        return JsonResponse(res,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

@api_view(["POST"])
def getNames(data):
    try:
        user_id = str(data.body.decode("utf-8").strip())
        index = model_to_dict(UserPattern.objects.get(user_id=user_id))['names_index']  
        namesList = ast.literal_eval(model_to_dict(UserPattern.objects.get(user_id=user_id))['user_names_pattern'])
        res = []
        for i in range(index,index+3):
            res.append(namesList[i])
        UserPattern.objects.filter(user_id=user_id).update(names_index = index+3)
        return JsonResponse(res,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

@api_view(["POST"])
def getMovies(data):
    try:
        user_id = str(data.body.decode("utf-8").strip())
        index = model_to_dict(UserPattern.objects.get(user_id=user_id))['movie_index']  
        moviesList = ast.literal_eval(model_to_dict(UserPattern.objects.get(user_id=user_id))['user_movies_pattern'])
        movies_indexes = []
        for i in range(index,index+3):
            movies_indexes.append(moviesList[i])
        UserPattern.objects.filter(user_id=user_id).update(movie_index = index+3)
        movies = [model_to_dict(Movie.objects.get(id=movie_id+206)) for movie_id in movies_indexes]
        return JsonResponse(movies,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

@api_view(["GET"])
def getDynamics(request):
    return JsonResponse(model_to_dict(Dynamic.objects.first()),safe=False)

@api_view(["GET"])
def getMoviesCount(request):
    return JsonResponse(len(Movie.objects.all()),safe=False)

@api_view(["GET"])
def getFNamesCount(request):
    return JsonResponse(len(Fname.objects.all()),safe=False)

@api_view(["GET"])
def createFnames(request):
    try:
        with open('DB_Data/fname.json') as f:
            data = json.load(f)
            for fname in data[2]['data']:
                fname_instance = Fname.objects.create(
                    first_name=fname['first_name'],
                    race=fname['race'],
                    gender=fname['gender'])
        return JsonResponse('First names created!',safe=False)
    except ValueError as e:
        print("----Error----")
        return response(e.args[0])

@api_view(["GET"])
def createLnames(request):
    try:
        with open('DB_Data/lname.json') as f:
            data = json.load(f)
            for lname in data[2]['data']:
                fname_instance = Lname.objects.create(
                    last_name=lname['last_name'],
                    race=lname['race'])
        return JsonResponse('Last names created!',safe=False)
    except ValueError as e:
        print("----Error----")
        return response(e.args[0])

@api_view(["GET"])      
def createMovies(request):
    try:
        with open('DB_Data/movies_1.json') as f:
            data = json.load(f)
            for movie in data[2]['data']:
                movie_instance = Movie.objects.create(
                    title=movie['title'],
                    review=movie['review'],
                    link=movie['link'],
                    rating=movie['rating'],
                    image_url=movie['image_link'],
                    length = movie['length'],
                    genre = movie['genre'],
                    release_date = movie['release_date'],
                    )
        return JsonResponse('Movies created!',safe=False)
    except ValueError as e:
        print("----Error----")
        return response(e.args[0])

@api_view(["GET"])      
def createUpdatedMovies(request):
    try:
        data = pd.read_csv('DB_Data/trim_movies.csv')
        for i in range(len(data)):
            # print(data.iloc[[i]]['Title'].values[0])
            movie_instance = Movie.objects.create(
                    title=data.iloc[[i]]['Title'].values[0],
                    review=data.iloc[[i]]['Review'].values[0],
                    link=data.iloc[[i]]['link'].values[0],
                    rating=int(data.iloc[[i]]['Rating'].values[0]),
                    image_url=data.iloc[[i]]['image_link'].values[0],
                    length = data.iloc[[i]]['Length'].values[0],
                    genre = data.iloc[[i]]['Genre'].values[0],
                    release_date = data.iloc[[i]]['Released_date'].values[0],
                    )

        return JsonResponse('Movies created!',safe=False)
    except ValueError as e:
        print("----Error----")
        return response(e.args[0])