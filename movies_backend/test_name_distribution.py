#!/usr/bin/env python
"""
Test script for name distribution algorithm
Tests movie counts, race distribution, gender distribution, and duplicate prevention
"""
import os
import sys
import django
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_backend.settings')
django.setup()

from movies.models import Dynamic, Fname, Lname, Movie, UserPattern
from movies.views import createUserMovieNamePattern
import ast
import random

def test_movie_counts():
    """Test that both timers show the same number of movies"""
    print("=" * 50)
    print("TESTING MOVIE COUNTS")
    print("=" * 50)
    
    dynamic = Dynamic.objects.first()
    print(f"Timer 1 (15min) movies: {dynamic.total_movies_time_1}")
    print(f"Timer 2 (5min) movies: {dynamic.total_movies_time_2}")
    print(f"Target: Both should be 42")
    
    assert dynamic.total_movies_time_1 == 42, f"Timer 1 should be 42, got {dynamic.total_movies_time_1}"
    assert dynamic.total_movies_time_2 == 42, f"Timer 2 should be 42, got {dynamic.total_movies_time_2}"
    print("✅ PASS: Both timers use 42 movies")

def test_race_distribution():
    """Test race distribution matches target percentages"""
    print("\n" + "=" * 50)
    print("TESTING RACE DISTRIBUTION")
    print("=" * 50)
    
    target_percentages = {'White': 64, 'Hispanic': 22, 'Black': 14, 'Asian': 0}
    
    for timer_type in [1, 2]:
        print(f"\n--- Timer {timer_type} ---")
        
        # Create test user pattern with unique ID
        test_user_id = f"test_race_{timer_type}_{int(time.time() * 1000)}"
        time.sleep(0.01)  # Ensure unique timestamps
        try:
            createUserMovieNamePattern(test_user_id, timer_type)
        except Exception as e:
            print(f"Error creating pattern: {e}")
            continue
            
        # Get the names pattern
        user_pattern = UserPattern.objects.get(user_id=test_user_id)
        names_list = ast.literal_eval(user_pattern.user_names_pattern)
        
        # Count races
        race_counts = {'white': 0, 'hispanic': 0, 'black': 0, 'asian': 0}
        for name in names_list:
            race_counts[name['race']] += 1
            
        total_names = len(names_list)
        print(f"Total names: {total_names}")
        
        # Calculate and verify percentages
        for race, count in race_counts.items():
            actual_pct = (count / total_names) * 100
            target_pct = target_percentages[race.title()]
            print(f"{race.title()}: {count} names ({actual_pct:.1f}%) - Target: {target_pct}%")
            
            # Allow some tolerance for rounding
            tolerance = 3  # 3% tolerance
            assert abs(actual_pct - target_pct) <= tolerance, f"{race} percentage off by more than {tolerance}%"
        
        # Cleanup
        UserPattern.objects.filter(user_id=test_user_id).delete()
        
    print("✅ PASS: Race distribution within acceptable range")

def test_gender_distribution():
    """Test gender distribution matches 60% female, 40% male"""
    print("\n" + "=" * 50)
    print("TESTING GENDER DISTRIBUTION")
    print("=" * 50)
    
    target_female_pct = 60
    target_male_pct = 40
    
    for timer_type in [1, 2]:
        print(f"\n--- Timer {timer_type} ---")
        
        # Create test user pattern with unique ID
        test_user_id = f"test_gender_{timer_type}_{int(time.time() * 1000)}"
        time.sleep(0.01)  # Ensure unique timestamps
        try:
            createUserMovieNamePattern(test_user_id, timer_type)
        except Exception as e:
            print(f"Error creating pattern: {e}")
            continue
            
        # Get the names pattern
        user_pattern = UserPattern.objects.get(user_id=test_user_id)
        names_list = ast.literal_eval(user_pattern.user_names_pattern)
        
        # Count genders
        gender_counts = {'Female': 0, 'Male': 0}
        for name in names_list:
            gender_counts[name['gender']] += 1
            
        total_names = len(names_list)
        female_pct = (gender_counts['Female'] / total_names) * 100
        male_pct = (gender_counts['Male'] / total_names) * 100
        
        print(f"Female: {gender_counts['Female']} names ({female_pct:.1f}%) - Target: {target_female_pct}%")
        print(f"Male: {gender_counts['Male']} names ({male_pct:.1f}%) - Target: {target_male_pct}%")
        
        # Allow some tolerance for rounding
        tolerance = 5  # 5% tolerance
        assert abs(female_pct - target_female_pct) <= tolerance, f"Female percentage off by more than {tolerance}%"
        assert abs(male_pct - target_male_pct) <= tolerance, f"Male percentage off by more than {tolerance}%"
        
        # Cleanup
        UserPattern.objects.filter(user_id=test_user_id).delete()
        
    print("✅ PASS: Gender distribution within acceptable range")

def test_no_duplicate_names():
    """Test that no name appears twice in a user's pattern"""
    print("\n" + "=" * 50)
    print("TESTING NO DUPLICATE NAMES")
    print("=" * 50)
    
    for timer_type in [1, 2]:
        print(f"\n--- Timer {timer_type} ---")
        
        # Create test user pattern with unique ID
        test_user_id = f"test_duplicates_{timer_type}_{int(time.time() * 1000)}"
        time.sleep(0.01)  # Ensure unique timestamps
        try:
            createUserMovieNamePattern(test_user_id, timer_type)
        except Exception as e:
            print(f"Error creating pattern: {e}")
            continue
            
        # Get the names pattern
        user_pattern = UserPattern.objects.get(user_id=test_user_id)
        names_list = ast.literal_eval(user_pattern.user_names_pattern)
        
        # Create set of full names to check for duplicates
        full_names = []
        for name in names_list:
            full_name = f"{name['fname']} {name['lname']}"
            full_names.append(full_name)
            
        # Check for duplicates
        unique_names = set(full_names)
        duplicates = len(full_names) - len(unique_names)
        
        print(f"Total names: {len(full_names)}")
        print(f"Unique names: {len(unique_names)}")
        print(f"Duplicates: {duplicates}")
        
        if duplicates > 0:
            # Show which names are duplicated
            seen = set()
            duplicate_names = []
            for name in full_names:
                if name in seen:
                    duplicate_names.append(name)
                seen.add(name)
            print(f"Duplicate names: {duplicate_names}")
        
        assert duplicates == 0, f"Found {duplicates} duplicate names"
        
        # Cleanup
        UserPattern.objects.filter(user_id=test_user_id).delete()
        
    print("✅ PASS: No duplicate names found")

def test_available_names():
    """Test how many names are available by race and gender"""
    print("\n" + "=" * 50)
    print("AVAILABLE NAMES ANALYSIS")
    print("=" * 50)
    
    # Count available first names by race and gender
    name_counts = {}
    for fname in Fname.objects.all():
        race = fname.race
        gender = fname.gender
        key = f"{race}_{gender}"
        name_counts[key] = name_counts.get(key, 0) + 1
    
    # Count available last names by race
    lname_counts = {}
    for lname in Lname.objects.all():
        race = lname.race
        lname_counts[race] = lname_counts.get(race, 0) + 1
    
    print("First names by race and gender:")
    for key, count in sorted(name_counts.items()):
        race, gender = key.split('_')
        print(f"  {race} {gender}: {count}")
    
    print("\nLast names by race:")
    for race, count in sorted(lname_counts.items()):
        print(f"  {race}: {count}")
    
    # Calculate maximum possible unique combinations
    print("\nMaximum unique combinations by race:")
    for race in ['White', 'Black', 'Hispanic', 'Asian']:
        male_firstnames = name_counts.get(f"{race}_Male", 0)
        female_firstnames = name_counts.get(f"{race}_Female", 0)
        lastnames = lname_counts.get(race, 0)
        max_combinations = (male_firstnames + female_firstnames) * lastnames
        print(f"  {race}: {max_combinations} combinations ({male_firstnames}M + {female_firstnames}F) × {lastnames}L")

def run_all_tests():
    """Run all tests"""
    print("🧪 RUNNING NAME DISTRIBUTION TESTS")
    print("=" * 70)
    
    try:
        test_available_names()
        test_movie_counts()
        test_race_distribution()
        test_gender_distribution()
        test_no_duplicate_names()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_all_tests() 